from App.Module.Utility import *
import base64

def main() -> None:
  try:
    
    # Input Base64 encoded
    encoded = ''

    # Str -> Bytes -> Str
    decoded = base64.b64decode(encoded)
    decoded = decoded.decode('utf-8')

    pp({
      'encoded': encoded,
      'decoded': decoded,
    })

  except Exception as e:
    print(f"[ERROR] main: {e}")


# Start main function
if __name__ == "__main__":
  main()