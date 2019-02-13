

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?title=Argonaut+Questionnaire+Sampler&version=3.0.0

User-Agent: python-requests/2.20.0
Accept: application/fhir+json
Content-Type: application/fhir+json
[other headers]
~~~

**Response**

~~~
Response Code: 200 (OK)
Content-Type: application/fhir+json; charset=utf-8
Content-Location: http://sqlonfhir-stu3.azurewebsites.net/fhir/Bundle/urn:uuid:b5e40cf4865f46b3a00524b3dac8e364
[other headers]


{
   "resourceType": "Bundle",
   "id": "urn:uuid:b5e40cf4865f46b3a00524b3dac8e364",
   "meta": {
      "lastUpdated": "2019-02-13T08:38:59.164+00:00"
   },
   "type": "searchset",
   "total": 1,
   "link": [
      {
         "relation": "self",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?title=Argonaut+Questionnaire+Sampler&version=3.0.0&_snapshot=636856439391647462"
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
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\r\n\t<b>Argonaut Questionnaire Sampler</b>\r\n\t<hr/>\r\n\t\t<span style=\"color: gray;\">Publisher:</span> Argonaut Project\r\n</div>\r\n"
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
        ...[snipped for brevity]....

~~~
