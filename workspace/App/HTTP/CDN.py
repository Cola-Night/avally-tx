from flask import request, abort, send_file
from typing import Any
import magic
import os

# App.HTTP.CDN@main
def main(params:dict = {}) -> Any :

  # Use "filepath" to lookup file in CDN directory
  source = 'Storage/CDN/{filepath}'
  source = source.format(**{
    'filepath': params['filepath'],
  })

  # Convert to RealPath
  source = os.path.abspath(source)

  # [Error-404] when file not exists
  if os.path.isfile(source) == False:
    abort(404)

  # Guess file MIME-Type
  mime = magic.from_file(source, mime=True)

  # (Response MediaFile)
  return send_file(source, mimetype=mime)