from App.Module.Utility import *
from flask import request
from typing import Any
import xmltodict
import requests
import uuid
import os

# [module]: App.HTTP.TaxOneAPI.eTaxReceipt@main
# [url]: /taxone-API/V2.1/etax/receipt

# S4HANA CommunicationArrangement, Outbound:
# - eDocument Thailand: Send Tax Invoice
# - eDocument Thailand: Send Debit/Credit Note
# - eDocument Thailand: Send Receipt
# - eDocument Thailand: Get Status

# tuple = HTTP-Response (Body, StatusCode, Headers)
def main(params:dict = {}) -> tuple:

  # Context
  CTX = {
    'Params': params,
    'Request': {
      'method': '',
      'headers': {},
      'body':  '',
    },
    'Response': {
      'status': 200,
      'headers': {
        'Content-Type': 'text/xml',
      },
      'body': {},
    },
    'SAP': {
      'ContentType': [],
      'Authorization': {},
      'SoapAction': {},
      'SoapPayload': {},
    },
    'TaxOne': {},
  }

  # Stop when Response.status NOT 200
  response = proccessing(CTX,[
    initParams,           # 200|500 Custom parameters / Config
    initRequest,          # 200|400 HTTP-Request + update Context

    validReqMethod,       # 200|400 Request.Method
    validReqContentType,  # 200|40X Request.Header[Content-Type]
    # validReqAuth,         # 200|40X Request.Header[Authorization]
    # validReqSoapAction,   # 200|40X Request.Header[SOAPAction]
    validReqBody,         # 200|40X Request.Body

    # sapToTaxOne,          # 200|500 Build-Payload for TaxOneAPI
    # taxOneSubmit,         # 200|??? send Payload to TaxOneAPI
    # taxOneValidate,       # 200|??? Validate TaxOneAPI.response
    responseBody,         # 200|??? Build Response [Body]
  ])

  # HTTP-Response (body, status, headers)
  return response

# [main] Pipe-Line proccessing
def proccessing(CTX:dict, process:list = []) -> tuple:

  # Shortcut context
  res = CTX['Response']

  # Execute each callback 
  # Break when StatusCode NOT 200
  for callback in process:

    # Break when Response.status changed (NOT 200)
    if res['status'] != 200:
      break

    # Execute callback
    output = callback(CTX)

    # Skip NULL/None
    if output == None:
      continue

    # Overwrite Response.StatusCode
    if isinstance(output, int):
      res['status'] = output

    # Overwrite Response.Body
    if isinstance(output, tuple):
      res['status']  = output[0]
      res['body']    = output[1]
      res['headers'] = output[2]

  # (tuple) HTTP-Response
  return (
    res['body'],    # str|list|dict
    res['status'],  # int [200|4XX,5XX]
    res['headers'], # dict
  )



# [init] validate input params
def initParams(CTX:dict) -> int:

  # Shortcut Context
  Params = CTX['Params']
  
  # 200/OK 
  return 200

# [init] Get data from HTTP-Request
def initRequest(CTX:dict) -> int:

  # Shortcut Context
  req = CTX['Request']

  # Get RAW Request-Body
  body = request.get_data()   # RAW-Bytes 
  body = body.decode('utf-8') # Bytes to String

  # Update context[Request]
  req['method']  = request.method
  req['headers'] = dict(request.headers)
  req['body']    = body

  # 200/OK
  return 200


# [valid] Validate Request.Method
def validReqMethod(CTX:dict) -> int:
  
  # Shortcut
  req = CTX['Request']

  # HTTP-Methods allow to pass
  allow = ['POST']

  # Method not allow (400/BadRequest)
  if req['method'] not in allow:
    return 400

  # 200/OK
  return 200

