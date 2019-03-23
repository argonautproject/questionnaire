

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?context-code=task&value=example

User-Agent: python-requests/2.20.0
Accept: application/fhir+json
Content-Type: application/fhir+json
[other headers]
~~~

**Response**

~~~
Response Code: 200 (OK)
Content-Type: application/fhir+json; charset=utf-8
Content-Location: http://sqlonfhir-stu3.azurewebsites.net/fhir/Bundle/urn:uuid:f43f23115d954cd28716556d7bb26287
[other headers]


{
    "resourceType": "Bundle",
    "id": "urn:uuid:f43f23115d954cd28716556d7bb26287",
    "meta": {
        "lastUpdated": "2019-02-27T02:15:12.686+00:00"
    },
    "type": "searchset",
    "total": 67,
    "link": [
        {
            "relation": "self",
            "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire??context-code=task&value=example&_snapshot=636868305126868471"
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
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><b>Argonaut Questionnaire Sampler</b><hr /><span style=\"color: gray;\">Publisher:</span> Argonaut Project\r\n</div>"
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
                                    "code": "example",
                                    "display": "Example of Use"
                                }
                            ]
                        }
                    }
                ],

        ...[snipped for brevity]....

~~~
