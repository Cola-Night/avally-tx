from App.Module.Utility import *
from App.Module.MacroCSV import MacroCSV
from flask import Flask, request, jsonify, send_from_directory, redirect, abort
from flask_cors import CORS
from datetime import datetime, timezone
from typing import Any
import importlib
import uuid
import json
import os

# Flask (HTTP/Web service)
server = Flask(__name__,
  static_url_path='',
  static_folder='Public',
)

# Cross-Origin by pathname prefix
CORS(server, resources={
  r"/api/*": {
    "origins": "*",
    "methods": ["GET", "POST"]
  },
  r"/taxone-API/*": {
    "origins": "*",
    "methods": ["GET", "POST"]
  },
})

# [Utility] shortcut to HTTP-Controller file (App/HTTP/*.py)
def http_controller(controller:str, params:dict = {}) -> Any:
  
  # Split [ModulePath, CallbackFunction]
  path, callback = controller.split('@')

  # Dynamic import module (by path)
  module = importlib.import_module(path)
  module = importlib.reload(module)

  # Find callback function in module
  callback = getattr(module,callback)

  # Execute callback (Any)
  response = callback(params)

  # (int | tuple)
  return response

# [HTTP-Request-Log] log Request-History into CSV-File
def log_request_history() -> str:
  try:
    # Handling multiple CSV
    log = MacroCSV()

    # Prepare CSV-Writer
    log.create(
      file='.temp/request-logs/#request-logs.csv',
      name='RequestLogs',
      headers=[
        'DateTime',
        'Method',
        'URL',
        'Query',
        'Context',
      ],
    )

    # Get current DateTime "2026-12-31T23:59:59+00:00"
    current_dt = datetime.now(timezone.utc)
    current_dt = current_dt.isoformat()

    # Request-Context (json-file save location)
    context = log_request_context()

    # (string) Raw-QueryString (bytes->string)
    query = request.query_string
    query = query.decode('utf-8')

    # Append new request-history (CSV-Row)
    # Note: use "name" as shortcut when append new row
    log.append('RequestLogs',[
      current_dt,
      request.method,
      request.path,
      query,
      context['code'],
    ])
  except Exception as e:
    raise

# [HTTP-Request-Log] Log Request-Context into JSON-File (Request-Body details)
def log_request_context() -> dict:
  try:
    # Loop until file is unique
    while True:

      # Unique code
      code = uuid.uuid4()

      # basename (filename.ext)
      basename = 'req-{code}.json'
      basename = basename.format(**{
        'code': code,
      })

      # Request-Log save location
      save = '.temp/request-logs/{basename}'
      save = save.format(**{
        'basename': basename,
      })

      # Stop when file is unique
      if not os.path.isfile(save):
        break

    # Parent directories
    parent = os.path.dirname(save)

    # Create missing directories
    if not os.path.isdir(parent):
      os.makedirs(parent, exist_ok=True)

    # Request-Headers
    headers = dict(request.headers)

    # (list) QueryString (split "&")
    queries = request.query_string
    queries = queries.decode('utf-8')
    queries = queries.split('&')

    # Request-Body (default)
    body = None

    # Rquest-Body
    if request.method != 'GET':
      body = request.get_data()   # RAW-Bytes 
      body = body.decode('utf-8') # Bytes to String
      body = body.splitlines()    # Split LineBreak

    # Save Request-Context (JSON-file)
    jsonSave(save,{
      'method':   request.method,
      'pathname': request.path,
      'headers':  headers,
      'queries':  queries,
      'body':     body,
    })

    # (dict)
    return {
      'code': code,
      'save': save,
      'basename': basename,
    }
  except Exception as e:
    raise





# [HTML] Error-404 page
@server.errorhandler(404)
def error_404(error):
  log_request_history()
  return send_from_directory(
    directory='Resources/HTML',
    path='Error-404.html',
  )

# [HTML] Home page
@server.route('/',methods=['GET'])
def index():
  log_request_history()
  return send_from_directory(
    directory='Public',
    path='index.html',
  )

# [Media] Response Media-File from "Storage/CDN/..."
@server.route('/cdn/<path:filepath>')
def file_cdn(filepath):
  log_request_history()
  return http_controller(
    controller='App.HTTP.CDN@main',
    params={
      'filepath':filepath,
    }
  )

# [HTML] Request-Logs page
@server.route('/request-logs')
def request_logs_index():

  # required secret cookie to access
  if 'secret' not in request.cookies:
    return abort(404) # fake 404 (real=403)

  # Get cookie value
  value = request.cookies.get('secret')

  # Todo: fix cookie value
  if value != 'AVALLY_Test':
    return abort(404) # fake 404 (real=403)

  # (text/html) Response
  return send_from_directory(
    directory='Resources/HTML/Request-Logs',
    path='Index.html',
  )





# [JSON/TaxOne-API] /taxone-API/V2.1/etax/receipt
# SAP SOAP-Payload -> Convert-Payload -> Send to OneTax-API
@server.route('/taxone-API/V2.1/etax/receipt',methods=['POST'])
def api_taxone_etax_receipt() -> tuple:
  log_request_history()
  return http_controller(
    controller='App.HTTP.TaxOneAPI.eTaxReceipt@main',
    params={},
  )




# [JSON|API-V1|Request-Logs] List records (multiple)
@server.route('/api/v1/request-logs/records.json', methods=['GET'])
def api_v1_request_logs_records():
  return http_controller('App.HTTP.API.V1.RequestLogs@Records')

# [JSON|API-V1|Request-Logs] Request-Context details
@server.route('/api/v1/request-logs/record.json', methods=['GET'])
def api_v1_request_logs_record():
  return http_controller('App.HTTP.API.V1.RequestLogs@Record')

# [JSON|API-V1|Request-Logs] Clear logs
@server.route('/api/v1/request-logs/clear.json', methods=['POST'])
def api_v1_request_logs_clear():
  return http_controller('App.HTTP.API.V1.RequestLogs@Clear')



# Start WebServer
if __name__ == '__main__':
  server.run(
    debug=True,
    host='0.0.0.0',
    port=8000,
  )