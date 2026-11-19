# TaxOne-API

- Generate document
- HTTP Status-Code

## Generate document

Method:
  - POST

URL-Examples:
  - https://[Host]/taxone-API/[Version]/etax/receipt
  - https://test.streamtaxone.com/taxone-API/V2.1/etax/receipt
  - https://smarttaxone.streamtaxone.com/taxone-API/V2.1/etax/receipt

Headers:
  - Authorization: Basic [Base64("USERNAME:PASSWORD")]
  - Content-Type: application/json
  - API-Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.B64(Payload).Base64(Signature)

<br>

```txt
NOTE: Header[API-Key] without prefix `Bearer` 

✅ Correct
API-Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....

❌ Wrong:
API-Key: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....
```

## Response JSON

```
Note: M/O | M = Mandatory | O = Optional
```

| Field Name            | Type         | Description                               | M/O |
|:----------------------|:-------------|:------------------------------------------|:---:|
| data.transactionRefNo | String       | Transaction ID Referenced from Body Input |  O  |
| data.resultCode       | String       |                                           |  M  |
| data.resultMessage    | String       |                                           |  M  |
| data.fileNamePdf      | NULL, String | Generated PDF name                        |  M  |
| data.fileDataPdf      | NULL, String | Generated PDF in Base64 format            |  O  |
| data.fileNameXml      | NULL, String | Generated XML name                        |  M  |
| data.fileDataXml      | NULL, String | Generated XML in Base64 format            |  O  |
| header.messageID      | String       | Message ID Referenced from Body Input     |  O  |
| header.responseDTTM   | String       | System received time                      |  M  |


#### Result Code and Message

| Code | Message                     |
|:----:|:----------------------------|
| 200  | Success                     |
| 201  | Duplicate geerated document |
| 202  | Invalid data value          |
| 203  | Invalid data format         |
| 301  | Authentication failure      |

#### Error-Case: 301 &mdash; "Authentication failure"

```json
{
  "data": {
    "transactionRefNo": "",
    "resultCode": "301",
    "resultMessage": "Authentication failure",
    "fileNamePdf": null,
    "fileDataPdf": null,
    "fileNameXml": null,
    "fileDataXml": null
  },
  "header": {
    "messageID": "STREAM01",
    "responseDTTM": "2026-11-17 18:06:12"
  }
}
```

#### Success-202: Valid-Formal but Invalid data 

```json
{
  "data": {
    "transactionRefNo": "",
    "resultCode": "202",
    "resultMessage": "Please check product or branch code",
    "fileNamePdf": null,
    "fileDataPdf": null,
    "fileNameXml": null,
    "fileDataXml": null
  },
  "header": {
    "messageID": "STREAM01",
    "responseDTTM": "2026-11-19 16:44:25"
  }
}
```

#### Success-Case: 200 &mdash; "Receive Transaction Success"

```json
{
  "data": {
    "transactionRefNo": "TX20230810140030867",
    "resultCode": "200",
    "resultMessage": "Receive Transaction Success",
    "fileNamePdf": "20230810_ST_Test_001_TIV_EN.pdf",
    "fileDataPdf": "Base64......",
    "fileNameXml": "20230810_ST_Test_001_TIV_EN.xml",
    "fileDataXml": "Base64......",
  },
  "header": {
    "messageID": "XXXXXYYYYYZZZZZ",
    "responseDTTM": "2023-08-10 15:48:40"
  }
}
```

## HTTP Status-Code

| Code                       | Description          |
|:---------------------------|:---------------------|
| 200 OK                     | Valid request format |
| 400 Bad Request            | Invalid parameter    |
| 404 Not Found              | Invalid URL          |
| 405 Method Not Allowed     | Invalid Method       |
| 500 Inteernal SErver Error | Invalid Body         |