from App.Module.Utility import *
import select
import sys
import os

# Testing CLI-Input
def main() -> None:
  try:
    # Context
    CTX = {}

    # Testing
    testInputOrTimeout(CTX)
  except Exception as e:
    print(f"[ERROR] x-cli: {e}")

# Test CLI wait for user input or timeout
def testInputOrTimeout(CTX:dict) -> None:
  try:
    print('[testInputOrTimeout]')

    # input with timer (30 seconds)
    command = inputTimer('input: ', 30.0)

    # When timeout
    if command == '':
      print('')
      print('!! TIMEOUT !!')
      return

    # Preview selected command
    print(f"{command}")

  except Exception as e:
    raise

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