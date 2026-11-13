from App.Module.Utility import *
import importlib
import inspect
import os

# Main
def main() -> None:
  try:
    
    # Context
    CTX = {
      'CollectionPath': [
        'App/CLI/Controller',
        'App/Script',
      ],
      'CollectionMap': {},
    }

    # init
    initCollection(CTX)

  except Exception as e:
    print(f"[ERROR] main: {e}")

# Scan .py files in "CollectionPath" directories
def initCollection(CTX) -> dict:
  try:
    # Loop each path in CollectionPath
    for index, path in enumerate(CTX['CollectionPath']):
      
      # List files in directory
      files = listRecursiveFiles(path)

      # Add .py files to CollectionMap
      for filepath in files:

        # Skip files in "__pycache__" directories
        if '__pycache__' in filepath:
          continue

        # List functions in .py file
        module = listDefinedFunctions(filepath)

        # Get [source,function]
        CTX['CollectionMap'][module['source']] = module['functions']

    # Preview
    pp(list(CTX['CollectionMap'].keys()))

  except Exception as e:
    print(f"[ERROR] initCollection: {e}")



# [helper] 
def listRecursiveFiles(path:str) -> list:
  try:
    # default output
    output = []

    # Expected path to be directory
    if not os.path.isdir(path):
      return output

    # Add files in directory into output
    for root, dirs, files in os.walk(path):
      for file in files:
        output.append(
          os.path.join(root, file)
        )

    # (list) files
    return output
  except Exception as e:
    raise

# [helper]
def listDefinedFunctions(source) -> list:
  try:
    # default output
    output = {
      'source': '',
      'functions': [],
    }

    # Convert filepath to python module
    # "App/Example/File.py" => "App.Example.File"
    if True:
      # Remove file-ext (.py)
      if source.endswith('.py'):
        source = source[:-3]

      # Replace slash to dot
      source = source.replace('/','.')
    
    # Update output[module-path]
    output['source'] = source

    # import module
    module = importlib.import_module(source)

    # Loop through all members of the module
    for name, obj in inspect.getmembers(module):
      # Skip not function
      if not inspect.isfunction(obj):
        continue
      # Skip import functions
      if obj.__module__ != module.__name__:
        continue
      # Update output
      output['functions'].append(name)
        
    # (dict)
    return output
  except Exception as e:
    raise 

# Start main function
if __name__ == "__main__":
  main()