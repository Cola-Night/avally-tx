from App.Module.Utility import *
import base64

def main() -> None:
  try:
    
    # Original-Text
    original = 'Testing'

    # Conv. text to bytes
    encoded = original.encode('utf-8')
    encoded = base64.b64encode(encoded)
    encoded = encoded.decode("utf-8")

    pp({
      'original': original,
      'encoded': encoded,
    })

  except Exception as e:
    print(f"[ERROR] main: {e}")
