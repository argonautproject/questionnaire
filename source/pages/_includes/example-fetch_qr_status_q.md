

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse?status=completed&questionnaire=questionnaire-example-search

User-Agent: python-requests/2.20.0
Accept: application/fhir+json
Content-Type: application/fhir+json
[other headers]
~~~

**Response**

~~~
Response Code: 200 (OK)
Content-Type: application/fhir+json; charset=utf-8
[other headers]

    
{
   "resourceType": "Bundle",
   "id": "urn:uuid:1e79af295b464c7a95e037ed445bd03b",
   "meta": {
      "lastUpdated": "2019-02-13T10:28:30.82+00:00"
   },
   "type": "searchset",
   "total": 2,
   "link": [
      {
         "relation": "self",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse?status=completed&questionnaire=questionnaire-example-search&_snapshot=636856505108205642"
      }
   ],
   "entry": [
      {
         "fullUrl": "http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse/questionnaireresponse-example-search",
         "resource": {
            "resourceType": "QuestionnaireResponse",
            "id": "questionnaireresponse-example-search",
            "meta": {
               "versionId": "1",
        ...[snipped for brevity]....
      
~~~
