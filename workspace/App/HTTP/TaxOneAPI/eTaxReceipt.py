from App.Module.Utility import *
from App.Model.S4TX import S4TX
from flask import request
from typing import Any
import xmltodict
import requests
import uuid
import os

# [module]: App.HTTP.TaxOneAPI.eTaxReceipt@main
# [url]: /taxone-API/V2.1/etax/receipt

# Trigger
# S4HANA CommunicationArrangement, Outbound:
# - eDocument Thailand: Send Tax Invoice
# - eDocument Thailand: Send Debit/Credit Note
# - eDocument Thailand: Send Receipt
# - eDocument Thailand: Get Status

# Process-Steps:
# 1. Validate HTTP-Request from S4hana
# 2. Convert S4hana XML/Soap to API-Body/JSON
# 3. Send API-Body/JSON to TaxOne-API
# 4. Validate Response from TaxOne-API
# 5. Convert TaxOne-API Response/JSON to XML/Soap (for S4hana)
# 6. Send XML/Soap back to S4hana

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
    'S4': {
      'ContentType': [],
      'SoapAction': {},
      'SoapPayload': {},
    },
    'TaxOne': {
      'Version': 'V2.1',
      'Host': 'test.streamtaxone.com',
      'Endpoint': 'https://{Host}/taxone-API/{Version}/etax/receipt',
      'Payload': {},
    },
  }

  # Stop proccessing when Response.status NOT 200
  response = proccessing(CTX,[
    # Prepare Context data
    initParams,   # 200|500 Custom-Config with CTX.Params
    initRequest,  # 200|500 Flask.Request => update Context

    # 1. Validate HTTP-Request from S4hana
    validReqMethod,       # 200|400 Validate Request.Method
    validReqContentType,  # 200|40X Validate Request.Header[Content-Type]
    validReqAuth,         # 200|40X Validate Request.Header[Authorization]
    validReqSoapAction,   # 200|40X Validate Request.Header[SOAPAction]
    validReqBody,         # 200|40X Validate Request.Body

    # 2. Convert S4hana XML/Soap to API-Body/JSON
    sapToTaxOne, # 200|500 Build API-Body/JSON for TaxOneAPI

    # 3. Send API-Body/JSON to TaxOne-API
    taxOneSubmit, # 200|??? send Payload to TaxOneAPI

    # 4. Validate Response from TaxOne-API
    validTaxOne, # 200|??? Validate TaxOneAPI.response

    # 5. Convert TaxOne-API Response/JSON to XML/Soap (for S4hana)
    responseBuild,  # 200|???

    # 6. Send XML/Soap back to S4hana
    responseSubmit, # 200|???
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

# [init] Allow HTTP-Controller to set custom config/params
def initParams(CTX:dict) -> int:

  # Shortcut Context
  Params = CTX['Params']

  # 200/OK 
  return 200

# [init] Update CTX.Request with Falsk.request
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
  
  # Context Shortcut
  req = CTX['Request']

  # List valid HTTP-Methods
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

  # List valid MIME-Type's
  allow = [
    'text/xml',             # SOAP 1.1
    'application/xml',      # SOAP ?.?
    'application/soap+xml', # SOAP 1.2
  ]

  # [400/BadRequest] Unknown MIME-Type
  if CT[0] not in allow:
    return 400

  # Update context
  CTX['S4']['ContentType'] = CT

  # 200/OK
  return 200

# [valid] Validate Request.Header[Authorization]
def validReqAuth(CTX:dict) -> int:

  # Context Shortcut
  req     = CTX['Request']
  headers = req['headers']

  # [401/Unauthorized] required Header[Authorization]
  if 'Authorization' not in headers:
    return 401

  # [401/Unauthorized] Header[Authorization] empty
  if len(headers['Authorization']) < 1:
    return 401

  # 200/OK
  return 200

# [valid] Validate Request.Header[SOAPAction] and may be empty ("")
def validReqSoapAction(CTX:dict) -> int:

  # Shortcut Context
  headers = CTX['Request']['headers']

  # [200] when Header[SOAPAction] missing
  if 'SOAPAction' not in headers:
    return 200

  # Update Context
  CTX['S4']['SoapAction'] = headers['SOAPAction']

  # 200/OK
  return 200

# [valid] Validate Request.Body (XML)
def validReqBody(CTX:dict) -> int:

  # Shortcut
  req  = CTX['Request']
  body = req['body']

  # [Error-400] body empty
  if body == '':
    return 400

  # Convert XML to dict
  data = xmltodict.parse(body)

  # Update Content
  CTX['S4']['SoapPayload'] = data

  # 200/OK
  return 200




# [S4 (S4HANA)]
# Convert Payload from S4HANA (CTX.S4.SoapPayload)
# to TaxOne-API accept format (XML/SOAP?)
def sapToTaxOne(CTX:dict) -> int:

  # Find S4hana.XML
  xml = CTX['S4']['SoapPayload']

  # Convert XML to TaxOne.JSON
  body = S4TX.convert(xml)

  # Update context
  CTX['TaxOne']['Paylod'] = body

  # 200/OK
  return 200

# [TaxOne] Send Converted-Payload to TaxOne-API
def taxOneSubmit(CTX:dict) -> int:

  # Prepare Request-Body (XML/SOAP)
  # Note: dummy payload XML/SOAP 
  xml = 'Resources/Soap/EmptyBody.xml'
  xml = fileLoad(xml)

  # todo: send HTTP-Request to TaxOne-API
  # Send HTTP-Request, Wait Response
  if False:
    response = requests.post(
      url='http://localhost/api/v1/test-request.json',
      data=xml,
      headers={
        'content-type': 'text/xml',
      },
    )


  # 200/OK
  return 200

# todo: wait TaxOne-API Spec.
# [TaxOne] Validate TaxOne-API response
def validTaxOne(CTX:dict) -> int:
  return 200

# Use TaxOne-API data to build Response
def responseBuild(CTX:dict) -> int:
  return 200

# [???] HTTP-Response send Empty/Soap back to S4HANA
def responseSubmit(CTX:dict) -> int:

  # Shortcut
  res = CTX['Response']

  # Update Reponse-Header
  res['headers']['Content-Type'] = 'application/soap+xml'

  # Response-Body XML/Soap -- Empty soap:Body
  res['body'] = 'Resources/Soap/EmptyBody.xml'
  res['body'] = fileLoad(res['body'])

  # DEBUG
  res['body'] = CTX['TaxOne']['Paylod']

  #  [200/OK]
  return 200
