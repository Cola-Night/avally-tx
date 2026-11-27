from App.Module.Utility import *
from App.Module.EnvelopeParser import EnvelopeParser
from App.Module.StructureAnalyzer import StructureAnalyzer
from App.Module.eTaxReceipt import eTaxReceipt
import pandas as pd
import fnmatch
import sys
import os

# Testing convert S4HANA/XML to TaxOne-API/JSON
def main() -> None:
  try:

    CTX = {
      'Path': {
        'CDN':        'Storage/CDN',
        'S4':         'Storage/S4HANA',
        'Receipt':    '{S4}/Receipt',
        'TaxInvoice': '{S4}/TaxInvoice',
      },
      'StructureAnalyzer': {
        # S4HANA download XML
        'S4Hana/SendReceiptRequest': {
          'n0:SendReceiptRequest': [
            'key=Body',
            'key=transactionID',
          ],
          'n0:SendReceiptRequest/Body': [
            'key=n2:ExchangedDocumentContext',
            'key=n2:ExchangedDocument',
            'key=n2:SupplyChainTradeTransaction',
          ],
          'n0:SendReceiptRequest/Body/n2:ExchangedDocumentContext': [
            'key=n3:GuidelineSpecifiedDocumentContextParameter'
          ],
          'n0:SendReceiptRequest/Body/n2:ExchangedDocument': [
            'key=n3:ID',
            'key=n3:Name',
            'key=n3:TypeCode',
            'key=n3:IssueDateTime',
            'key=n3:GlobalID',
            'key=n3:CreationDateTime',
          ],
          'n0:SendReceiptRequest/Body/n2:SupplyChainTradeTransaction': [
            'key=n3:ApplicableHeaderTradeAgreement',
            'key=n3:ApplicableHeaderTradeDelivery',
            'key=n3:ApplicableHeaderTradeSettlement',
            'key=n3:IncludedSupplyChainTradeLineItem',
          ],
        },
        'S4Hana/SendTaxInvoiceRequest': {
          'n0:SendTaxInvoiceRequest': [
            'key=Body',
            'key=transactionID',
          ],
        },

        # Testing XML same Root-TagName, different children
        'Test/ExperimentReceipt/T1': {
          'x1:ExperimentReceipt': [
            'key=header',  
            'key=etax',  
          ],
          'x1:ExperimentReceipt/header': [
            'key=messageID',
            'key=sentDTTM',
            'key=outputResponseType',
          ],
          'x1:ExperimentReceipt/etax': [
            'key=documentLanguage',
            'key=documentRefNo',
          ],
        },
        'Test/ExperimentReceipt/T2': {
          'x1:ExperimentReceipt': [
            'key=Header',
            'key=Records',
          ],
          'x1:ExperimentReceipt/Records/record/?': [
            'key=code',
            'key=name',
          ],
        },

        # Testing
        'Test/ExperimentTaxInvoice/T1': {
          'x1:ExperimentTaxInvoice': [
            'key=Collection',
          ],
        },
        'Test/ExperimentTaxInvoice/T2': {
          'x1:ExperimentTaxInvoice': [
            'key=Records',
          ],
          'x1:ExperimentTaxInvoice/Records/record/?': [
            'key=code',
            'key=name',
          ],
        },
      },
      'eDocuments': {
        'S4/Receipt': {
          'source': '{Receipt}/R-14000000002026/n0-SendReceiptRequest.xml',
        },
        'S4/TaxInvoice': {
          'source': '{TaxInvoice}/TaxInvoice-0090001097/n0-SendTaxInvoiceRequest.xml',
        },
        'ExperimentReceipt-01': {
          'source': '{CDN}/xml/ExperimentReceipt-01.xml',
        },
        'ExperimentReceipt-02': {
          'source': '{CDN}/xml/ExperimentReceipt-02.xml',
        },
        'ExperimentTaxInvoice-01': {
          'source': '{CDN}/xml/ExperimentTaxInvoice-01.xml',
        },
        'ExperimentTaxInvoice-02': {
          'source': '{CDN}/xml/ExperimentTaxInvoice-02.xml',
        },
      },
    }

    # [init]
    initPath(CTX)
    initAnalyzer(CTX)
    initEnvelope(CTX)

    # [Test-Converter]
    convertToTaxOneJSON(CTX)
    

  except Exception as e:
    print(f"[ERROR] main: {e}")

# [init] Replace placeholder
def initPath(CTX:dict) -> None:
  try:
    # Shortcut
    collection = CTX['Path']

    # Replace placeholder
    for name, path in collection.items():
      collection[name] = path.format(**collection)

    # Update context
    CTX['Path'] = collection

  except Exception as e:
    raise

# [init] Prepare StructureAnalyzer
def initAnalyzer(CTX:dict) -> None:
  try:
    # Context
    collection = CTX['StructureAnalyzer']
    analyzer   = StructureAnalyzer()
    
    # Register [Structure-Name, Structure-Conditions]
    for name, conditions in collection.items():
      analyzer.define(name,conditions)

    # Update context
    CTX['StructureAnalyzer'] = analyzer

  except Exception as e:
    raise

# [init] Load XML/Soap (unwrap <soap:Envelope>)
def initEnvelope(CTX:dict) -> None:
  try:
    # Shortcut context
    documents = CTX['eDocuments']
    analyzer  = CTX['StructureAnalyzer']

    # Load XML-Files to EnvelopeParser
    for name, data in documents.items():

      # Update file place-holder
      file = data['source']
      file = file.format(**CTX['Path'])

      # Load XML-file into Parser
      envelope = EnvelopeParser({
        'file': file,
      })

      # Get Structure-Name by analyze XML-Structure
      structure = analyzer.scan(envelope.body)

      # Overwrite context
      documents[name] = {
        'structure': structure,
        'envelope':  envelope,
      }

  except Exception as e:
    raise

