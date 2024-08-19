# fhir-templates.py

fhir_headers = {
           'Content-Type': 'application/fhir+json',
           'Accept': 'application/fhir+json'
           }

json_headers = {
           'Content-Type': 'application/json',
           'Accept': 'application/json'
           }



q_ref = "my_ref"  #placeholder for dict value
# dict
task_patch= [
    {
        "op": "add",
        "path": "/output",
        "value": [
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/uv/sdc/CodeSystem/temp",
                            "code": "questionnaire-response"
                        }
                    ]
                },
                "valueReference": {
                    "reference": q_ref
                }
            }
        ]
    }
]

qr_templ = {
    "resourceType": "QuestionnaireResponse",
    "id": "test",
    "meta": {
        "profile": [
            "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-questionnaireresponse"
        ]
    },
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><h3>Response Summary</h3></div>"
    },
    "identifier": {
        "value": "test"
    },
    "questionnaire": "questionnaire-example-canonical",
    "status": "completed",
    "subject": {
        "reference": "Patient/subject1"
    },
    "authored": "2018-05-21",
    "author": {
        "reference": "Practitioner/prov-admin1"
    }
}
def aqr_templ(q_url, q_title):
    return {
          "resourceType": "QuestionnaireResponse",
          "id": "test",
          "meta": {
            "profile": [
              "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-adap-questionnaireresponse"
            ]
          },
          "text": {
            "status": "generated",
            "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><h3>Response Summary</h3></div>"
          },
          "identifier": {
            "value": "test"
          },
          "questionnaire": {
            "reference": "Questionnaire/questionnaire-example-housing"
          },
          "status": "in-progress",
          "subject": {
            "reference": "Patient/subject1"
          },
          "context": {
            "reference": "Encounter/encounter1"
          },
          "authored": "2018-05-21",
          "author": {
            "reference": "Practitioner/prov-admin1"
          },
          "source": {
            "reference": "Patient/subject1"
          },
          "contained": [
            {
              "resourceType": "Questionnaire",
              "meta": {
                "profile": [
                  "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-adaptive-questionnaire"
                ]
              },
              "status": "active",
              "url": "{url}".format(url=q_url),
              "title": 'Contained Adaptive {title}'.format(title=q_title)
            }
          ]
        }


if __name__ == "__main__":
    print(aqr_templ('foo', 'bar'))
