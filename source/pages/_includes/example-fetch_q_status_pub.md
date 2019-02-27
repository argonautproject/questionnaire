

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?_count=75&status=draft&publisher=Argonaut+Project

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
   "id": "urn:uuid:0037e580968f40d494a9afcc19e3ce2d",
   "meta": {
      "lastUpdated": "2019-02-27T02:59:42.676+00:00"
   },
   "type": "searchset",
   "total": 30,
   "link": [
      {
         "relation": "self",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?_count=75&status=draft&publisher=Argonaut+Project&_snapshot=636868331826761687"
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
                  "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-questionnaire"
               ]
            },
            "text": {
               "status": "generated",
               "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><b>Argonaut Questionnaire Sampler</b><hr /><span style=\"color: gray;\">Publisher:</span> Argonaut Project\r\n</div>"
            },
            "extension": [
               {
                  "url": "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/extension-timeLimit",
                  "valueDuration": {
                     "value": 5,
                     "unit": "minute",
                     "system": "http://unitsofmeasure.org",
                     "code": "min"
                  }
               }
            ],
            "url": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-search",
            "identifier": [
               {
                  "system": "http://acme.org/q-identifiers",
                  "value": "questionnaire-example-sampler"
               }
            ],
            "version": "3.0.0",
            "title": "Argonaut Questionnaire Sampler",
            "status": "draft",
            "date": "2018-07-26",
            "publisher": "Argonaut Project",
            "useContext": [
               {
                  "code": {
                     "system": "http://hl7.org/fhir/usage-context-type",
                     "code": "task",
                     "display": "Workflow Task"
                  },
                  "valueCodeableConcept": {
                     "coding": [
                        {
                           "system": "http://acme.org",
        ...[snipped for brevity]....

~~~
