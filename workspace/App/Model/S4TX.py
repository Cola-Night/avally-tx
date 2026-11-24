from App.Module.Utility import *

# Convert S4HANA.XML to TaxOne.JSON
class S4TX:
  
  @classmethod
  def convert(self, xml: str|list|dict) -> dict:
    try:
      # Context
      CTX = {
        'S4': xml,
        'TaxOne': {
          'header': {},
          'etax': {},
        },
        'Template': {},
      }

      # process
      self.loadTemplate(CTX)
      self.buildDocuments(CTX)

      # (dict) TaxOne
      return CTX['TaxOne']
    except Exception as e:
      raise

  # Load template resources
  @classmethod
  def loadTemplate(self, CTX:dict):
    try:
      # Load templates
      temp = 'Storage/TaxOne/API-Body-Template.json'
      temp = jsonLoad(temp)

      # remember templates
      CTX['Template'] = temp

      # Build RequestBody base structure
      body = temp['Template/Body']
      body = body['Structure']

      # Clone template (avoid overwrite original)
      CTX['TaxOne'] = body.copy()
      
    except Exception as e:
      raise
  
  # Use data in S4HANA.XML to create Documents[]
  @classmethod
  def buildDocuments(self, CTX:dict) -> None:
    try:
      # Shortcut
      body = CTX['TaxOne']

      # DUMMY create Documents[]
      for i in range(2):
        # Create Template/Document
        doc = self.createDocument(CTX)
        body['etax']['documents'].append(doc)

        # Create dummy Product
        pro = self.createProduct(CTX)
        doc['products'].append(pro)

    except Exception as e:
      raise
  
  # Create template Document
  @classmethod
  def createDocument(self, CTX:dict) -> dict:
    try:
      # Shortcut
      temp = CTX['Template']

      # Create template
      doc = temp['Template/Document']
      doc = doc['Structure']
      doc = doc.copy()

      # (dict)
      return doc
    except Exception as e:
      raise

  # Create template Product
  @classmethod
  def createProduct(self, CTX:dict) -> dict:
    try:
      # Shortcut
      temp = CTX['Template']

      # Create template
      pro = temp['Template/Product']
      pro = pro['Structure']
      pro = pro.copy()

      # (dict)
      return pro
    except Exception as e:
      raise