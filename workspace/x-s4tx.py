from App.Module.Utility import *
from App.Model.S4TX import S4TX

# Testing convert S4HANA.XML to TaxOne.JSON
def main() -> None:
  try:
    # Load S4HANA.XML
    xml = 'Storage/S4HANA/TaxInvoice/TaxInvoice-0090001097/n0-SendTaxInvoiceRequest.xml'
    xml = fileLoad(xml)

    # Convert XML to JSON (Request-Body)
    body = S4TX.convert(xml)

    pp(body)

  except Exception as e:
    print(f"[ERROR] main: {e}")
  
# Start main function
if __name__ == "__main__":
  main()