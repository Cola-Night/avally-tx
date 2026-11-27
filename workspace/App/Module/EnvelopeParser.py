from typing import Any
from collections.abc import Callable
from App.Module.Utility import *
import pandas as pd
import xmltodict
import os

# XML or Soap-XML parser
class EnvelopeParser:

  def __init__(self, options:dict = {}):

    # properties
    self.file = None  # source file -- loadFile()
    self.head = None  # <soap:Header>
    self.body = None  # <soap:Body>
    self.root = ''    # Root-Node in <soap:Body>

    # setup on construct
    self.setup(options)

  # Load options to set properties
  def setup(self, options:dict = {}) -> self:
    try:

      # Load XML
      if 'xml' in options:
        self.loadXML(options['xml'])

      # Load XML in file
      if 'file' in options:
        self.loadFile(options['file'])

      # (self)
      return self
    except Exception as e:
      raise

  # Load XML
  def loadXML(self, xml:str) -> self:
    try:
        
      # Parse XML and unwrap <XX:Envelope>
      data = self.unwrap(xml)

      # Envelope data
      self.head = data['head'] # <soap:Header> (None|dict)
      self.body = data['body'] # <soap:Body>   (None|dict)

      # Root-Node (str)
      self.root = self.getKey(self.body,0)

      # (self)
      return self

    except Exception as e:
      raise

  # Load XML from file
  def loadFile(self, file:str) -> self:
    try:
      # [Error] file not exists
      if os.path.isfile(file) == False:
        raise ValueError(f"file not exists ({file})")
      
      # Read XML in file
      xml = fileLoad(file)

      # Load XML
      return self.loadXML(xml)

    except Exception as e:
      raise

  @classmethod
  def filter(self, tree:list|dict, mapping:dict = {}) -> dict:
    try:
      # default output
      output = {}

      # Update output
      for key, path in mapping.items():
        output[key] = self.pointer(tree,path)

      # (dict)
      return output
    except Exception as e:
      raise
  
  # Unwrap <XX:Envelope> (if exists)
  @classmethod
  def unwrap(self, xml:str) -> dict:
    try:
      # Soap-Envelope collection
      collection = {
        'soapenv:Envelope': {
          'head': 'soapenv:Envelope/soapenv:Header',
          'body': 'soapenv:Envelope/soapenv:Body',
        },
        'soap:Envelope': {
          'head': 'soap:Envelope/soap:Header',
          'body': 'soap:Envelope/soap:Body',
        },
      }

      # default output
      output = {
        'head': None,
        'body': None,
      }

      # Parse XML
      data = xmltodict.parse(xml)
      root = self.getKey(data,0)

      # Root-Node is <XX:Envelope>
      if root in collection:
        # Select Envelope-mapping {head,body}
        mapping = collection[root]

        # Extract data
        output['head'] = self.pointer(data,mapping['head'])
        output['body'] = self.pointer(data,mapping['body'])

      # Root-Node is NOT <XX:Envelope>
      if output['body'] == None:
        output['body'] = data

      # (dict) {head,body}
      return output

    except Exception as e:
      raise

  @classmethod
  def getKey(self, tree:list|dict, index:int) -> None | str:
    try:
      # List keys in tree
      keys = tree.keys()
      keys = list(keys)

      # (None) Index not found
      if len(keys) < index:
        return None

      # (str) Select key by index
      return keys[index]
    except Exception as e:
      raise

  @classmethod
  def pointer(self, tree:list|dict, path:str|list) -> Any:
    try:
      # Split path
      if isinstance(path, str):
        path = path.split('/')
      
      # Go deeper into nested-data
      for index, key in enumerate(path):

        # Convert key to int
        if isinstance(tree, list):
          key = int(key)
    
        # path not found
        if key not in tree:
          tree = None
          break
    
        # Go deeper
        tree = tree[key]

      # (Any)
      return tree
    except Exception as e:
      raise

  # Collapse nested/tree data structure to 2D-Map [key => value]
  @classmethod
  def collapse(self, tree:list|dict, separator:str = '/') -> dict:
    try:
      # Convert nested-data to 2D-Map
      data = pd.json_normalize(tree, sep=separator)
      data = data.to_dict(orient='records')[0]

      # (dict) 2D-Map
      return data
    except Exception as e:
      raise
