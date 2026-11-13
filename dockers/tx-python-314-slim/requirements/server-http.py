from flask import Flask
import json

# Prepare Flask (HTTP service)
server = Flask(__name__,
  static_url_path='',
  static_folder='Public',
)

@server.route('/')
def index():
  return 'Flask.index'

# Start WebServer
if __name__ == '__main__':
  server.run(
    debug=True,
    host='0.0.0.0',
  )