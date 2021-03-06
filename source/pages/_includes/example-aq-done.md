Note that these json examples are annotated with nonstandard comments and snipped for brevity.

**request**

`POST [base]/Questionnaire/questionnaire-example-adaptive-sampler/$next-question`

**payload**

~~~
{"resourceType": "QuestionnaireResponse",
    "id": "questionnaireresponse-example-adaptive-sampler",
    "meta": {
      "profile": [
        "http://fhir.org/guides/argonaut/questionnaire/StructureDefinition/argo-adap-questionnaireresponse"
      ],
    // contained Questionnaire
    "contained": [
      {
        "resourceType": "Questionnaire",
        "id": "questionnaire-example-adaptive-sampler",
        "meta": {
          "profile": [
            "http://fhir.org/guides/argonaut/questionnaire/StructureDefinition/argo-questionnaire"
          ]
        },
        //the 'url' element identifies the adaptive questionnaire - the set of questions for a particular adaptive questionnaire
        "url": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler",
        "title": "Argonaut Questionnaire Sampler",
        "status": "draft",
        ...[snipped for brevity]....
        "item": [
        {
          "linkId": "g1",
          //COMMENT - unique url for the Server to identify the adaptive questionnaire question for processing  (figure out what is the next question and/or calculating the score) this could also be a GUID.
          "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1",
          "text": "Header Text",
          "type": "group",
          "required": true,
          "item": [
            {
              "linkId": "g1.d",
              //COMMENT - unique url for the Server to identify the adaptive questionnaire question for processing  (figure out what is the next question and/or calculating the score)
              "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1.d",
              "text": "The Argonaut Questionnaire Sampler is designed to show all the question types that can be used in the Argonaut Questionnaire Project:\n\n1 boolean\n2 decimal\n3 integer\n4 dateDate\n5 dateTime\n6 timeTime\n7 string\n8 textText\n9 urlUrl\n10 choice\n11 open-choice\n12 quantity\n",
              "type": "display",
              "required": true
            }
          ]
        },
        {
          "linkId": "g2",
          "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g2",
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
              "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g2.q1",
              "text": "Check the box if the following statement is true.  The average air speed velocity of a laden European swallow is greater than a laden African swallow.",
              "type": "boolean",
              "required": true,
              "repeats": false
            }
          ]
        },
        //COMMENT - third item group is the current question
        {
          "linkId": "g3",
          "type": "group",
          "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g3",
          "item": [
            {
              "extension": [
                {
                  "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-ordinalValue",
                  "valueDecimal": 7
                }
              ],
              "linkId": "g3.q1",
              "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g3",
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
    //COMMENT -references the contained Questionnaire
    "questionnaire": {
      "reference": "#questionnaire-example-adaptive-sampler"
    },
    "status": "in-progress",
  ...[snipped for brevity]....
  //COMMENT -first group is display only so no scoring or processing by the Server
  "item": [
  {
    "linkId": "g1",
    "item": [
      {
        "linkId": "g1.d"
      }
     ]
    },
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
    },
    },
    //COMMENT -third group question-answer pair updated by client to be processed by the Server to determine the next question and the score
    {
      "linkId": "g3",
      "item": [
        {
          "linkId": "g3.q1",
          "answer": [
            {
              "valueDecimal": 12.38
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

~~~
{
  "resourceType": "QuestionnaireResponse",
  "id": "questionnaireresponse-example-adaptive-sampler",
  "meta": {
    "profile": [
      "http://fhir.org/guides/argonaut/questionnaire/StructureDefinition/argo-adap-questionnaireresponse"
    ],
  //COMMENT - contained Questionnaire
  "contained": [
    {
      "resourceType": "Questionnaire",
      "id": "questionnaire-example-adaptive-sampler",
      "meta": {
        "profile": [
          "http://fhir.org/guides/argonaut/questionnaire/StructureDefinition/argo-questionnaire"
        ]
      },
      //COMMENT -the 'url' element identifies the adaptive questionnaire - the set of questions for a particular adaptive questionnaire
      "url": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler",
      "title": "Argonaut Questionnaire Sampler",
      "status": "draft",
      ...[snipped for brevity]....
      "item": [
      {
        "linkId": "g1",
        //COMMENT - unique url for the Server to identify the adaptive questionnaire question for processing  (figure out what is the next question and/or calculating the score) this could also be a GUID.
        "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1",
        "text": "Header Text",
        "type": "group",
        "required": true,
        "item": [
          {
            "linkId": "g1.d",
            //COMMENT - unique url for the Server to identify the adaptive questionnaire question for processing  (figure out what is the next question and/or calculating the score)
            "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1.d",
            "text": "The Argonaut Questionnaire Sampler is designed to show all the question types that can be used in the Argonaut Questionnaire Project:\n\n1 boolean\n2 decimal\n3 integer\n4 dateDate\n5 dateTime\n6 timeTime\n7 string\n8 textText\n9 urlUrl\n10 choice\n11 open-choice\n12 quantity\n",
            "type": "display",
            "required": true
          }
        ]
      },
      {
        "linkId": "g2",
        "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g2",
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
            "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g2.q1",
            "text": "Check the box if the following statement is true.  The average air speed velocity of a laden European swallow is greater than a laden African swallow.",
            "type": "boolean",
            "required": true,
            "repeats": false
          }
        ]
      },
      //COMMENT - third item group is the current question
      {
        "linkId": "g3",
        "type": "group",
        "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g3",
        "item": [
          {
            "extension": [
              {
                "url": "http://hl7.org/fhir/StructureDefinition/questionnaire-ordinalValue",
                "valueDecimal": 7
              }
            ],
            "linkId": "g3.q1",
            "definition": "http://fhir.org/guides/argonaut/questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g3",
            "text": "What is the average air speed velocity of a laden swallow in m/sec?",
            "type": "decimal",
            "required": true,
            "repeats": false
          }
        ]
      },
      //COMMENT - add a readOnly hidden score question to a final item group.
      {
        "linkId": "g4",
        "type": "group",
        "item": [
          {
            "extension": [
              {
                "url": "http://fhir.org/guides/argonaut/questionnaire/StructureDefinition/extension-hidden",
                "valueBoolean": true
              }
            ],
            "linkId": "g4.q1",
            "text": "The total score is:",
            "type": ,
            "required": true,
            "repeats": false,
            "readOnly": true
            }
          }
        ]
      }
     ]
    }
  ]
  },
  //COMMENT -references the contained Questionnaire
  "questionnaire": {
    "reference": "#questionnaire-example-adaptive-sampler"
  },
  //COMMENT - status of ‘complete’ is a signal to the Client that the adaptive Questionnaire is done!  
  "status": "complete",
...[snipped for brevity]....
"item": [
{
  "linkId": "g1",
  "item": [
    {
      "linkId": "g1.d"
    }
   ]
  },
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
  },
  },
  {
    "linkId": "g3",
    "item": [
      {
        "linkId": "g3.q1",
        "answer": [
          {
            "valueDecimal": 12.38
          }
        ]
      }
    ]
  },
  //COMMENT - add a readOnly hidden score question to a final item group.
  {
    "linkId": "g4",
    "item": [
      {
        "linkId": "g4.q1",
        "answer": [
          {
            "valueQuantity": {
              "value" : 24,
              "unit" : "points",
              "system" : "http://unitsofmeasure.org",
              "code" : "\{score\}"
            }
          }
        ]
      }
    ]
  }
 ]
}
~~~
