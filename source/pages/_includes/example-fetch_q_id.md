

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?_id=questionnaire-example-search

User-Agent: python-requests/2.20.0
Accept: application/fhir+json
Content-Type: application/fhir+json
[other headers]
~~~

**Response**

~~~
Response Code: 200 (OK)
Content-Type: application/fhir+json; charset=utf-8
Content-Location: http://sqlonfhir-stu3.azurewebsites.net/fhir/Bundle/urn:uuid:ce7769e8aac54f5084f059626d6c32de
[other headers]

    
{
   "resourceType": "Bundle",
   "id": "urn:uuid:ce7769e8aac54f5084f059626d6c32de",
   "meta": {
      "lastUpdated": "2019-02-13T08:38:57.477+00:00"
   },
   "type": "searchset",
   "total": 1,
   "link": [
      {
         "relation": "self",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?_id=questionnaire-example-search&_snapshot=636856439374771977"
      }
   ],
   "entry": [
      {
         "fullUrl": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire/questionnaire-example-search",
         "resource": {
            "resourceType": "Questionnaire",
            "id": "questionnaire-example-search",
            "meta": {
               "versionId": "19",
               "lastUpdated": "2019-02-13T08:37:05.202+00:00",
        ...[snipped for brevity]....
      
~~~
