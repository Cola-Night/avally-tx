from App.Module.Utility import *
import base64

def main() -> None:
  try:
    
    # Input Base64 encoded
    encoded = []
    
    # default output
    decoded = []

    # Str -> Bytes -> Str
    for value in encoded:
      # Base64 decode
      value = base64.b64decode(value)
      value = value.decode('utf-8')
      # Update output
      decoded.append(value)

    # View
    pp({
      'encoded': encoded,
      'decoded': decoded,
    })

  except Exception as e:
    print(f"[ERROR] main: {e}")
