import base64
import json
import inspect
import pprint
import os

# Pretty-Print
def pp(data) -> None:
  pprint.pp(data)

# EXPERIMENTAL
# list function/method parameters
def inspectParams(callback) -> list:
  sig = inspect.signature(callback)
  params = list(sig.parameters.keys())
  return params


# Convert [list|dict] to 2D-Map (dict)
def flat2D(data:list|dict, parent_key:str='', sep:str='/') -> dict:
  items = []
  if isinstance(data, dict):
    for k, v in data.items():
      new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
      items.extend(flat2D(v, new_key, sep=sep).items())
  elif isinstance(data, list):
    for i, v in enumerate(data):
      new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
      items.extend(flat2D(v, new_key, sep=sep).items())
  else:
    items.append((parent_key, data))
  return dict(items)


# list files in directory
def listFiles(path:str) -> None | list:
  try:
    # [None] path is not directory
    if not os.path.isdir(path):
      return None

    # default output
    files = []

    # List files in directory
    with os.scandir(path) as entries:
      for entry in entries:
        # Only file (Skip directory or shortcut)
        if not entry.is_file():
          continue
        
        # Add file
        files.append(
          os.path.join(path,entry.name)
        )

    # (list)
    return files
  except Exception as e:
    raise

# Check file-type is "file" (not dir)
def isFile(path:str) -> bool:
  try:
    return os.path.isfile(path)
  except Exception as e:
    raise

# Save data into file
def fileSave(file, data):
  try:
    # Try convert data to string
    if not isinstance(data, str):
      data = str(data)

    # Write data into file
    with open(file, "w", encoding="utf-8") as f:
      f.write(data)
  except Exception as e:
    raise

# Load data from file
def fileLoad(file):
  try:
    with open(file, "r") as f:
      return f.read()
  except Exception as e:
    raise

# Get filepath "dirname" and create missing dirs
def mkDirname(file:str) -> bool:
  try:
    # Get dirname
    dirname = os.path.dirname(file)
    # create directories recursively
    os.makedirs(dirname, exist_ok=True)
    return True
  except:
    return False

# Validate JSON
def isValidJSON(encoded:str) -> bool:
  try:
    json.loads(encoded)
    return True
  except json.decoder.JSONDecodeError:
    return False

# Load JSON-file
def jsonLoad(file) -> list | dict:
  try:
    # Open file (r = read mode)
    with open(file, "r", encoding="utf-8") as f:
      data = json.load(f)
    
    # (list|dict)
    return data
  except Exception as e:
    raise

# Save JSON-file
def jsonSave(file, data: str|list|dict) -> bool:
  try:
    # Convert (list|dict) to string (JSON Pretty-Print)
    if not isinstance(data, str):
      data = json.dumps(data, indent=2, ensure_ascii=False)

    # Input is string but invalid JSON
    if isValidJSON(data) == False:
      return False

    # Write JSON info file (w = write mode)
    with open(file, "w", encoding="utf-8") as f:
      f.write(data)
    
    # (bool) success
    return True
  except Exception as e:
    raise





# Base64 encode
def b64_encode(message:str|bytes) -> str:
  try:
    # convert: message/string -> message/bytes
    if isinstance(message, str):
      message = message.encode('utf-8')

    # convert: message/bytes -> base64/bytes -> base64/string
    encoded_b = base64.b64encode(message)
    encoded_s = encoded_b.decode("utf-8")

    # (string)
    return encoded_s
  except Exception as e:
    raise

# Base64 decode
def b64_decode(encoded:str) -> str:
  try:
    # b64/string -> decoded/bytes -> decoded/string
    decoded_b = base64.b64decode(encoded)
    decoded_s = decoded_b.decode('utf-8')
    return decoded_s
  except Exception as e:
    raise

