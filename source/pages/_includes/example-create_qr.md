

**Request**

~~~
POST http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse

User-Agent: python-requests/2.20.0
Accept: application/fhir+json
Content-Type: application/fhir+json
[other headers]
~~~

**Response**

~~~
Response Code: 201 (Created)
Content-Type: application/fhir+json; charset=utf-8
Content-Location: http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse/2dcdb4a057b941c9b3ad0c8d5bf68d42/_history/1
[other headers]

    
{
   "resourceType": "QuestionnaireResponse",
   "id": "2dcdb4a057b941c9b3ad0c8d5bf68d42",
   "meta": {
      "versionId": "1",
      "lastUpdated": "2019-02-13T09:07:09.672+00:00",
      "profile": [
         "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-questionnaireresponse"
      ]
   },
   "text": {
      "status": "generated",
      "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n    <h3>Response Summary</h3>\n    <strong>Questionnaire URL:</strong> http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-sampler<br />\n    <strong>Date Completed:</strong> 2019-02-13T00:39:38.320181Z<br />\n    <hr /> <br /><strong>The Argonaut Questionnaire Sampler is designed to show all the question types that can be used in the Argonaut Questionnaire Project:\n\n1 boolean\n2 decimal\n3 int
        ...[snipped for brevity]....
      
~~~
