from App.Module.Utility import *
from App.Module.eTaxReceipt import eTaxReceipt
from App.Module.CollapseMap import CollapseMap
from flask import request
from typing import Any
import requests
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
# 1. Prepare Context data
# 2. Validate HTTP-Request from S4hana
# 3. Build API-Body/JSON -- S4hana XML/Soap to API-Body/JSON
# 4. Convert TaxOne-API Response to XML/Soap (for S4hana)

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
      'cMap': None,
    },
    'TaxOne': {
      'Endpoint': 'https://{Host}/taxone-API/{Version}/etax/receipt',
      'Receipt': None,
    },
  }

  # Stop proccessing when Response.status NOT 200
  response = proccessing(CTX,[
    # 1. Prepare Context data
    initParams,       # 200|500 Custom-Config with CTX.Params
    initRequest,      # 200|500 Flask.Request => update Context
    initCollapseMap,  # 200|500 Prepare XML/Soap handler
    initETaxReceipt,  # 200|500 Prepare TaxOne Receipt-API handler

    # 2. Validate HTTP-Request from S4hana
    validReqMethod,       # 200|400 Validate Request.Method
    validReqContentType,  # 200|40X Validate Request.Header[Content-Type]
    # validReqAuth,         # 200|40X Validate Request.Header[Authorization]
    validReqSoapAction,   # 200|40X Validate Request.Header[SOAPAction]
    validReqBody,         # 200|40X Validate Request.Body

    # 3. Build API-Body/JSON -- S4hana XML/Soap to API-Body/JSON
    taxOneBuild,    # 200|500 Build API-Body/JSON for TaxOneAPI
    taxOneSubmit,   # 200|??? send Payload to TaxOne-API
    taxOneResponse, # 200|??? Validate Response from TaxOneAPI

    # 4. Convert TaxOne-API Response to XML/Soap (for S4hana)
    s4Build,    # 200|??? Build Soap/XML Response
    s4Response, # 200|??? Send HTTP-Response back to S4Hana
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

# [init] Extract data from Falsk.request and update CTX.Request 
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

# [init] Prepare CollapseMap for handling nested XML/Soap
def initCollapseMap(CTX:dict) -> int:

  # Prepare CollapseMap for handling
  # Nested XML/Soap
  cMap = CollapseMap()

  # Update context
  CTX['S4']['cMap'] = cMap

  # (200/OK)
  return 200 

# [init] Prepare TaxOne-API XML-handler
def initETaxReceipt(CTX:dict) -> int:

  # Prepre eTaxReceipt
  receipt = eTaxReceipt()

  # Update context
  CTX['TaxOne']['Receipt'] = receipt

  # (200/OK)
  return 200 




# [valid] Validate Request.Method
def validReqMethod(CTX:dict) -> int:
  
  # Context Shortcut
  req = CTX['Request']

  # List valid HTTP-Methods
  allow = ['POST']

  # (400/BadRequest) Method not allow
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

  # [200] when Header[SOAPAction] empty
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
  cMap = CTX['S4']['cMap']

  # Load Request-Body XML to cMap
  cMap.importXML(body)
  
  # 200/OK
  return 200




# [TaxOne-API)]
# Convert Payload from S4HANA.XML to Request-Body.JSON
def taxOneBuild(CTX:dict) -> int:

  xml     = CTX['Request']['body']
  cMap    = CTX['S4']['cMap']
  receipt = CTX['TaxOne']['Receipt']

  # Load Request-Body XML
  cMap.importXML(xml)



  # 200/OK
  return 200

# [TaxOne] Send Converted-Payload to TaxOne-API
def taxOneSubmit(CTX:dict) -> int:

  # eTax/Receipt
  receipt = CTX['TaxOne']['Receipt']
  response = receipt.send()

  # 200/OK
  return 200

# [TaxOne] Validate TaxOne-API response
def taxOneResponse(CTX:dict) -> int:
  return 200




# Use TaxOne-API data to build Response
def s4Build(CTX:dict) -> int:
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
