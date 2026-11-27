from App.Module.Utility import *
import pandas as pd
import fnmatch
import uuid

# Data-Structure Analyzer
class StructureAnalyzer:

  # Constructor
  def __init__(self):
    self.collection = {}

  # Register Structure-Name and Conditions
  def define(self, name:str, conditions:dict = {}) -> self:

    # Register new {Structure-Name => {Node-Selector => Rules[]}} 
    if name not in self.collection:
      self.collection[name] = {}

    # Select collection
    structure = self.collection[name]

    # Set Node-Selector and Rules
    for selector, rules in conditions.items():

      # Set Node-Selector
      if selector not in structure:
        structure[selector] = []

      # Select conditions-list
      conditions = structure[selector]

      # Parse Rules (string to dict)
      for rule in rules:
        
        # default
        args = []

        # Split rule (string) [key=value]
        if isinstance(rule, str):
          rule = rule.split('=', 1)
          args = rule[1].split(',')
          rule = rule[0]
        
        # Add condition
        conditions.append({
          'rule': rule,
          'args': args,
        })

    # (self)
    return self

  # Get Structure-Name by analyze input data
  def scan(self, data:list|dict) -> str:

    # default output
    structure = 'UNKNOWN'

    # Convert nested-data to summery-map
    summery = self.summery_mapping(data)

    # Try each Structure-Rule
    for name, conds in self.collection.items():
      if self.__compare(name,summery,conds) == True:
        structure = name
        break

    # (string) Structure-Name
    return structure


  # [Private]
  # Compare data with Structure-Condition
  def __compare(self, name:str, summery:dict, conditions:dict = {}) -> bool:

    # Validate-Rule mapping
    mapping = {
      'key': self.keyExists,
    }

    # (False) stop when some condition failed
    for pattern, rules in conditions.items():

      # Search summery-items matched path-pattern
      items = self.summery_filter(summery,pattern)

      # (False) Path-pattern not match
      if len(items) == 0:
        return False

      # Process validation each rules+items
      for r in rules:
        for item in items:
          # [ERROR] unknown rule
          if r['rule'] not in mapping:
            raise ValueError(f"unknown rule ({r['rule']})")

          # Select callback from mapping
          callback = mapping[r['rule']]

          # Validate-Rule failed
          if callback(item,r['args']) == False:
            return False

    # Matched found
    return True




  # [Summery-Data]
  @classmethod
  def summery_mapping(self, data:list|dict) -> dict:

    # Process memory
    summery   = {}
    tasklist  = []
    
    # Initialize tasklist
    tasklist.append({
      'path': '',
      'data': data,
    })
  
    # Continue until tasklist empty
    while len(tasklist) > 0:
      
      # Loop variables
      task = tasklist.pop()
      path = task['path']
      data = task['data']
  
      # Process dict {key => value}
      if isinstance(data, dict):

        # Update summery (Skip root)
        if len(path) > 0:
          summery[path] = {
            'type': 'dict',
            'data': data,
          }
  
        # Update tasklist
        for key, value in data.items():
          tasklist.append({
            'path': self.summery_key(path,key),
            'data': value,
          })
  
        # Goto next task
        continue
  
      # Process list {index => value}
      if isinstance(data, list):
        # Update tasklist
        for index, value in enumerate(data):
          tasklist.append({
            'path': self.summery_key(path,index),
            'data': value,
          })
  
        # Goto next task
        continue
  
      # Process value [str,int,float,object,etc...]
      if not isinstance(data, (dict, list)):
        summery[path] = {
          'type': type(data).__name__,
          'data': data,
        }
  
    # (dict)
    return summery

  # [Summery-Data]
  @classmethod
  def summery_filter(self, summery:dict, pattern:str) -> list:
    # default output
    matches = []

    # Search match path-pattern
    for path, info in summery.items():
      if fnmatch.fnmatch(path,pattern) == True:
        matches.append(info)

    # (list)
    return matches

  # [Summery-Data]
  @classmethod
  def summery_key(self, path:str, key:int|str) -> str:

    # join character
    separator = '/'

    # Force key to be string
    path = separator.join([path,str(key)])
    path = path.strip('/')

    # (str)
    return path

  # [Validate-Rule]
  @staticmethod
  def keyExists(item:dict, args:list = []) -> bool:
    if item['type'] != 'dict':
      return False

    # Listing dict.keys
    keys = list(item['data'].keys())

    # Key not found
    if args[0] not in keys:
      return False

    # Key exists
    return True