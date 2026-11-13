from App.Module.Utility import *
from flask import request
import uuid
import os

# API.V1.Test@main
# [GET|POST|PUT] /api/v1/test.json
# Testing client HTTP-Request
def main(params:dict = {}):
  try:
    # Request [Method, Headers, Queries]
    method  = request.method
    headers = dict(request.headers)
    queries = request.args.to_dict()

    # Request-Body (use Header[Content-Type])
    body = parseRequestBody(headers)

    # Request-Log save location
    save = '.temp/request-test/{code}.json'
    save = save.format(**{
      'code': uuid.uuid4(),
    })

    # Get parent directories
    parent = os.path.dirname(save)

    # Create missing dir
    if not os.path.isdir(parent):
      os.makedirs(parent, exist_ok=True)

    # Save Request-Log into JSON-File
    jsonSave(save,{
      'method': method,
      'headers': headers,
      'queries': queries,
      'body': body,
    })

    # Response-Body (JSON)
    response = {
      'status':   200,
      'method':   method,
      'headers':  headers,
      'queries':  queries,
      'body':     body,
    }

    # HTTP-Response
    return response
  except Exception as e:
    raise

# parse RequestBody
def parseRequestBody(headers:dict):
  try:
    # default output
    body = None

    # Missing "Content-Type"
    if 'Content-Type' not in headers:
      return body

    # Split Content-Type data
    CT = headers['Content-Type']
    CT = CT.split(';')

    # Use MIME-Type to select parse body method
    match CT[0]:
      case 'application/json':
        body = request.get_json()
      case 'multipart/form-data':
        # Raw Body
        raw = request.get_data()  # RAW-Bytes 
        raw = raw.decode('utf-8') # Convert Bytes to String
        raw = raw.splitlines()    # Split Line-Breaks
        # FormData
        FM = request.form.to_dict()
        # Update output
        body = {
          'FormData': FM,
          'Raw': raw,
        }
      case _:
        body = request.get_data()   # RAW-Bytes 
        body = body.decode('utf-8') # Convert Bytes to String
        body = body.splitlines()    # Split Line-Breaks

    # (RequestBody)
    return body
  except Exception as e:
    raise
