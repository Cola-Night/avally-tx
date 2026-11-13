from flask import request
import uuid

# [POST] /api/v1/upload.json (API.V1.Upload@main)
# Upload file to temp-upload directory.
# then return { uppload-token }
def main(params:dict = {}):

  # TempUploadFile unique token
  token = generateToken()

  # Response-Body
  response = {
    'status': 200,
    'message': 'upload success',
    'token': token,
  }

  # HTTP-Response
  return response


# Genetate unique token
def generateToken() -> str:

  # Geneate token
  token = uuid.uuid4()

  # upload temp storage
  path = '.temp/upload/{token}'
  path = path.format(**{
    'token': token,
  })

  # Geneate new token if already in used
  while os.path.isfile(path):

    # Geneate new token
    token = uuid.uuid4()

    # upload temp storage
    path = '.temp/upload/{token}'
    path = path.format(**{
      'token': token,
    })

  # (string) temp-upload-token
  return token