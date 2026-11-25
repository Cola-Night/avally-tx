from typing import Any
import base64
import json
import requests

# TaxOne-API eTax/Receipt handler
class eTaxReceipt:

  def __init__(self, options:dict = {}):

    # TaxOne API-Config
    self.api = {
      'host': 'test.streamtaxone.com',
      'version': 'V2.1',
      'method': 'POST',
      'url': 'https://{host}/taxone-API/{version}/etax/receipt',
      'headers': {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': '',
        'API-Key': '',
      },
    }
    
    # [Request-Body]
    self.body = {
      'header': {
        'messageID': 'Example-ID',
        'sentDTTM': '2020-08-21 10:00:00',
        'outputResponseType': 2
      },
      'etax': {
        'documentLanguage': 'EN',
        'documentRefNo': '',
        'docRefIssueDateTime': '',
        'documentRefType': '',
        'productCode': 'Test-Stream',
        'branchCode': '00000',
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
          'email': ''
        },
        'mailingAddress': {
          'shipPostcode': '',
          'shipAddressLine1': '',
          'shipAddressLine2': '',
          'shipAddressLine3': '',
          'shipCountryID': ''
        },
        'documents': [],
        'optional': {}
      },
    }

    # Send Request & Response
    self.results = None

    # Update API-Config
    self.setup(options)

  # Update properties
  def setup(self, options:dict) -> self:
    try:
      # Set API-Host
      if 'host' in options:
        self.setHost(options['host'])

      # Set API-Version
      if 'version' in options:
        self.setVersion(options['version'])

      # Set API-Key
        if 'api-key' in options:
          self.setApiKey(options['api-key'])

      # (self)
      return self
    except Exception as e:
      raise



  # [API-Config] Set Host
  def setHost(self, host:str) -> self:
    try:
      # Update API-Config
      self.api['host'] = host

      # (self)
      return self

    except Exception as e:
      raise

  # [API-Config] Set Version
  def setVersion(self, version:str) -> self:
    try:

      # Update API-Config
      self.api['version'] = version

      # (self)
      return self

    except Exception as e:
      raise

  # [API-Config] Set HTTPBasicAuth (Header.Authorization)
  def setBasicAuth(self, username:str, password:str) -> self:
    try:
      # separator character
      separator = ':'

      # Base64 username:password
      auth = [username,password]
      auth = separator.join(auth)
      auth = auth.encode('utf-8')
      auth = base64.b64encode(auth)
      auth = auth.decode('utf-8')

      # Update API-Headers
      self.api['headers']['Authorization'] = auth

      # (self)
      return self

    except Exception as e:
      raise

  # [API-Config] API-Key (JWT)
  def setApiKey(self, key:str) -> self:
    try:
      # Shortshot to request-headers
      headers = self.api['headers']

      # Set API-Key
      headers['API-Key'] = key

      # (self)
      return self
    except Exception as e:
      raise





  # [Request-Body] Bind single value to Request-Body (one-by-one)
  def bind(self, path:str|list, value:Any) -> self:
    try:
      # Convert string to list (array)
      if isinstance(path, str):
        path = path.split('.')

      # Pop last path item
      last = path.pop()

      # Cursor start point
      cursor = self.body

      # go deeper into nested var
      for key in path:
        # list-index need to by int
        if isinstance(cursor, list):
          key = int(key)

        # Update cursor
        cursor = cursor[key]
      
      # Use last-ley to set value
      cursor[last] = value

      # (self)
      return self
    except Exception as e:
      raise
    
  # [Request-Body] Bind multiple values to Request-Body (bulk)
  def mapping(self, data:dict = {}) -> self:
    try:
      # Update
      for path, value in data.items():
        self.bind(path,value)

      # (self)
      return self
    except Exception as e:
      raise




  # [Request-Body] Add new document into "etax.documents"
  def addDocument(self, data:dict = {}) -> dict:
    try:
      # Create new document (record)
      doc = {
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
        'basisAmount': 10000.0,
        'calculatedAmount': 700.0,
        'originalInformationAmount': 0.0,
        'lineTotalAmount': 10000.0,
        'differenceInformationAmount': 0.0,
        'allowanceTotalAmount': 0.0,
        'taxBasisTotalAmount': 10000.0,
        'taxTotalAmount': 700.0,
        'grandTotalAmount': 10700.0,
        'products': [],
      }

      # Use input data to update document 
      for key, value in data.items():
        if key in doc:
          doc[key] = value

      # Shortcut
      documents = self.body['etax']['documents']

      # Add document (record)
      documents.append(doc)

      # (dict) document
      return doc
    except Exception as e:
      raise

  # [Request-Body] Get document by index
  def getDocument(self, index:int) -> dict:
    try:

      # (dict) select Document (record) by index
      return self.body['etax']['documents'][index]

    except Exception as e:
      raise

  # [Request-Body] Add new Product into "etax.documents[d].products"
  def addProduct(self, doc:int|dict, data:dict = {}) -> dict:
    try:
      # Use index to find document (record)
      if isinstance(doc, int):
        doc = self.getDocument(doc)

      # Create new Product
      product = {
        'lineNO': '1',
        'itemID': '001',
        'itemName': 'Air Freight',
        'itemUnit': 'PCS',
        'calculatedRate': 7,
        'itemBilledQuantity': 1,
        'itemChargeAmount': 10000.0,
        'netLineTotalAmount': 10000.0,
        'taxTotalAmount': 700.0,
        'netIncludingTaxesLineTotalAmount': 10700.0,
        'optional': {
          'XXXDescription1': 'Refer : Ok',
          'XXXDescription2': '',
          'XXXDescription3': '',
          'XXXDescription4': ''
        },
      }

      # Update product values
      for key, value in data.items():
        if key in product:
          product[key] = value

      # Add Product
      doc['products'].append(product)
      
      # (dict)
      return product
    except Exception as e:
      raise

  # [Request-Body] Convert eTax-Receipt to JSON
  def toJSON(self, indent:int = 2) -> str:
    try:
      return json.dumps(
        self.body,
        indent=indent,
        ensure_ascii=False,
      )
    except Exception as e:
      raise
  
  # Export data for HTTP-Request
  def export(self) -> dict:
    try:
      # Replace placeholder
      url = self.api['url']
      url = url.format(**{
        'host':    self.api['host'],
        'version': self.api['version'],
      })

      # (dict)
      return {
        'url': url,
        'method': self.api['method'],
        'headers': self.api['headers'],
        'body': self.body,
      }
    except Exception as e:
      raise

  # Send HTTP-Request, wait-Response
  def send(self, options:dict = {}) -> dict:
    try:
      # (optional) Set properties before send
      self.setup(options)

      # Prepare data for HTTP-Request
      R = self.export()

      # Send Request, wait Response
      response = requests.request(
        method=R['method'],
        url=R['url'],
        headers=R['headers'],
        json=R['body'],
      )

      # Get Response-Headers
      headers = dict(response.headers)

      # Get Content-Type [0:MIME-Type, 1:charset]
      CT = headers['Content-Type']
      CT = CT.split(';')
      CT = list(map(str.strip,CT))

      # RAW Response.Body
      body = response.text

      # Response is JSON, then parse json
      if CT[0] == 'application/json':
        body = json.loads(body)

      # Convert Response to (dict)
      self.results = {
        'Request': R,
        'Response': {
          'status': response.status_code,
          'headers': headers,
          'body': body,
        },
      }

      # (dict) HTTP-Response data
      return self.results
    except Exception as e:
      raise
  