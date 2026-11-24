from App.Module.Utility import *
import importlib
import inspect
import os

# Execute python-script in "App/Script"
def main() -> None:
  try:
    # Context
    CTX = {
      'Path': {
        'Script': 'App/Script',
      },
      'Commands': {
        'b64-encode': {
          'callback': 'App.Script.B64Encode@main',
        },
        'b64-decode': {
          'callback': 'App.Script.B64Decode@main',
        },
      },
    }
    
  except Exception as e:
    print(f"[ERROR] main: {e}")

# Start main function
if __name__ == "__main__":
  main()