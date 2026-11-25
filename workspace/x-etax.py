from App.Module.Utility import *
from App.Module.eTaxReceipt import eTaxReceipt
from App.Module.CollapseMap import CollapseMap
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import time
import os

# Testing convert S4HANA.XML/Soap to TaxOne.JSON
def main() -> None:
  try:
    # Context
    CTX = {
      'xMap': None,
      'Receipt': None,
    }

    # Testing modules
    testCollapseMap(CTX)
    testReceipt(CTX)
    
  except Exception as e:
    print(f"[ERROR] main: {e}")

# Convert Nested-XML to 2D-Map
def testCollapseMap(CTX:dict):
  try:
    # Target XML file
    file = os.path.join(
      'Storage/S4HANA/TaxInvoice',
      'TaxInvoice-0090001098/n0-SendTaxInvoiceRequest.xml',
    )

    # Load XML as 2D-Map
    cMap = CollapseMap()
    cMap.loadXML(file,'n0:SendTaxInvoiceRequest/Body')

    # Split 2D-Map groups by prefix
    cMap.grouping('n2:ExchangedDocument/')
    cMap.grouping('n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeAgreement/n3:SellerTradeParty')
    cMap.grouping('n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeAgreement/n3:BuyerTradeParty')
    cMap.grouping('n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeDelivery/n3:ShipToTradeParty')
    cMap.grouping('n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeSettlement/n3:ApplicableTradeTax')
    cMap.grouping('n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeSettlement/n3:SpecifiedTradeAllowanceCharge')
    cMap.grouping('n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeSettlement/n3:SpecifiedTradeSettlementHeaderMonetarySummation')
    cMap.grouping('n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeSettlement/n3:InvoiceeTradeParty')
    cMap.grouping('n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeSettlement/n3:PayerTradeParty')
    cMap.grouping('n2:SupplyChainTradeTransaction/n3:IncludedSupplyChainTradeLineItem')

    # Update context
    CTX['XML'] = cMap

    # Debug-Prefix / Save JSON files
    if True:
      cMap.save('.temp/x-etax-flat.json')
      cMap.saveGroups('.temp/x-etax-group.json')

    # Update context
    CTX['cMap'] = cMap

  except Exception as e:
    print(f"[ERROR] main: {e}")

# Prepare TaxOne/eTax-Receipt
def testReceipt(CTX:dict):
  try:
    # Context
    cMap = CTX['XML']

    # Load API-Config
    config = jsonLoad('Config/ETax.json')
    
    # TaxOne/eTax-Receipt
    receipt = eTaxReceipt({
      'host':     config['Connection']['Host'],
      'version':  config['Connection']['Version'],
      'api-key':  config['API-Key'][0],
    })

    # Update context
    CTX['Receipt'] = receipt

    # Set BasicAuth[username,password]
    if True:
      receipt.setBasicAuth(
        username=config['BasicAuth']['Username'],
        password=config['BasicAuth']['Password'],
      )

    # Create new document (index=0,1)
    D0 = receipt.addDocument({})
    D1 = receipt.addDocument({})
    
    # Add Product (etax.documents.0.products.0)
    D0P0 = receipt.addProduct(D0,{})
    
    # Add Product (etax.documents.0.products.1)
    D0P1 = receipt.addProduct(D0,{
      'lineNO': '2',
      'itemID': '002',
      'itemBilledQuantity': 2,
      'itemChargeAmount': 10000.22,
      'netLineTotalAmount': 10000.22,
      'taxTotalAmount': 700.2,
      'netIncludingTaxesLineTotalAmount': 10700.2,
    })

    # Extract data from XML
    if cMap.groupExists('n2:ExchangedDocument'):

      # Get XML-data by GroupName
      V = cMap.getGroup('n2:ExchangedDocument')

      # Bind value one-by-one
      receipt.bind('header.messageID',V['n3:ID'])
      receipt.bind('header.sentDTTM','2026-11-25 23:59:59')
      receipt.bind('etax.documentLanguage',V['n3:Name/@languageID'])

    # Bind multiple values
    if True:
      receipt.mapping({
        'etax.documentRefNo': '',
        'etax.docRefIssueDateTime': '',
        'etax.documentRefType': '',
        'etax.customerProfile.cusVATBranch': '',
        'etax.customerProfile.mobileNo': '0123456789',
        'etax.customerProfile.email': 'test@mail.com',
        'etax.mailingAddress.shipPostcode': '22222',
        'etax.mailingAddress.shipAddressLine1': 'Line1',
        'etax.mailingAddress.shipAddressLine2': 'Line2',
        'etax.mailingAddress.shipAddressLine3': 'Line3',
        'etax.mailingAddress.shipCountryID': 'TH',
        'etax.optional.Description1': 'Desc1',
      })

    # Test update Document[0]
    if True:
      receipt.mapping({
        'etax.documents.0.purpose': '',
        'etax.documents.0.purposeCode': '',
        'etax.documents.0.dcnTaxInvoice': True,
      })

    # Export HTTP-Request data
    data = receipt.export()

    # JSON-save, API-Body preview
    save = '.temp/x-etax.json'
    if mkDirname(save) == True:
      jsonSave(save,data)

    # Send API-Request, Wait Response
    response = receipt.send()
    
    # JSON-save, API-Body preview
    save = '.temp/x-etax-send.json'
    if mkDirname(save) == True:
      jsonSave(save,response)

  except Exception as e:
    print(f"[ERROR] main: {e}")

# Start main function
if __name__ == "__main__":
  main()