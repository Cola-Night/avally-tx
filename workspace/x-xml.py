from typing import Any
from collections.abc import Callable
from App.Module.Utility import *
from App.Module.EnvelopeParser import EnvelopeParser
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import sys
import os

# Testing XML/Soap parser with EnvelopeParser
# Detect Structure/Type
def main() -> None:
  try:
    # Context
    CTX = {
      'Status': 'OK',
      'Collection': [
        # Test <soap:Envelope>
        'Storage/CDN/soap/cxf-th-sendinvoice-00.soap.xml',
        'Storage/CDN/soap/cxf-th-sendinvoice-01.soap.xml',
        'Storage/CDN/soap/soap-01.xml',
        'Storage/CDN/soap/soap-02.xml',
        'Storage/CDN/soap/soap-03.xml',
        
        # Test xml from S4HANA/eDocument
        'Storage/S4HANA/Receipt/R-14000000002026/n0-SendReceiptRequest.xml',
        'Storage/S4HANA/Receipt/R-14000000092026/n0-SendReceiptRequest.xml',
        'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001097/n0-SendTaxInvoiceRequest.xml',
        'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001098/n0-SendTaxInvoiceRequest.xml',
        'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001099/n0-SendTaxInvoiceRequest.xml',
        'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001100/n0-SendTaxInvoiceRequest.xml',

        # Test XML-Name same name but different structure
        'Storage/CDN/xml/TestSameRootName-01.xml',
        'Storage/CDN/xml/TestSameRootName-02.xml',
      ],
      'Structure': {
        'th:TaxInvoiceSendRequest': [
          {
            'validator': isTaxInvoiceSendRequest,
            'root': 'th:TaxInvoiceSendRequest',
            'body': {
              'DocumentHeader':  'th:TaxInvoiceSendRequest/th:DocumentHeader',
              'TaxRegistration': 'th:TaxInvoiceSendRequest/th:TaxRegistration',
              'InvoiceContent':  'th:TaxInvoiceSendRequest/th:InvoiceContent',
            },
          },
        ],
        'OrderItems': [
          {
            'validator': isOrderItems,
            'root': 'OrderItems',
            'body': {
              'Item': 'OrderItems/Item',
            },
          },
        ],
        'GetUserInfoResponse': [
          {
            'validator': isGetUserInfoResponse,
            'root': 'GetUserInfoResponse',
            'body': {
              'UserResult': 'GetUserInfoResponse/UserResult',
            },
          },
        ],
        'web:GetStockPriceRequest': [
          {
            'validator': isGetStockPriceRequest,
            'root': 'web:GetStockPriceRequest',
            'body': {
              'StockTicker': 'web:GetStockPriceRequest/web:StockTicker',
            },
          },
        ],
        'n0:SendReceiptRequest': [
          {
            'validator': isSendReceiptRequest,
            'root': 'n0:SendReceiptRequest/Body',
            'body': {
              'ContextID':   'n0:SendReceiptRequest/Body/n2:ExchangedDocumentContext/n3:GuidelineSpecifiedDocumentContextParameter/n3:ID',
              'Document':    'n0:SendReceiptRequest/Body/n2:ExchangedDocument',
              'TradeAgreement-Seller': 'n0:SendReceiptRequest/Body/n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeAgreement/n3:SellerTradeParty',
              'TradeAgreement-Buyer': 'n0:SendReceiptRequest/Body/n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeAgreement/n3:BuyerTradeParty',
              'ShipToTradeParty': 'n0:SendReceiptRequest/Body/n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeDelivery/n3:ShipToTradeParty',
              'MonetarySummation': 'n0:SendReceiptRequest/Body/n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeSettlement/n3:SpecifiedTradeSettlementHeaderMonetarySummation',
              'InvoiceeTradeParty': 'n0:SendReceiptRequest/Body/n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeSettlement/n3:InvoiceeTradeParty',
              'PayerTradeParty': 'n0:SendReceiptRequest/Body/n2:SupplyChainTradeTransaction/n3:ApplicableHeaderTradeSettlement/n3:PayerTradeParty',
            },
          },
        ],
        'n0:SendTaxInvoiceRequest': [
          {
            'validator': isSendTaxInvoiceRequest,
            'root': 'n0:SendTaxInvoiceRequest/Body',
            'body': {
              'DocContext':   'n0:SendTaxInvoiceRequest/Body/n2:ExchangedDocumentContext/n3:GuidelineSpecifiedDocumentContextParameter/n3:ID',
              'Doc':          'n0:SendTaxInvoiceRequest/Body/n2:ExchangedDocument',
              'Transaction':  'n0:SendTaxInvoiceRequest/Body/n2:SupplyChainTradeTransaction',
            },
          },
        ],
        'TestSameRootName': [
          {
            'validator': isTestSameRootName_RecordList,
            'root': 'TestSameRootName--RecordList',
            'body': {
              'header':   'TestSameRootName/DocumentHeader',
              'records':  'TestSameRootName/RecordList/record',
            },
          },
          {
            'validator': isTestSameRootName_Collection,
            'root': 'TestSameRootName--Collection',
            'body': {
              'records': 'TestSameRootName/Collection/record',
            },
          },
        ],
      },
      'Envelope': [
        # EnvelopeParser({file=xml}), ...
      ],
    }

    # processing
    initEnvelopeParser(CTX)
    initValidator(CTX)

  except Exception as e:
    print(f"[ERROR] main: {e}")