# [valid] Validate Request.Header[Content-Type]
def validReqContentType(CTX:dict) -> int:

  # Shortcut [Request-Headers]
  headers = CTX['Request']['headers']

  # [400/Bad-Request] Missing "Content-Type"
  if 'Content-Type' not in headers:
    return 400

  # Split Content-Type data:
  # - [0] text/xml | application/xml | application/soap+xml
  # - [1] charset=utf-8
  # - [2] action="http://example.org
  CT = headers['Content-Type']
  CT = CT.split(';')

  # MIME-Type allow to pass
  allow = [
    'text/xml',             # SOAP 1.1
    'application/xml',      # SOAP ?.?
    'application/soap+xml', # SOAP 1.2
  ]

  # [400/BadRequest] Unknown MIME-Type
  if CT[0] not in allow:
    return 400

  # Update context
  CTX['SAP']['ContentType'] = CT

  # 200/OK
  return 200

# [valid] Validate Request.Header[Authorization]
def validReqAuth(CTX:dict) -> int:

  # Shortcut
  req     = CTX['Request']
  headers = req['headers']

  # [401/Unauthorized] missing "Authorization"
  if 'Authorization' not in headers:
    return 401

  # Find Auth-Base64
  code = headers['Authorization']
  code = code.removeprefix('Basic ')

  # Allow Base64
  allow = [
    'QVZBTExZX1Rlc3Q6QVZBTExZX1Rlc3Q=',
  ]

  # Unknown Authorization
  if code not in allow:
    return 401

  # Base64 decode
  auth = b64_decode(code)
  auth = auth.split(':')

  # Remember Auth Base64 code
  CTX['Auth']['code'] = code

  # Decoded Auth [user,pass]
  CTX['Auth']['user'] = auth[0]
  CTX['Auth']['pass'] = auth[1]

  # 200/OK
  return 200

# todo: validate 
# [valid] Validate Request.Header[SOAPAction]
# and may be empty ("")
def validReqSoapAction(CTX:dict) -> int:

  # Shortcut Context
  headers = CTX['Request']['headers']

  # todo: change to 400 if missing ??
  # Missing Header[SOAPAction]
  if 'SOAPAction' not in headers:
    return 200

  # Update Context
  CTX['SAP']['SoapAction'] = headers['SOAPAction']

  # 200/OK
  return 200

# todo: validate XML-Structure ?
# [valid] Validate Request.Body
def validReqBody(CTX:dict) -> int:

  # Shortcut
  req  = CTX['Request']
  body = req['body']

  # Ignore empty body
  if body == '':
    return 400

  # parse XML/SOAP
  data = xmltodict.parse(body)

  # Update Content
  CTX['SAP']['SoapPayload'] = data

  # 200/OK
  return 200





# todo: wait TaxOne-API Spec.
# [SAP] Convert S4HANA-Payload to TaxOne-API formal
def sapToTaxOne(CTX:dict) -> int:

  # todo: Convert SOAP to payload for TaxOne-API

  # 200/OK
  return 200

# todo: wait TaxOne-API Spec.
# [TaxOne] Send Converted-Payload to TaxOne-API
def taxOneSubmit(CTX:dict) -> int:

  # Prepare Request-Body (XML/SOAP)
  # Note: dummy payload XML/SOAP 
  xml = 'Resources/Soap/EmptyBody.xml'
  xml = fileLoad(xml)

  # Send HTTP-Request, Wait Response
  response = requests.post(
    url='http://localhost/api/v1/test-request.json',
    data=xml,
    # timeout=30,
    headers={
      'content-type': 'text/xml',
    },
  )

  # todo: send HTTP-Request to TaxOne-API

  # 200/OK
  return 200

# todo: wait TaxOne-API Spec.
# [TaxOne] Validate TaxOne-API response
def taxOneValidate(CTX:dict) -> int:
  return 200



# [???] HTTP-Response send Empty/Soap back to S4HANA
def responseBody(CTX:dict) -> int:

  # Shortcut
  res = CTX['Response']

  # Update Reponse-Header
  res['headers']['Content-Type'] = 'application/soap+xml'

  # Response-Body XML/Soap -- Empty soap:Body
  res['body'] = 'Resources/Soap/EmptyBody.xml'
  res['body'] = fileLoad(res['body'])

  #  [200/OK]
  return 200
