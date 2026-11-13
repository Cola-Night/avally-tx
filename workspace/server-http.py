from App.Module.Utility import *
from flask import Flask, request, jsonify, send_from_directory, redirect, abort
from flask_cors import CORS
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

# Set Cross-Origin by pathname prefix
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

# [Utility] HTTP-Controller shortcut
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

# [Utility] Log HTTP-Request data
def log_request() -> str:
  try:
    # Request-Log save location
    save = '.temp/request-logs/req-{code}.json'
    save = save.format(**{
      'code': uuid.uuid4(),
    })

    # Parent directories
    parent = os.path.dirname(save)

    # Create missing directories
    if not os.path.isdir(parent):
      os.makedirs(parent, exist_ok=True)

    # Request-Headers
    headers = dict(request.headers)

    # Rquest-Body
    body = request.get_data()   # RAW-Bytes 
    body = body.decode('utf-8') # Bytes to String
    body = body.splitlines()    # Split LineBreak

    # Save Request-Log
    jsonSave(save,{
      'method': request.method,
      'url': request.url,
      'headers': headers,
      'body': body,
    })

    # (string) file save location
    return save
  except Exception as e:
    raise


# [HTML/Error-404] Error Page
@server.errorhandler(404)
def error_404(error):
  log_request()
  return send_from_directory(
    directory='Resources/HTML',
    path='Error-404.html',
  )

# [HTML/Home]
@server.route('/',methods=['GET'])
def index():
  log_request()
  return send_from_directory(
    directory='Public',
    path='index.html',
  )

# [MediaFile] Response MediaFile from "Storage/CDN/..."
@server.route('/cdn/<path:filepath>')
def file_cdn(filepath):
  return http_controller(
    controller='App.HTTP.CDN@main',
    params={
      'filepath':filepath,
    }
  )



# [HTML/Request-Logs] list
@server.route('/request-logs')
def request_logs_index():
  return send_from_directory(
    directory='Resources/HTML/Request-Logs',
    path='Index.html',
  )

# [HTML/Request-Logs] View record
@server.route('/request-logs/record')
def request_logs_record():
  return send_from_directory(
    directory='Resources/HTML/Request-Logs',
    path='Record.html',
  )



# todo: research methods
# [JSON/TaxOne-API] /taxone-API/V2.1/etax/receipt
# SAP SOAP-Payload -> Convert-Payload -> Send to OneTax-API
@server.route(
  '/taxone-API/V2.1/etax/receipt',
  methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
)
def api_taxone_etax_receipt() -> tuple:
  log_request()
  return http_controller(
    controller='App.HTTP.TaxOneAPI.eTaxReceipt@main',
    params={},
  )



# [JSON|API-V1|Request-Logs] List records (multiple)
@server.route('/api/v1/request-logs/records.json', methods=['GET'])
def api_v1_request_logs_records():
  return http_controller('App.HTTP.API.V1.RequestLogs@Records')

# [JSON|API-V1|Request-Logs] View record (single)
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