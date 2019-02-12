**request**

`POST [base]/Questionnaire/questionnaire-example-adaptive-sampler/$next-q`

**payload**

~~~
 {
    "resourceType": "QuestionnaireResponse",
    "id": "questionnaireresponse-example-adaptive-sampler",
    "meta": {
      "profile": [
        "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-adaptive-questionnaire"
      ],
    // contained Questionnaire
    "contained": [
      {
        "resourceType": "Questionnaire",
        "id": "questionnaire-example-adaptive-sampler",
        "meta": {
          "profile": [
            "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-questionnaire"
          ]
        },
        "url": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler",
        "title": "Argonaut Questionnaire Sampler",
        "status": "draft",
        //no items since initiating the adaptive questionnaire
      ...
      }
    ]
    },
    //references the contained Questionnaire
    "questionnaire": {
      "reference": "#questionnaire-example-adaptive-sampler"
    },
    "status": "in-progress",
   ...
   //no items since is just getting started
   }
  }
~~~

**response**

~~~
{
  "resourceType": "QuestionnaireResponse",
  "id": "questionnaireresponse-example-adaptive-sampler",
  "meta": {
    "profile": [
      "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-adaptive-questionnaire"
    ],
  // contained Questionnaire
  "contained": [
    {
      "resourceType": "Questionnaire",
      "id": "questionnaire-example-adaptive-sampler",
      "meta": {
        "profile": [
          "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-questionnaire"
        ]
      },
      //the 'url' element identifies the adaptive questionnaire - the set of questions for a particular adaptive questionnaire
      "url": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler",
      "title": "Argonaut Questionnaire Sampler",
      "status": "draft",
      ...
      //add first item group which is a display only not a questions
      "item": [
      {
        "linkId": "g1",
        // unique url for the Server to identify the adaptive questionnaire question for processing (figure out what is the next question and/or calculating the score) this could also be a GUID
        "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1"
        "text": "Header Text",
        "type": "group",
        "required": true,
        "item": [
          {
            "linkId": "g1.d",
            // unique url for the Server to identify the adaptive questionnaire question for processing  (figure out what is the next question and/or calculating the score)
            "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1.d1"
            "text": "The Argonaut Questionnaire Sampler is designed to show all the question types that can be used in the Argonaut Questionnaire Project:\n\n1 boolean\n2 decimal\n3 integer\n4 dateDate\n5 dateTime\n6 timeTime\n7 string\n8 textText\n9 urlUrl\n10 choice\n11 open-choice\n12 quantity\n",
            "type": "display",
            "required": true
          }
        ]
      }
     ]
    }
  ]
  },
  //reference to contained Questionnaire
  "questionnaire": {
    "reference": "#questionnaire-example-adaptive-sampler"
  },
  "status": "in-progress",
...
//no items since is just getting started
}
~~~
