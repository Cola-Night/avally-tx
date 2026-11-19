# Research

## API Key Generation / Replacement

If you need to generate a new API Key or replace an existing one, please contact
the administrator via email at taxoneapp@stream.co.th.
The administrator will generate a new API Key and send it to you.

Authentication
The API uses Basic Authentication, which requires the following credentials:
  - Username
  - Password
  - API-Key

ref: 


## x-test.py TaxOneAPI@main

```bash
# Execute testing script
# - file: App/Testing/TaxOneAPI.py
# - module: App.Testing.TaxOneAPI
# - function: main()
python x-test.py TaxOneAPI@main
```

### [T01] send without header[Authorization]

```txt
HTTP/1.1 400 BAD REQUEST
Content-Type: application/json;charset=UTF-8

{
  "timestamp": 1794974115964,
  "status": 400,
  "error": "Bad Request",
  "exception": "org.springframework.web.bind.ServletRequestBindingException",
  "message": "Missing request header 'Authorization' for method parameter of type String"
}
```

### [T02] send without header[API-Key]

```txt
HTTP/1.1 400 BAD REQUEST
Content-Type: application/json;charset=UTF-8

{
  "timestamp": 1794974233139,
  "status": 400,
  "error": "Bad Request",
  "exception": "org.springframework.web.bind.ServletRequestBindingException",
  "message": "Missing request header 'API-Key' for method parameter of type String"
}
```

### Mapping S4HANA-XML (n1) to TaxOne-API

| API-Body                  | Type              | Example             |
|:--------------------------|:------------------|:--------------------|
| header.messageID          | String            |                     |
| header.messsentDTTMageID  | String            | YYYY-MM-DD hh:mm:ss |
| header.outputResponseType | Int               | 2                   |
| etax.documentLanguage     | String            | EN                  |
| etax.documentRefNo        | String            |                     |
| etax.docRefIssueDateTime  | String            |                     |
| etax.documentRefType      | String            |                     |
| etax.productCode          | String            | Stream              |
| etax.branchCode           | String            | 00000               |
| etax.customerProfile      | Record{}          | CustomerProfile{}   |
| etax.mailingAddress       | Record{}          | MailingAddress{}    |
| etax.documents            | [ Record{}, ... ] | [ Document{}, ... ] |
| etax.optional             | Map{Key,Value}    | ???                 |



#### [Record] CustomerProfile{}:

| Key             | Type   | Example             |
|:----------------|:-------|:--------------------|
| cusCompanyName  | String |                     |
| cusTaxType      | String | TXID                |
| cusTaxID        | String | 010554409966600000  |
| cusVATBranch    | String |                     |
| cusPostcode     | String |                     |
| cusAddressLine1 | String |                     |
| cusAddressLine2 | String |                     |
| cusAddressLine3 | String |                     |
| cusCountryID    | String | TH                  |
| mobileNo        | String |                     |
| email           | String |                     |

#### [Record] MaillingAddress{}:

| Key              | Type   | Example |
|:-----------------|:-------|:--------|
| shipPostcode     | String | ?       |
| shipAddressLine1 | String | ?       |
| shipAddressLine2 | String | ?       |
| shipAddressLine3 | String | ?       |
| shipCountryID    | String | ?       |

#### [Record] Document{}:

| Key                          | Type              | Example             |
|:-----------------------------|:------------------|:--------------------|
| documentNo                   | String            |                     |
| documentType                 | String            |                     |
| documentTypeCode             | String            |                     |
| purpose                      | String            |                     |
| purposeCode                  | String            |                     |
| issueDateTime                | String            | YYYY-MM-DD hh:mm:ss |
| creationDateTime             | String            | YYYY-MM-DD hh:mm:ss |
| currency                     | String            | THB                 |
| taxCode                      | String            | VAT                 |
| dcnTaxInvoice                | Bool              | TRUE,FALSE          |
| calculatedRate               | Number/Int?       |                     |
| basisAmount                  | Number/Float      | 10000.0             |
| calculatedAmount             | Number/Float      | 700.0               |
| originalInformationAmount    | Number/Float      | 0.0                 |
| lineTotalAmount              | Number/Float      | 10000.0             |
| differenceInformationAmount  | Number/Float      | 0.0                 |
| allowanceTotalAmount         | Number/Float      | 0.0                 |
| taxBasisTotalAmount          | Number/Float      | 10000.0             |
| taxTotalAmount               | Number/Float      | 700.0               |
| grandTotalAmount             | Number/Float      | 10700.0             |
| products                     | [ Record{}, ... ] | [ Project{}, ... ]  |

#### [Record] Project{}:

| Key                               | Type           | Example |
|:----------------------------------|:---------------|:--------|
| lineNO                            | String         |         |
| itemID                            | String         |         |
| itemName                          | String         |         |
| itemUnit                          | String         |         |
| calculatedRate                    | Number/Int?    |         |
| itemBilledQuantity                | Number/Int?    |         |        
| itemChargeAmount                  | Number/Float   |         |
| netLineTotalAmount                | Number/Float   |         |
| netIncludingTaxesLineTotalAmount  | Number/Float   |         |
| optional                          | Map{Key,Value} | ???     |