# fhir-templates.py

headers = {'Content-Type': 'application/fhir+json', 'Accept': 'application/fhir+json'}


qr_templ = {"resourceType":"QuestionnaireResponse","id":"test","meta":{"profile":["http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-questionnaireresponse"]},"text":{"status": "generated","div":"<div xmlns=\"http://www.w3.org/1999/xhtml\"><h3>Response Summary</h3></div>"},"identifier":{"value":"test"},"questionnaire":{"reference":"Questionnaire/questionnaire-example-housing"},"status":"completed","subject":{"reference":"Patient/subject1"},"context":{"reference":"Encounter/encounter1"},"authored":"2018-05-21","author":{"reference":"Practitioner/prov-admin1"},"source":{"reference":"Patient/subject1"}}

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
