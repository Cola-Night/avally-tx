from App.Module.Utility import *
import importlib
import inspect
import select
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
        'Prefix': 'App.Testing',
        'Callback':  None, # None | list
        'Arguments': [],
        'Mapping': {
          'MacroCSV': {},
          'TaxOneAPI': {},
        },
      },
    }

    # [init]
    initArguments(CTX)
    initScanModules(CTX)
    startExecutor(CTX)

  except Exception as e:
    print(f"[ERROR] x-test: {e}")

# [init] Use terminal arguments to update context
def initArguments(CTX:dict) -> None:
  try:
    # remove first-item in list
    args = sys.argv[1:]

    # empty input
    if len(args) < 1:
      return

    # Context shortcut
    EX = CTX['Executor']

    # use first-arg as callback (module@function)
    callback = args[0].split('@')

    # Set default-function (if missing)
    if len(callback) < 2:
      callback.append('main')
    
    # Update context
    EX['Callback']  = callback
    EX['Arguments'] = args[1:]

  except Exception as e:
    raise

# [init]
def initScanModules(CTX:dict) -> None:
  try:
    # Context shortcut
    EX = CTX['Executor']
    
    # Listing python-script files
    files = listFiles(CTX['Path']['Collection'])

    # Reset mapping
    EX['Mapping'] = {}

    # Convert file-path to module-path
    for source in files:

      # Convert to module-path
      module = source[:-3].replace('/','.')

      # Lookup key
      key = module.removeprefix(EX['Prefix'])
      key = key.lstrip('.')
      
      # Update mapping
      EX['Mapping'][key] = {
        'source': source,
        'module': module,
      }

  except Exception as e:
    raise

# Load module and execute
def startExecutor(CTX:dict) -> None:
  try:
    # Shortcut
    EX = CTX['Executor']

    # Callback not set
    if EX['Callback'] == None:
      return

    # Module-Path
    path = '{Prefix}.{Path}'
    path = path.format(**{
      'Prefix': EX['Prefix'],
      'Path': EX['Callback'][0],
    })
    
    # Load module (python-script file)
    module = importlib.import_module(path)
    module = importlib.reload(module)

    # Select function in module
    callback = getattr(module,EX['Callback'][1])

    # Execute callback
    response = callback(*EX['Arguments'])

  except Exception as e:
    raise






# Todo:
# Input with timer (default 10.0 seconds)
def inputTimer(label: str, secs: float = 10.0) -> str:

  # Display input label
  print(label, end="", flush=True)

  # waiting for user input or timeout
  ready, _, _ = select.select([sys.stdin], [], [], secs)

  # input success
  if ready:
    return sys.stdin.readline().rstrip("\n")
  
  # timeout
  return ''


# Start main function
if __name__ == "__main__":
  main()