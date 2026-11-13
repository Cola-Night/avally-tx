from flask import request

# API.V1.Index@main
def main(params:dict = {}):

  # Response-Body
  response = {
    'api/v1': {
      # list api urls
      '/api/v1/index.json': {
        'methods': 'GET',
        'accept': '*',
      },
      # test file upload
      '/api/v1/upload.json': {
        'methods': 'POST',
        'accept': 'multipart/form-data',
        'response': 'application/json',
      },
      # test client request
      '/api/v1/test.json': {
        'methods': 'GET|POST|PUT|DELETE|PATCH',
        'accept': '*',
      },
    },
    'taxone-API/V2.1': {
      '/taxone-API/V2.1/etax/receipt': {
        'methods': 'POST',
        'accept': 'text/xml',
      },
    },
  }

  # HTTP-Response
  return response