# Convert XML to eTax/JSON
def convertToTaxOneJSON(CTX:dict) -> None:
  try:

    # Context
    documents = CTX['eDocuments']

    # Mapping [XML-Structure => callback]
    mapping = {
      'S4Hana/SendReceiptRequest':    toTaxOneReceiptV0,
      'S4Hana/SendTaxInvoiceRequest': toTaxOneTaxInvoiceV0,
      'Test/ExperimentReceipt/T1':    toTaxOneReceiptT1,
      'Test/ExperimentReceipt/T2':    toTaxOneReceiptT2,
      'Test/ExperimentTaxInvoice/T1': toTaxOneTaxInvoiceT1,
      'Test/ExperimentTaxInvoice/T2': toTaxOneTaxInvoiceT2,
    }

    # Convert Envelope.Body to TaxOne-JSON
    for name, doc in documents.items():

      # Skip unknown XML-Structure
      if doc['structure'] == 'UNKNOWN':
        print(f"Unknown XML: {name}")
        continue

      # Get callback by XML-Structure name
      callback = doc['structure']
      callback = mapping[callback]
      
      # EnvelopeParser
      envelope = doc['envelope']

      # Convert XML-data to TaxOne-JSON
      body = callback(envelope)

      # filename
      filename = name.replace('/','-')

      # JSON-file save location
      save = '.temp/xml2json/{name}.json'
      save = save.format(**{
        'name': filename,
      })

      # Create dir + save file
      if mkDirname(save) == True:
        jsonSave(save,body)
        print(save)

  except Exception as e:
    raise






# [Custom-XML-Mapping]
def toTaxOneReceiptV0(envelope:EnvelopeParser) -> dict:

  # eTax mapping
  etax = eTaxReceipt()
  D0 = etax.addDocument({})
  D0P0 = etax.addProduct(D0,{})

  # Convert XML to JSON
  body = etax.export()
  body = body['body']

  # (dict)
  return body

# [Custom-XML-Mapping]
def toTaxOneTaxInvoiceV0(envelope:EnvelopeParser) -> dict:
  return {'NOTE':'toTaxOneTaxInvoiceV0'}

# [Custom-XML-Mapping]
def toTaxOneReceiptT1(envelope:EnvelopeParser) -> dict:

  # XML-Data
  x = {
    'header': 'x1:ExperimentReceipt/header',
    'etax':   'x1:ExperimentReceipt/etax',
  }

  # Get XML-Data
  for key, query in x.items():
    x[key] = envelope.pointer(envelope.body,query)

  # XML-Shortcut
  h = x['header']
  e = x['etax']
  c = e['customerProfile']
  m = e['mailingAddress']

  # eTax mapping
  etax = eTaxReceipt()

  # Add Document[], Product[]
  D0 = etax.addDocument({})
  D0P0 = etax.addProduct(D0,{})

  # Mapping <header>
  etax.mapping({
    'header.messageID':           h['messageID'],
    'header.sentDTTM':            h['sentDTTM'],
    'header.outputResponseType':  h['outputResponseType'],
  })

  # Mapping <etax>
  etax.mapping({
    'etax.documentLanguage':    e['documentLanguage'],
    'etax.documentRefNo':       e['documentRefNo'],
    'etax.docRefIssueDateTime': e['docRefIssueDateTime'],
    'etax.documentRefType':     e['documentRefType'],
    'etax.productCode':         e['productCode'],
    'etax.branchCode':          e['branchCode'],
  })

  # Mapping <etax.customerProfile>
  etax.mapping({
    'etax.customerProfile.cusCompanyName':  c['cusCompanyName'],
    'etax.customerProfile.cusTaxType':      c['cusTaxType'],
    'etax.customerProfile.cusTaxID':        c['cusTaxID'],
    'etax.customerProfile.cusVATBranch':    c['cusVATBranch'],
    'etax.customerProfile.cusPostcode':     c['cusPostcode'],
    'etax.customerProfile.cusAddressLine1': c['cusAddressLine1'],
    'etax.customerProfile.cusAddressLine2': c['cusAddressLine2'],
    'etax.customerProfile.cusAddressLine3': c['cusAddressLine3'],
    'etax.customerProfile.cusCountryID':    c['cusCountryID'],
    'etax.customerProfile.mobileNo':        c['mobileNo'],
    'etax.customerProfile.email':           c['email'],
  })

  # Mapping <etax.mailingAddress>
  etax.mapping({
    'etax.mailingAddress.shipPostcode':     m['shipPostcode'],
    'etax.mailingAddress.shipAddressLine1': m['shipAddressLine1'],
    'etax.mailingAddress.shipAddressLine2': m['shipAddressLine2'],
    'etax.mailingAddress.shipAddressLine3': m['shipAddressLine3'],
    'etax.mailingAddress.shipCountryID':    m['shipCountryID'],
  })

  # Convert XML to JSON
  body = etax.export()
  body = body['body']

  return body

# [Custom-XML-Mapping]
def toTaxOneReceiptT2(envelope:EnvelopeParser) -> dict:
  return {'NOTE':'toTaxOneReceiptT2'}

# [Custom-XML-Mapping]
def toTaxOneTaxInvoiceT1(envelope:EnvelopeParser) -> dict:
  return {'NOTE':'toTaxOneTaxInvoiceT1'}

# [Custom-XML-Mapping]
def toTaxOneTaxInvoiceT2(envelope:EnvelopeParser) -> dict:
  return {'NOTE':'toTaxOneTaxInvoiceT2'}

# Start main function
if __name__ == "__main__":
  main()
