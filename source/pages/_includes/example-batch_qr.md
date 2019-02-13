

**Request**

~~~
POST http://sqlonfhir-stu3.azurewebsites.net/fhir

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
   "type": "transaction-response",
   "total": 14,
   "entry": [
      {
         "fullUrl": "http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse/questionnaire-example-delete",
         "resource": {
            "resourceType": "QuestionnaireResponse",
            "id": "questionnaire-example-delete",
            "meta": {
               "versionId": "8",
               "lastUpdated": "2019-02-13T09:55:57.695+00:00",
               "profile": [
                  "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-questionnaireresponse"
               ]
            },
            "text": {
               "status": "generated",
               "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><h3>Response Summary</h3><strong>Questionnaire URL:</strong> http://fhir.org/guides
        ...[snipped for brevity]....
      
~~~
