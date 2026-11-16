from App.Module.Utility import *
from flask import request
import os

# [JSON] Fetch multiple Request-Logs records
def Records(params:dict = {}) -> tuple:
  try:
    # Context
    CTX = createContext(params)
    res = CTX['Response']

    # List logs files
    records = listRequestLogs(CTX)

    # Count files
    total = len(records)

    # Response-Body (JSON)
    res['Body'] = {
      'Total': total,
      'Records': records,
    }

    # HTTP-Response (body,status,headers)
    return responseTuple(CTX)
  except Exception as e:
    raise

# [JSON] Fetch single Request-Logs record
def Record(params:dict = {}) -> tuple:
  try:
    # Context
    CTX = createContext(params)
    res = CTX['Response']

    # QueryString
    key = request.args.get('key')

    # [400/BadRequest] required query "key"
    if key == None:
      return responseError(400)

    # Find Request-Log file
    find = '{path}/{key}'
    find = find.format(**{
      'path': CTX['Path']['RequestContext'],
      'key': key,
    })

    # [404/NotFound] file not found
    if not os.path.isfile(find):
      return responseError(404)

    # Read JSON-File + Response-Body (JSON)
    res['Body'] = jsonLoad(find)

    # HTTP-Response (body,status,headers)
    return responseTuple(CTX)
  except Exception as e:
    raise

# [JSON] Clear Request-Logs
def Clear(params:dict = {}) -> tuple:
  try:
    # Context
    CTX = createContext(params)
    res = CTX['Response']

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
      'Path': {
        'RequestContext': '.temp/request-logs', 
        'RequestHistory': '.temp/request-logs.csv', 
      }
    }

    # (dict)
    return CTX
  except Exception as e:
    raise

# List Request-Logs files
def listRequestLogs(CTX:dict) -> list:
  try:
    
    # default output
    records = []

    # List files in directory
    files = listFiles(CTX['Path']['RequestContext'])

    # Ignore error?
    if files == None:
      return records

    # Add files into records
    for index, path in enumerate(files):

      # Get file created time (timestamp)
      created = os.path.getctime(path)

      # Get file basename
      basename = os.path.basename(path)

      # Update records
      records.append({
        'key': basename,
        'created': created,
      })

    # Sort by created time (DESC)
    records.sort(key=lambda x: x['created'], reverse=True)

    # (list)
    return records
  except Exception as e:
    raise

# Delete request-context files
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
        deleted.append(key)

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


# [response] Convert CTX[Response] to tuple (Body, Status, Headers)
def responseTuple(CTX:dict) -> tuple:

  # shortcut Response
  res = CTX['Response']

  return (
    res['Body'],    # str|list|dict
    res['Status'],  # int [200,4XX,5XX]
    res['Headers'], # dict
  )

# [response]
def responseError(code:int) -> tuple:

  # Mapping Error-Code => Message
  mapping = {
    400: 'bad request',
    404: 'not found',
  }

  # JSON-Body
  body = {
    'code': code,
    'error': mapping[code],
  }

  # (tuple)
  return (body,body['code'])