

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse?status=completed&patient=subject1&context=encounter2

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
   "id": "urn:uuid:e9a87fdd8b244ca4ab4ee4a29caef4b1",
   "meta": {
      "lastUpdated": "2019-02-13T11:15:50.915+00:00"
   },
   "type": "searchset",
   "total": 1,
   "link": [
      {
         "relation": "self",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse?status=completed&patient=subject1&context=encounter2&_snapshot=636856533509154158"
      }
   ],
   "entry": [
      {
         "fullUrl": "http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse/questionnaireresponse-example-phq9-enc2",
         "resource": {
            "resourceType": "QuestionnaireResponse",
            "id": "questionnaireresponse-example-phq9-enc2",
            "meta": {
               "versionId": "2",
               "lastUpdated": "2018-07-27T20:36:40.103+00:00",
               "profile": [
                  "http://fhir.org/guides/argonaut/questionnaire/StructureDefinition/argo-questionnaireresponse"
               ]
            },
            "identifier": {
               "value": "test"
            },
            "questionnaire": {
               "reference": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-phq9"
            },
            "status": "completed",
            "subject": {
               "reference": "Patient/subject1"
            },
            "context": {
               "reference": "Encounter/encounter2"
            },
            "authored": "2018-07-27T04:04:33.927848",
            "author": {

        ...[snipped for brevity]....

~~~
