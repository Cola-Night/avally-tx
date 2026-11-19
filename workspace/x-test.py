from App.Module.Utility import *
import importlib
import inspect
import sys
import os

# Execute python-script in "App/Testing"
def main() -> None:
  try:
    # Context
    CTX = {
      'Path': {
        'Collection': 'App/Testing',
      },
      'Executor': {
        'selected': 'App.Testing.MacroCSV',
        'function': 'main',
        'arguments': [],
      },
    }

    # [init]
    # initArguments(CTX)
    # initScanModules(CTX)

    # [Executor]
    startExecutor(CTX)

  except Exception as e:
    print(f"[ERROR] x-test: {e}")

# [init] Get input arguments
def initArguments(CTX:dict) -> None:
  try:
    print('initArguments')
    
    # remove script-name
    params   = sys.argv[1:]
    length   = len(params)
    executor = ''

    # use first-param as executor
    if length > 0:
      executor = params[0]
      executor = executor.split('@')
      params   = params[1:]

    # Shortcut
    EX = CTX['Executor']

    # Update context
    match len(executor):
      case 1:
        EX['module'] = executor[0]
        EX['function'] = executor[1]

    # Update context
    EX['params']
  except Exception as e:
    raise

# [init]  
def initScanModules(CTX:dict) -> None:
  try:
    print('initScanModules')

    # Listing python-script files
    files = CTX['Path']['T']
    files = listFiles(files)

    # Process
    for path in files:
      # Convert file-path to module-path
      mp = path[:-3].replace('/','.')
      pp([path,mp])

  except Exception as e:
    raise

# Load module and execute
def startExecutor(CTX:dict) -> None:
  try:
    # Shortcut
    X = CTX['Executor']
    M = X['selected']
    F = X['function']

    # Load module (python-script file)
    module = importlib.import_module(M)
    module = importlib.reload(module)

    # Get function by string
    callback = getattr(module,F)

    # ERROR callback not callable
    if callable(callback) == False:
      raise ValueError(f"invalid callback ({M}@{F})")

    # Execute callback
    response = callback(*X['arguments'])
  except Exception as e:
    raise

# Start main function
if __name__ == "__main__":
  main()