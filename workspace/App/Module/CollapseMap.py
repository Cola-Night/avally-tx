from App.Module.Utility import *
import pandas as pd
import xmltodict
import os

# Collapse nested data to 2D-Map
class CollapseMap:

  def __init__(self, options:dict = {}):
    # Properties
    self.source     = None
    self.collection = {}
    self.groups     = {}

    # setup on construct
    self.setup(options)

  # Use dict to set multiple properties
  def setup(self, options: dict = {}) -> self:
    try:
      # Load XML into collection
      if 'load' in options:
        self.load(options['load'])
      
      # (self)
      return self
    except Exception as e:
      raise

  # Import XML (string)
  def importXML(self, xml:str, prefix:str = '') -> self:
    try:
      # Convert nested XML to 2D-Map
      data = xmltodict.parse(xml)
      data = pd.json_normalize(data, sep='/')
      data = data.to_dict(orient='records')[0]

      # Filter not match prefix
      for key, value in data.items():

        # Skip not match prefix
        if prefix != '' and key.startswith(prefix) != True:
          continue
        
        # Trim key-prefix
        key = key.removeprefix(prefix)
        key = key.removeprefix('/')

        # Add to collection
        self.collection[key] = value

      # (self)
      return self
    except Exception as e:
      raise
  
  # Load target XML file + collapse nested xml to 2D-Map
  def loadXML(self, file:str, prefix:str = '') -> self:
    try:
      # Confirm input file exists
      if os.path.isfile(file) == False:
        raise ValueError(f"invalid input file {file}")

      # remember source file
      self.source = file
      
      # Read XML in file
      xml = fileLoad(file)

      # (self)
      return self.importXML(xml,prefix)
    except Exception as e:
      raise
  

  # Save 2D-Map as JSON
  def save(self, file:str) -> str:
    try:
      # Save collection into JSON file
      if mkDirname(file) == True:
        jsonSave(file,self.collection)

      # (string) save file location
      return file
    except Exception as e:
      raise

  # Save Chunk-Groups as JSON
  def saveGroups(self, file:str) -> str:
    try:
      # Save collection into JSON file
      if mkDirname(file) == True:
        jsonSave(file,self.groups)

      # (string) save file location
      return file
    except Exception as e:
      raise

  # Select XML chunks
  def select(self, prefix: str, trim:bool = False) -> dict:
    try:
      # default output
      output = {}

      # Lookup items prefix matched
      for key, value in self.collection.items():

        # skip not match prefix
        if key.startswith(prefix) == False:
          continue

        # (optional) Trim Key-Prefix
        if trim == True:
          key = key.removeprefix(prefix)
          key = key.removeprefix('/')

        # add matched prefix chunks to output
        output[key] = value

      # (dict) matched prefix chunks
      return output
    except Exception as e:
      raise

  # Create chunk-group
  def grouping(self, prefix:str, name:str = '') -> dict:
    try:
      # Use prefix as name (if empty)
      if name == '':
        name = prefix

      # Remove trailing slash
      name = name.removesuffix('/')

      # Create new chunk-group
      self.groups[name] = self.select(prefix,True)

      # (dict)
      return {name: self.groups[name]}
    except Exception as e:
      raise

  # Check group exists
  def groupExists(self, name:str) -> bool:
    try:
      # GroupName not exists
      if name not in self.groups:
        return False
      
      # GroupName exists
      return True
    except Exception as e:
      raise

  # Get group
  def getGroup(self, name:str) -> dict:
    try:
      return self.groups[name]
    except Exception as e:
      raise
  
  # Filter Group-Data
  def filter(self, data:dict, prefix:str, trim:bool = False) -> dict:
    try:
      # default output
      output = {}

      # Lookup items prefix matched
      for key, value in data.items():

        # skip not match prefix
        if key.startswith(prefix) == False:
          continue

        # (optional) Trim Key-Prefix
        if trim == True:
          key = key.removeprefix(prefix)
          key = key.removeprefix('/')

        # add matched prefix chunks to output
        output[key] = value

      # (dict) matched prefix chunks
      return output

    except Exception as e:
      raise
