from App.Module.Utility import *
from requests.auth import HTTPBasicAuth
import requests

# Testing TaxOne-API 
# ref:
# - /documents/TaxOne-API/TAXONE JSON API SPEC V1.0.pdf
#
# HTTP-Request:
# ```
# [POST] https://test.streamtaxone.com/taxone-API/V2.1/etax/receipt
# Authorization: Basic {BASE64("USERNAME:PASSWORD")}
# Content-Type: application/json
# API-Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9......
# {
#   "header": {...},
#   "etax": {...}
# }
def main() -> None:
  try:
    # Context
    CTX = {
      'CONFIG': {
        'Host': 'test.streamtaxone.com',
        'Version': 'V2.1',
        'Username': 'AVALLY_Test',
        'Password': 'AVALLY_Test',
      },
      'Request': {
        'Method': 'POST',
        'URL': 'https://{Host}/taxone-API/{Version}/etax/receipt',
        'Headers': {
          'Content-Type': 'application/json;charset=UTF-8',
        },
        'Body': {
          'header': {},
          'etax': {},
        },
      },
      'Response': {
        'Code': 200,
        'Headers': {},
        'Body': {},
      },
    }

    # Prepare HTTP-Request
    initConfigJSON(CTX)
    initBasicAuth(CTX)
    initRequestURL(CTX)
    initRequestBody(CTX)

    # Send Request, wait Responsee
    sendRequest(CTX)
  except Exception as e:
    print(f"[ERROR] main: {e}")

# Overwrite [CONFIG] with JSON-file
def initConfigJSON(CTX:dict) -> None:
  try: 
    # Config file (.json)
    file = 'Config/ETax.json'

    # Load json-file
    data = jsonLoad(file)

    # Shortcut data in Config.json
    host      = data['Connection']['Host'] 
    username  = data['Authorization']['Basic']['Username'] 
    password  = data['Authorization']['Basic']['Password'] 
    token     = data['Authorization']['Bearer'][0]

    # Overwrite Context[CONFIG]
    CTX['CONFIG']['Host'] = host
    CTX['CONFIG']['Username'] = username
    CTX['CONFIG']['Password'] = password

    # Add Request.Header[API-Key]
    CTX['Request']['Headers']['API-Key'] = token

  except Exception as e:
    print(f"[ERROR] initConfigJSON: {e}")

# Prepare HTTPBasicAuth
def initBasicAuth(CTX:dict) -> None:
  try:
    # Find [username, password]
    username = CTX['CONFIG']['Username']
    password = CTX['CONFIG']['Password']

    # character between user,pass
    separator = ':'

    # Base64 credentials "Usernane:Password"
    credentials = [username, password]
    credentials = separator.join(credentials)
    credentials = b64_encode(credentials)

    # Header-Value
    # basic = 'Basic {credentials}'
    basic = 'Basic {credentials}'
    basic = basic.format(**{
      'credentials': credentials,
    })

    # Update Request.Headers
    CTX['Request']['Headers']['Authorization'] = basic

  except Exception as e:
    print(f"[ERROR] initBasicAuth: {e}")
    raise

# Prepare Request-URL
def initRequestURL(CTX:dict) -> None:
  try:
    # Shortcut
    Config  = CTX['CONFIG']
    Request = CTX['Request']
    
    # Replace placeholder
    url = Request['URL']
    url = url.format(**{
      'Host':     Config['Host'],
      'Version':  Config['Version'],
    })

    # Update context
    Request['URL'] = url

  except Exception as e:
    print(f"[ERROR] initRequestURL: {e}")
    raise

# Prepare Request-Body
def initRequestBody(CTX:dict) -> None:
  try:
    # Load eTax Request-Body example
    body = eTaxRequestBody()

    # Update context
    CTX['Request']['Body'] = body

  except Exception as e:
    print(f"[ERROR] initRequestBody: {e}")