# [init] Load XML file into EnvelopeParser
def initEnvelopeParser(CTX) -> None:
  try:
    # loop each files
    for index, file in enumerate(CTX['Collection']):

      # [Error] file not exists
      if os.path.isfile(file) == False:
        raise ValueError(f"file not exists ({file})")

      # Load XML/Soap-Parser
      envelope = EnvelopeParser({
        'file': file,
      })

      # Update context
      CTX['Envelope'].append(envelope)

  except Exception as e:
    raise

# Confirm all collection files exists
def initValidator(CTX:dict) -> None:
  try:
    # loop each envelope
    for index, envelope in enumerate(CTX['Envelope']):

      # [Skip] Use Root-Node to lookup validator function
      if envelope.root not in CTX['Structure']:
        print('--- unknown xml-structure')
        continue

      # Select validator
      valid = CTX['Structure'][envelope.root]

      # [Skip] validator not found (unknown XML-Structure)
      if len(valid) == 0:
        print('--- validator not found')
        continue

      # Orginal XML-2D
      original = envelope.collapse(envelope.body)

      # Try each validator
      for info in valid:

        # Prepare XML-Validator callback
        validator = info['validator']

        # Skip invalid XML-Structure
        if validator(envelope) == False:
          continue

        # Apply Custom-Filter on matched validator 
        if True:
          envelope.root = info['root']
          envelope.body = envelope.filter(envelope.body,info['body'])

        # Stop
        break

      # 2D-Map after custom-filter
      flat = envelope.collapse(envelope.body)

      # JSON save location
      save = '.temp/soap/{index}.json'
      save = save.format(**{'index':index})

      # Create path + save file
      if mkDirname(save) == True:
        jsonSave(save,{
          'file': envelope.file,
          'root': envelope.root,
          'body': envelope.body,
          'flat': flat,
          'original': original,
        })

    # Feedback
    print('completed initValidator')

  except Exception as e:
    raise







# [XML-Validator]
def isTaxInvoiceSendRequest(envelope:EnvelopeParser) -> bool:

  # Expected root-node to be <th:TaxInvoiceSendRequest>
  if envelope.root != 'th:TaxInvoiceSendRequest':
    return False

  # XML matched
  return True

# [XML-Validator]
def isOrderItems(envelope:EnvelopeParser) -> bool:

  # Expected root-node to be <OrderItems>
  if envelope.root != 'OrderItems':
    return False

  # XML matched
  return True

# [XML-Validator]
def isGetUserInfoResponse(envelope:EnvelopeParser) -> bool:

  # Expected root-node to be <GetUserInfoResponse>
  if envelope.root != 'GetUserInfoResponse':
    return False

  # XML matched
  return True

# [XML-Validator]
def isGetStockPriceRequest(envelope:EnvelopeParser) -> bool:

  # Expected root-node to be <web:GetStockPriceRequest>
  if envelope.root != 'web:GetStockPriceRequest':
    return False

  # XML matched
  return True

# [XML-Validator]
def isSendReceiptRequest(envelope:EnvelopeParser) -> bool:

  # Expected root-node to be <n0:SendReceiptRequest>
  if envelope.root != 'n0:SendReceiptRequest':
    return False

  # XML matched
  return True

# [XML-Validator]
def isSendTaxInvoiceRequest(envelope:EnvelopeParser) -> bool:

  # Expected root-node to be <n0:SendTaxInvoiceRequest>
  if envelope.root != 'n0:SendTaxInvoiceRequest':
    return False

  # XML matched
  return True

# [XML-Validator]
def isTestSameRootName_RecordList(envelope:EnvelopeParser) -> bool:

  # Expected root-node to be <TestSameRootName>
  if envelope.root != 'TestSameRootName':
    return False

  # Collapse nested/tree-data to 2D-Map
  flat = envelope.collapse(envelope.body)

  # Missing ChildNode <record>
  if 'TestSameRootName/RecordList/record' not in flat:
    return False

  # XML matched
  return True

# [XML-Validator]
def isTestSameRootName_Collection(envelope:EnvelopeParser) -> bool:

  # Expected root-node to be <TestSameRootName>
  if envelope.root != 'TestSameRootName':
    return False

  # Collapse nested/tree-data to 2D-Map
  flat = envelope.collapse(envelope.body)

  # Missing ChildNode <record>
  if 'TestSameRootName/Collection/record' not in flat:
    return False

  # XML matched
  return True





# Start main function
if __name__ == "__main__":
  main()
