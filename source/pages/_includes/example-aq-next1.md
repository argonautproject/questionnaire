**request**

`POST [base]/Questionnaire/questionnaire-example-adaptive-sampler/$next-q`

**payload**

~~~
{"resourceType": "QuestionnaireResponse",
      "id": "questionnaireresponse-example-adaptive-sampler",
      "meta": {
        "profile": [
          "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/aqr"
        ],
      // contained Questionnaire
      "contained": [
        {
          "resourceType": "Questionnaire",
          "id": "questionnaire-example-adaptive-sampler",
          "meta": {
            "profile": [
              "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/q"
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
            "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1"
            "text": "Header Text",
            "type": "group",
            "required": true,
            "item": [
              {
                "linkId": "g1.d",
                // unique url for the Server to identify the adaptive questionnaire question for processing  (figure out what is the next question and/or calculating the score)
                "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1.d"
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
      "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/aqr"
    ],
  // contained Questionnaire
  "contained": [
    {
      "resourceType": "Questionnaire",
      "id": "questionnaire-example-adaptive-sampler",
      "meta": {
        "profile": [
          "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/q"
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
        "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1"
        "text": "Header Text",
        "type": "group",
        "required": true,
        "item": [
          {
            "linkId": "g1.d",
            // unique url for the Server to identify the adaptive questionnaire question for processing  (figure out what is the next question and/or calculating the score)
            "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g1.d"
            "text": "The Argonaut Questionnaire Sampler is designed to show all the question types that can be used in the Argonaut Questionnaire Project:\n\n1 boolean\n2 decimal\n3 integer\n4 dateDate\n5 dateTime\n6 timeTime\n7 string\n8 textText\n9 urlUrl\n10 choice\n11 open-choice\n12 quantity\n",
            "type": "display",
            "required": true
          }
        ]
      },
      //add next item group as next question
      {
        "linkId": "g2",
        "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g2"
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
            "definition": "http://fhir.org/guides/argonaut-questionnaire/Questionnaire/questionnaire-example-adaptive-sampler#g2.q1"
            "text": "Check the box if the following statement is true.  The average air speed velocity of a laden European swallow is greater than a laden African swallow.",
            "type": "boolean",
            "required": true,
            "repeats": false
          }
        ]
      },

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
  }
 ]
}
~~~
