from App.Module.Utility import *
import pandas as pd
import xmltodict

# TaxInvoice-XML Analyzer
# 1. Convert TaxInvoice-XML to 2D-Map
# 2. Counting 2D-Path/Value (required tag, static value) 
def main() -> None:
  try:
    # Context
    CTX = {
      'TaxInvoice': { # name => filepath
        'TX-0090001097': 'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001097/n0-SendTaxInvoiceRequest.xml',
        'TX-0090001098': 'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001098/n0-SendTaxInvoiceRequest.xml',
        'TX-0090001099': 'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001099/n0-SendTaxInvoiceRequest.xml',
        'TX-0090001100': 'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001100/n0-SendTaxInvoiceRequest.xml',
        'TX-0090001102': 'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001102/n0-SendTaxInvoiceRequest.xml',
        'TX-0090001103': 'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001103/n0-SendTaxInvoiceRequest.xml',
        'TX-0090001105': 'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001105/n0-SendTaxInvoiceRequest.xml',
        'TX-0090001106': 'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001106/n0-SendTaxInvoiceRequest.xml',
      },
      'Path': {
        'SaveFlatJSON': '.temp/TaxInvoice/{name}.json',
        'SaveAnalysis': '.temp/TaxInvoice/#Analysis.json',
      },
      'Analysis': {},
    }

    # init
    processTaxInvoice(CTX)
    saveAnalysis(CTX)

  except Exception as e:
    print(f"[ERROR] TaxInvoice.main: {e}")

# [main] Read each TaxInvoice.xml, counting [path,value]
def processTaxInvoice(CTX:dict) -> None:
  try:
    # Loop each .xml files
    for name, path in CTX['TaxInvoice'].items():

      # Check file exists
      if isFile(path) == False:
        raise ValueError(f"file not exists `{path}`")

      # Processing XML
      data = fileLoad(path)
      data = xmltodict.parse(data)
      data = pd.json_normalize(data, sep='/')
      data = data.to_dict(orient='records')[0]
      data = simplifyFlatMap(data)

      # Use FlatMap to update CTX.Analysis
      updateAnalysis(CTX,name,data)

      # JSON save location
      save = CTX['Path']['SaveFlatJSON']
      save = save.format(**{
        'name': name,
      })

      # Save JSON-file (+ create missing dirs)
      if mkDirname(save) == True:
        jsonSave(save,data)
  except Exception as e:
    raise

# [main] Save CTX.Analysis into JSON-File
def saveAnalysis(CTX:dict) -> None:
  try:
    # Analysis save location
    save = CTX['Path']['SaveAnalysis']

    # Save JSON-file (+ create missing dirs)
    if mkDirname(save) == True:
      jsonSave(save,CTX['Analysis'])
  except Exception as e:
    raise





# Filter
def simplifyFlatMap(data:dict) -> dict:
  try:
    # default output
    prefix = 'n0:SendTaxInvoiceRequest/Body/'
    output = {}

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

# Update CTX.Analysis
def updateAnalysis(CTX:dict, name:str, data:dict) -> None:
  try:
    
    # Shortcut
    A = CTX['Analysis']

    # Update CTX.Analysis
    for key, value in data.items():

      # Value to string
      value = str(value)

      # New XML-Path detected
      if key not in A:
        A[key] = {
          'count': 0,
          'values': {},
        }

      # Update XML-Path count
      A[key]['count'] = (A[key]['count']+1)

      # Update value count
      if value not in A[key]['values']:
        A[key]['values'][value] = []

      # Update
      A[key]['values'][value].append(name)



  except Exception as e:
    raise





# Load S4HANA-eDoc XML from "Storage/S4HANA/TaxInvoice/*"
def initTaxInvoiceXML(CTX:dict) -> None:
  try:
    # Loop each eDoc "n0-SendTaxInvoiceRequest.xml"
    for name in CTX['TaxInvoice']:

      # Replace placeholder
      path = CTX['Path']['TaxInvoice']
      path = path.format(**{
        'name': name,
      })

      # Load XML from file
      xml = fileLoad(path)
      
      # Parse XML to dict
      data = xmltodict.parse(xml)

      # Convert nested dict to 2D-dict (panda)
      d_json = pd.json_normalize(data, sep='/')
      d_flat = d_json.to_dict(orient='records')[0]

      # Update context
      CTX['XML'][name] = d_flat

      # JSON save location
      save = '.temp/TaxInvoice/{name}.json'
      save = save.format(**{
        'name': name,
      })

      # Create missing dirs and save JSON-file
      if mkDirname(save) == True:
        jsonSave(save,d_flat)
  except Exception as e:
    raise

# Scan 
def countNodes(CTX:dict) -> None:
  try:
    # Loop each eDoc "n0-SendTaxInvoiceRequest.xml"
    for name in CTX['TaxInvoice']:
      print(name)

  except Exception as e:
    raise
