

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse?patient.gender=male&patient.birthdate=le1975

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
   "id": "urn:uuid:1e79af295b464c7a95e037ed445bd03b",
   "meta": {
      "lastUpdated": "2019-02-13T10:28:30.82+00:00"
   },
   "type": "searchset",
   "total": 25,
   "link": [
        ...[snipped for brevity]....
   ],
   "entry": [
      {
         "fullUrl": "http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse/questionnaireresponse-example-patient-search",
         },
         "contained": [
            {
               "id": "deid-p",
               "extension": [
                  {
                     "extension": [
                        {
                           "url": "text",
                           "valueString": "Asian"
                        },
                        {
                           "url": "ombCategory",
                           "valueCoding": {
                              "code": "asian",
                              "display": "Asian",
                              "system": "urn:oid:2.16.840.1.113883.6.238"
                           }
                        }
                     ],
                     "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"
                  }
               ],
               "name" : [
                  {
                    "_family" : {
                      "extension" : [
                        {
                          "url" : "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                          "valueCode" : "masked"
                        }
                      ]
                    },
                    "_given" : [
                      {
                        "extension" : [
                          {
                            "url" : "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode" : "masked"
                          }
                        ]
                      }
                    ]
                  }
                ],
               "address": [
                  {
                     "postalCode": "945"
                  }
               ],
               "birthDate": "1969",
               "gender": "male",
               "resourceType": "Patient"
            }
         ],
        ...[snipped for brevity]....
         "questionnaire": {
            "reference": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-sampler"
         },
         "source": {
            "reference": "Patient/subject1"
         },
         "status": "completed",
         "subject": {
            "reference": "#deid-p"
         },
         "resourceType": "QuestionnaireResponse"
      }

~~~
