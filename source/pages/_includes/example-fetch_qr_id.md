

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse?_id=questionnaireresponse-example-search

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
   "id": "urn:uuid:c10d8e84d0924f25a832868b9581670d",
   "meta": {
      "lastUpdated": "2019-02-13T10:28:27.237+00:00"
   },
   "type": "searchset",
   "total": 1,
   "link": [
      {
         "relation": "self",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse?_id=questionnaireresponse-example-search&_snapshot=636856505072374718"
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
