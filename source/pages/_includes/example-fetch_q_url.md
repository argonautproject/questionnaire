

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?url=http%3A%2F%2Ffhir.org%2Fguides%2Fargonaut-questionnaire%2FQuestionnaire%2Fquestionnaire-example-search

User-Agent: python-requests/2.20.0
Accept: application/fhir+json
Content-Type: application/fhir+json
[other headers]
~~~

**Response**

~~~
Response Code: 200 (OK)
Content-Type: application/fhir+json; charset=utf-8
Content-Location: http://sqlonfhir-stu3.azurewebsites.net/fhir/Bundle/urn:uuid:334db1311eea4e4b80f5560aed8b6d1f
[other headers]


{
   "resourceType": "Bundle",
   "id": "urn:uuid:334db1311eea4e4b80f5560aed8b6d1f",
   "meta": {
      "lastUpdated": "2019-02-13T08:38:57.977+00:00"
   },
   "type": "searchset",
   "total": 1,
   "link": [
      {
         "relation": "self",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?url=http%3A%2F%2Ffhir.org%2Fguides%2Fargonaut-questionnaire%2FQuestionnaire%2Fquestionnaire-example-search&_snapshot=636856439379772204"
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
    "profile": [
        "http://fhir.org/guides/argonaut/questionnaire/StructureDefinition/argo-questionnaire"
    ]
    },
    "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\r\n\t<b>Argonaut Questionnaire Sampler</b>\r\n\t<hr/>\r\n\t\t<span style=\"color: gray;\">Publisher:</span> Argonaut Project\r\n</div>\r\n"
    },
    "extension": [
    {
        "url": "http://fhir.org/guides/argonaut/questionnaire/StructureDefinition/extension-timeLimit",
        "valueDuration": {
            "value": 5,
            "unit": "minute",
            "system": "http://unitsofmeasure.org",
            "code": "min"
        }
    }
    ],
    "url": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-search",
        ...[snipped for brevity]....

~~~