# Send HTTP-Request
def sendRequest(CTX:dict) -> None:
  try:
    # Shortcut
    Request = CTX['Request']
    
    # File save location
    save_req = '.temp/TaxOne-req.json'
    save_res = '.temp/TaxOne-res.json'

    # Save Request into JSON-file
    jsonSave(save_req,Request)

    # Send Request, wait Response
    response = requests.request(
      method=Request['Method'],
      url=Request['URL'],
      headers=Request['Headers'],
      json=Request['Body'],
    )

    # Get response protocol (example: "HTTP/1.1")
    protocol = getResponseProtocol(response)

    # Summery Response
    results = {
      'Protocol': protocol,
      'StatusCode': response.status_code,
      'Headers': dict(response.headers),
      'Body': response.json(),
    }

    # Save into JSON
    jsonSave(save_res,results)

    # Feedback
    print(save_req)
    print(save_res)

  except Exception as e:
    print(f"[ERROR] sendRequest: {e}")





# [Util]
def getResponseProtocol(response) -> str:
  # Version map
  mapping = {
    10: 'HTTP/1.0',
    11: 'HTTP/1.1',
  }
  # (int) [10|11]
  version = response.raw.version
  # Lookup version-map with int (key)
  protocol = mapping.get(version,f"UNKNOWN/{version}")
  # (string)
  return protocol

# [Example]
# eTax Request-Body example
def eTaxRequestBody() -> dict:
  return {
    'header': {
      'messageID': 'STREAM01',
      'sentDTTM': '2020-08-21 10:00:00',
      'outputResponseType': 2,
    },
    'etax': {
      'documentLanguage': 'EN',
      'documentRefNo': '',
      'docRefIssueDateTime': '',
      'documentRefType': '',
      'productCode': 'IT-CLOUD-100',
      'branchCode': '00002',
      'customerProfile': {
        'cusCompanyName': 'บริษัท ทดสอบ จากัด',
        'cusTaxType': 'TXID',
        'cusTaxID': '010554409966600000',
        'cusVATBranch': '',
        'cusPostcode': '13160',
        'cusAddressLine1': 'ESTATE',
        'cusAddressLine2': 'MOO 1 BANGPA-IN',
        'cusAddressLine3': 'PHRA NAKORN SRI AYUTTHAYA',
        'cusCountryID': 'TH',
        'mobileNo': '',
        'email': '',
      },
      'mailingAddress': {
        'shipPostcode': '',
        'shipAddressLine1': '',
        'shipAddressLine2': '',
        'shipAddressLine3': '',
        'shipCountryID': '',
      },
      'documents': [
        {
          'documentNo': 'ST_IV_2101002',
          'documentType': 'TIV',
          'documentTypeCode': '388',
          'purpose': '',
          'purposeCode': '',
          'issueDateTime': '2020-06-30 00:00:00',
          'creationDateTime': '2020-06-30 00:00:00',
          'currency': 'THB',
          'taxCode': 'VAT',
          'dcnTaxInvoice': True,
          'calculatedRate': 7,
          'basisAmount': 10000.00,
          'calculatedAmount': 700.00,
          'originalInformationAmount': 0.00,
          'lineTotalAmount': 10000.00,
          'differenceInformationAmount': 0.00,
          'allowanceTotalAmount': 0.0,
          'taxBasisTotalAmount': 10000.00,
          'taxTotalAmount': 700.00,
          'grandTotalAmount': 10700.00,
          'products': [
            {
              'lineNO': '1',
              'itemID': '001',
              'itemName': 'Item 1',
              'itemUnit': 'PCS',
              'calculatedRate': 7,
              'itemBilledQuantity': 1,
              'itemChargeAmount': 10000.00,
              'netLineTotalAmount': 10000.00,
              'taxTotalAmount': 700.00,
              'netIncludingTaxesLineTotalAmount': 10700.00,
              'optional': {
                'XXXDescription1': 'Refer : Ok',
                'XXXDescription2': '',
                'XXXDescription3': '',
                'XXXDescription4': '',
              },
            },
          ],
        },
      ],
      'optional': {},
    },
  }
