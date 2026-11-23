from App.Module.Utility import *
import pandas as pd
import xmltodict

# [Testing]
# Encode S4HANA XML to JSON-Body
# For API "streamtaxone.com/taxone-API/V2.1/etax/receipt"

def main() -> None:
  try:
    # Context
    CTX = {
      'S4HANA': {
        'File': 'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001097/n0-SendTaxInvoiceRequest.xml',
        'Map2D': {},
      },
      'TaxOne': {
        'Template': 'Storage/TaxOne/API-Body-Template.json',
        'Body': {
          'header': {},
          'etax': {},
        },
      },
      'Mapping': {
        'Root': {},
      },
    }

    # Processing
    loadXml2Map2D(CTX)
    loadBodyTemplate(CTX)
    transferValues(CTX)

    # Preview JSON
    pp(CTX['TaxOne'])
  except Exception as e:
    print(f"[ERROR] main: {e}")


# Load S4HANA-XML and convert to 2D-Map dict(Key=Value)
def loadXml2Map2D(CTX:dict) -> None:
  try:
    print('loadXml2Map2D')

    # Find XML file
    file = CTX['S4HANA']['File']

    # Load XML + convert to 2D-Map 
    data = fileLoad(file)
    data = xmltodict.parse(data)
    data = pd.json_normalize(data, sep='/')
    data = data.to_dict(orient='records')[0]
    data = simplifyFlatMap(data)

    # Update context
    CTX['S4HANA']['Map2D'] = data

    # Temp save location
    save = '.temp/TaxOneMap.json'

    # Save 2D-Map JSON
    if mkDirname(save) == True:
      jsonSave(save,data)

  except Exception as e:
    raise

# Load JSON-Body template for TaxOne-API
def loadBodyTemplate(CTX:dict) -> None:
  try:
    
    # Find API-Body template json file
    source = CTX['TaxOne']['Template']

    # Load JSON from file
    CTX['TaxOne']['Body'] = jsonLoad(source)

  except Exception as e:
    raise

# Transfer 2D-Map(XML) values to JSON-Body
def transferValues(CTX:dict) -> None:
  try:
    # Map2D, Template
    data = CTX['S4HANA']['Map2D']
    body = CTX['TaxOne']['Body']

  except Exception as e:
    raise





# Filter
def simplifyFlatMap(data:dict) -> dict:
  try:
    # default output
    output = {}

    # Remove Wrapper-Node
    prefix = 'n0:SendTaxInvoiceRequest/Body/'

    # Loop FlatXML by key-value
    for key, value in data.items():

      # Skip Flat-Key outside of <n0:SendTaxInvoiceRequest>
      if key.startswith(prefix) == False:
        continue

      # Filter prefix
      key = key.removeprefix(prefix)

      # Update output
      output[key] = value

    # (dict)
    return output
  except Exception as e:
    raise