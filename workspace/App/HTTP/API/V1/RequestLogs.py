from App.Module.MacroCSV import MacroCSV
from App.Module.Utility import *
from flask import request
import os

# [Response/JSON] Fetch multiple Request-Logs records
def Records(params:dict = {}) -> tuple:
  try:
    # Context
    CTX = createContext(params)
    res = CTX['Response']
    
    # [middleware]
    # Required secret cookie to access API
    if validSecretCookie(CTX) == False:
      return responseError(403)

    # QueryString
    query = {
      'skip':  request.args.get('skip', default=0, type=int),
      'limit': request.args.get('limit', default=100, type=int),
    }

    # List logs files
    records = listRecords(CTX,query)

    # Response-Body (JSON)
    res['Body'] = {
      'Query':  query,
      'Records': records,
    }

    # HTTP-Response (body,status,headers)
    return responseTuple(CTX)
  except Exception as e:
    raise

# [Response/JSON] Fetch single Request-Logs record
def Record(params:dict = {}) -> tuple:
  try:
    # Context
    CTX = createContext(params)
    res = CTX['Response']
    
    # Required secret cookie to access API
    if validSecretCookie(CTX) == False:
      return responseError(403)

    # QueryString - Request-Context-Key
    key = request.args.get('key')

    # [400/BadRequest] required query "key"
    if key == None:
      return responseError(400)

    # Use "key" to find Request-Context file
    find = '{path}/req-{key}.json'
    find = find.format(**{
      'path': CTX['Path']['RequestContext'],
      'key': key,
    })

    # [404/NotFound] Request-Context file not found
    if not os.path.isfile(find):
      return responseError(404)

    # Read JSON-File + Response-Body (JSON)
    res['Body'] = jsonLoad(find)

    # HTTP-Response (body,status,headers)
    return responseTuple(CTX)
  except Exception as e:
    raise

# [Response/JSON] Clear Request-Logs
def Clear(params:dict = {}) -> tuple:
  try:
    # Context
    CTX = createContext(params)
    res = CTX['Response']

    # Required secret cookie to continue
    if validSecretCookie(CTX) == False:
      return responseError(403)

    # processing
    deleteRequestContext(CTX)
    truncateRequestHistory(CTX)

    # Update Response-Body
    res['Body'] = {
      'code': 200,
      'message': 'request-logs clear',
      'records': CTX['DeletedContexts'],
    }

    # HTTP-Response (body,status,headers)
    return responseTuple(CTX)
  except Exception as e:
    raise





# [init] Global Context / Shared config data
def createContext(params:dict = {}) -> dict:
  try:
    # Context
    CTX = {
      'Params': params,
      'Response': {
        'Status': 200,
        'Body': {},
        'Headers': {},
      },
      'Auth': {
        'CookieKey': 'secret',
        'CookieVal': 'AVALLY_Test',
      },
      'Path': {
        'RequestContext': '.temp/request-logs', 
        'RequestHistory': '.temp/request-logs/#request-logs.csv', 
      }
    }

    # (dict)
    return CTX
  except Exception as e:
    raise

# List Request-Logs records from CSV
def listRecords(CTX:dict, options:dict = {}) -> list:
  try:
    # Handling multiple CSV
    log = MacroCSV()

    # Create/Load CSV-File (input row=list)
    log.create(
      file=CTX['Path']['RequestHistory'],
      name='RequestLogs',
      headers=[
        'DateTime',
        'Method',
        'URL',
        'Query',
        'Context',
      ],
    )

    # default limit
    if 'limit' not in options:
      options['limit'] = 100

    # default skip
    if 'skip' not in options:
      options['skip'] = 0

    # Get Request-Logs records
    records = log.getRecords(
      name  = 'RequestLogs',
      limit = options['limit'],
      skip  = options['skip'],
    )

    # (list)
    return records
  except Exception as e:
    raise

# Delete all Request-Context (JSON) files
def deleteRequestContext(CTX:dict) -> list:
  try:
    records = listRequestLogs(CTX)
    deleted = []

    # Delete Request-Logs files
    for index, record in enumerate(records):
      
      # Convert record-key to filepath (.json)
      filepath = '{path}/{key}'
      filepath = filepath.format(**{
        'path': CTX['Path']['RequestContext'],
        'key': record['key'],
      })

      # Delete Request-Context file (.json)
      if os.path.exists(filepath):
        os.remove(filepath)
        deleted.append(record['key'])

    # Update App-Context
    CTX['DeletedContexts'] = deleted

    # (list) deleted files
    return deleted
  except Exception as e:
    raise

# Clear Request-History CSV
def truncateRequestHistory(CTX:dict) -> bool:
  try:
    # Request-History file (CSV)
    history = CTX['Path']['RequestHistory']

    # (bool=False) failed
    # Request-History file not exists
    if not os.path.isfile(history):
      return False

    # Read CSV First-Line
    with open(history, "r") as f:
      first_line = f.readline()

    # Clear CSV (except First-Line)
    with open(history, "w") as f:
      f.write(first_line)

    # (bool=True) success
    return True
  except Exception as e:
    raise

# Has secrect Cookie
def validSecretCookie(CTX:dict) -> bool:
  try:
    # Shortcut context
    auth = CTX['Auth']

    # auth cookie-key missing
    if auth['CookieKey'] not in request.cookies:
      return False
    
    # Get cookie.secret value
    value = request.cookies.get(auth['CookieKey'])

    # Invalid Cookie-Value
    if auth['CookieVal'] != value:
      return False

    # (bool=True) success
    return True
  except Exception as e:
    raise



# [response-helper] Convert CTX[Response] to tuple (Body, Status, Headers)
def responseTuple(CTX:dict) -> tuple:

  # shortcut Response
  res = CTX['Response']

  return (
    res['Body'],    # str|list|dict
    res['Status'],  # int [200,4XX,5XX]
    res['Headers'], # dict
  )

# [response-helper]
def responseError(code:int) -> tuple:

  # Mapping Error-Code => Message
  mapping = {
    400: 'bad request',
    403: 'forbidden',
    404: 'not found',
  }

  # JSON-Body
  body = {
    'code': code,
    'error': mapping[code],
  }

  # (tuple)
  return (body,body['code'])