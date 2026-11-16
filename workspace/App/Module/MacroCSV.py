from typing import Self
import csv
import os

# Handling multiple CSV files
class MacroCSV:

  # Constructor
  def __init__(self, options = {}):
    self.collection = {}

  # Create new file (if already exists, auto load)
  def create(self, name, file, headers:None | list = None) -> self:
    try:
      # Load already exists CSV-file
      if os.path.isfile(file):
        return self.load(name, file)

      # Parent directories
      parent = os.path.dirname(file)

      # Create missing directories
      if not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)

      # Write CSV-Headers into file
      if isinstance(headers, list):
        with open(file, mode='w', encoding='utf-8-sig', newline='') as handle:
          writer = csv.writer(handle)
          writer.writerow(headers)

      # timestamp [created, updated]
      created = os.path.getctime(file)
      updated = os.path.getmtime(file)

      # Add to collection {name: {file,headers}}
      self.collection[name] = {
        'file': file,
        'headers': headers,
        'created': created,
        'updated': updated,
      }

      # (self)
      return self
    except PermissionError as e:
      print(f"PermissionError: {e}")
    except OSError as e:
      print(f"OSError: {e}")
      raise
    
  # Load exists csv file
  def load(self, name:str, file:str) -> self:
    try:
      # default vars
      headers = []

      # Read CSV headers
      with open(file, mode="r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        headers = next(reader)

      # timestamp [created, updated]
      created = os.path.getctime(file)
      updated = os.path.getmtime(file)

      # Add to collection {name: {file,headers}}
      self.collection[name] = {
        'file': file,
        'headers': headers,
        'created': created,
        'updated': updated,
      }

      # (self)
      return self
    except PermissionError as e:
      raise
    except OSError as e:
      raise

  # Append new CSV-Row
  def append(self, name:str, row:list | dict) -> Self:
    try:
      # ERROR: unknown collection name
      if name not in self.collection:
        raise ValueError(f"unknown name: {name}")

      # Lookup CSV-File by name
      data = self.collection[name]
      file = data['file']

      # csv.writer | csv.DictWriter
      with open(file, mode='a', newline='', encoding='utf-8-sig') as handle:
        writer = self.writerByType(handle,row)
        writer.writerow(row)

      # (self)
      return self
    except Exception as e:
      raise

  # Read CSV-file headers
  def readHeaders(self, file:str) -> list:
    try:
      # default headers
      headers = []

      # Read CSV-file headers
      with open(file, mode='r', newline='', encoding='utf-8-sig') as handle:
        reader = csv.reader(handle)
        headers = next(reader)

      # (list)
      return headers
    except PermissionError as e:
      raise
    except OSError as e:
      raise

  # Use row type to construct (csv.writer) or (csv.DictWriter)
  def writerByType(self, handle, row:list | dict):
    try:
      # default writer handle
      writer = None

      # row is (list) = csv.writer
      if isinstance(row, list):
        writer = csv.writer(handle)

      # row is (dict) = csv.DictWriter
      if isinstance(row, dict):
        headers = self.readHeaders(handle.name)
        writer  = csv.DictWriter(handle, fieldnames=headers)

      # (None|csv.writer|csv.DictWriter)
      return writer
    except Exception as e:
      raise
  