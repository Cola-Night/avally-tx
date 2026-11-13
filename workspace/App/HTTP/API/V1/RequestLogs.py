from App.Module.Utility import *
from flask import request
import os

# [JSON] List Request-Logs records (multiple)
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

# [JSON] Read Request-Logs JSON-File
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
      'path': CTX['Path'],
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

    # List logs files
    records = listRequestLogs(CTX)

    # List deleted files
    deleted = []

    # Delete Request-Logs files
    for index, record in enumerate(records):
      if os.path.exists(record['path']):
        # Delete file
        os.remove(record['path'])
        # Deleted record
        deleted.append(record)

    # Update Response-Body
    res['Body'] = {
      'code': 200,
      'message': 'request-logs clear',
      'records': deleted,
    }

    # HTTP-Response (body,status,headers)
    return responseTuple(CTX)

  except Exception as e:
    raise





# [init] Create Context (CTX)
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
      'Path': '.temp/request-logs',
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
    files = listFiles(CTX['Path'])

    # Ignore error?
    if files == None:
      return records

    # Add files into records
    for index, path in enumerate(files):

      # Get file created time (timestamp)
      created = os.path.getctime(path)

      # Update records
      records.append({
        'path': path,
        'created': created,
      })

    # Sort by created time (DESC)
    records.sort(key=lambda x: x['created'], reverse=True)

    # (list)
    return records
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