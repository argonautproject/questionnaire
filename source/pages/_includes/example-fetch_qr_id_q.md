

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse?_id=questionnaireresponse-example-search&_include=QuestionnaireResponse%3Aquestionnaire

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
   "id": "urn:uuid:25162d3c0d1241348e129bf592fe20a0",
   "meta": {
      "lastUpdated": "2019-02-13T10:28:28.112+00:00"
   },
   "type": "searchset",
   "total": 1,
   "link": [
      {
         "relation": "self",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse?_id=questionnaireresponse-example-search&_include=QuestionnaireResponse%3Aquestionnaire&_snapshot=636856505081124854"
      }
   ],
   "entry": [
      {
         "fullUrl": "http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse/questionnaireresponse-example-search",
         "resource": {
            "resourceType": "QuestionnaireResponse",
            "id": "questionnaireresponse-example-search",
            "meta": {

        ...[snipped for brevity]....


   "resourceType": "Questionnaire",
   "id": "questionnaire-example-sampler",
   "meta": {
      "versionId": "1",
      "lastUpdated": "2019-02-13T05:57:59.507-05:00",
      "profile": [
        "http://fhir.org/guides/argonaut/questionnaire/StructureDefinition/argo-questionnaire"
      ]
    },
  "text": {

        ...[snipped for brevity]....

~~~
