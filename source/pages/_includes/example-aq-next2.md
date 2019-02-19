**request**

`POST [base]/Questionnaire/questionnaire-example-adaptive-sampler/$next-question`

**payload**

~~~json
{"resourceType": "QuestionnaireResponse",
      "id": "questionnaireresponse-example-adaptive-sampler",
      "meta": {
        "profile": [
          "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-adap-questionnaireresponse"
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
          //first item group is a display only
          "item": [
          {
            "linkId": "g1",
            // unique url for the Server to identify the adaptive questionnaire question for processing  (figure out what is the next question and/or calculating the score) this could also be a GUID.
            "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1",
            "text": "Header Text",
            "type": "group",
            "required": true,
            "item": [
              {
                "linkId": "g1.d",
                // unique url for the Server to identify the adaptive questionnaire question for processing  (figure out what is the next question and/or calculating the score)
                "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1.d",
                "text": "The Argonaut Questionnaire Sampler is designed to show all the question types that can be used in the Argonaut Questionnaire Project:\n\n1 boolean\n2 decimal\n3 integer\n4 dateDate\n5 dateTime\n6 timeTime\n7 string\n8 textText\n9 urlUrl\n10 choice\n11 open-choice\n12 quantity\n",
                "type": "display",
                "required": true
              }
            ]
          },
          //second item group is a question
          {
            "linkId": "g2",
            "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g2",
            "type": "group",
            "item": [
              {
                "extension": [
                  {
                    "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-ordinalValue",
                    "valueDecimal": 17
                  }
                ],
                "linkId": "g2.q1",
                "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g2.q1",
                "text": "Check the box if the following statement is true.  The average air speed velocity of a laden European swallow is greater than a laden African swallow.",
                "type": "boolean",
                "required": true,
                "repeats": false
              }
            ]
          }
         ]
        }
      ]
      },
      //references the contained Questionnaire
      "questionnaire": {
        "reference": "#questionnaire-example-adaptive-sampler"
      },
      "status": "in-progress",
    ...
    //first group is display only so no scoring or processing by the Server
    "item": [
    {
      "linkId": "g1",
      "item": [
        {
          "linkId": "g1.d"
        }
       ]
      },
      //second group is question-answer pair added by client to be processed by the Server to determine the next question
      {
        "linkId": "g2",
        "item": [
          {
            "linkId": "g2.q1",
            "answer": [
              {
                "valueBoolean": false
              }
            ]
          }
        ]
      }

     ]
    }
}

~~~

**response**

~~~json
{
  "resourceType": "QuestionnaireResponse",
  "id": "questionnaireresponse-example-adaptive-sampler",
  "meta": {
    "profile": [
      "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/argo-adap-questionnaireresponse"
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
      "item": [
      {
        "linkId": "g1",
        // unique url for the Server to identify the adaptive questionnaire question for processing  (figure out what is the next question and/or calculating the score) this could also be a GUID.
        "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1",
        "text": "Header Text",
        "type": "group",
        "required": true,
        "item": [
          {
            "linkId": "g1.d",
            // unique url for the Server to identify the adaptive questionnaire question for processing  (figure out what is the next question and/or calculating the score)
            "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1.d",
            "text": "The Argonaut Questionnaire Sampler is designed to show all the question types that can be used in the Argonaut Questionnaire Project:\n\n1 boolean\n2 decimal\n3 integer\n4 dateDate\n5 dateTime\n6 timeTime\n7 string\n8 textText\n9 urlUrl\n10 choice\n11 open-choice\n12 quantity\n",
            "type": "display",
            "required": true
          }
        ]
      },
      {
        "linkId": "g2",
        "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g2",
        "type": "group",
        "item": [
          {
            "extension": [
              {
                "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-ordinalValue",
                "valueDecimal": 17
              }
            ],
            "linkId": "g2.q1",
            "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g2.q1",
            "text": "Check the box if the following statement is true.  The average air speed velocity of a laden European swallow is greater than a laden African swallow.",
            "type": "boolean",
            "required": true,
            "repeats": false
          }
        ]
      },
      // add third item group as next question
      {
        "linkId": "g3",
        "type": "group",
        "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g3",
        "item": [
          {
            "extension": [
              {
                "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-ordinalValue",
                "valueDecimal": 7
              }
            ],
            "linkId": "g3.q1",
            "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g3",
            "text": "What is the average air speed velocity of a laden swallow in m/sec?",
            "type": "decimal",
            "required": true,
            "repeats": false
          }
        ]
      }
     ]
    }
  ]
  },
  //references the contained Questionnaire
  "questionnaire": {
    "reference": "#questionnaire-example-adaptive-sampler"
  },
  "status": "in-progress",
...
//first group is display only so no scoring or processing by the Server
"item": [
{
  "linkId": "g1",
  "item": [
    {
      "linkId": "g1.d"
    }
   ]
  },
  //second group is question-answer pair so processed by the Server to determine the next question
  {
    "linkId": "g2",
    "item": [
      {
        "linkId": "g2.q1",
        "answer": [
          {
            "valueBoolean": false
          }
        ]
      }
    ]
  }
 ]
}
~~~
