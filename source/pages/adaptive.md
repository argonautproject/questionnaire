---
title: Adaptive Forms
layout: default
active: guidance
topofpage: true
---

{:.no_toc}

<!-- TOC  the css styling for this is \pages\assets\css\project.css under 'markdown-toc'-->

* Do not remove this line (it will not be displayed)
{:toc}

## Introduction

The Argonaut Questionnaire Implementation Guide defines a series of interactions which cover the basic workflow for the creation, discovery and retrieval of "computer adaptive forms" using FHIR Questionnaire and QuestionnaireResponse and the FHIR API.

- Dynamic forms
- Adjust what questions are asked based on previous answers
- Logic defined external to Questionnaire
- Iteratively submit response to API (FHIR operations)
- Locally Questionnaire/QuestionnaireResponse updated on the fly
- Record total score as an Observation

<!--
Demonstration by Raheel Sayeed (Smart on FHIR Post-Doc)
EASIPRO: Northwestern, Harvard, USC, working on integration of PROMIS into the healthcare system.
-->

## Example Scenario

This simple scenario serves as an effective means to describe the Argonaut Questionnaire basic workflow and API

~~~ text
 ...todo...
~~~

## Workflow Steps


initial operation --> subsequent operation --> create QuestionnaireResponse with contained Questionnaire.  

Use Parameters resource to capture the data needed between the Client and Server

Assume each Q SHALL only represent:
- *a single* question ('what is the capital of Assyria?')
- *a single* display  ('Answer these questions three!!')
- *a single* group of:
  - 1+ question (e.g., age, sex, zip code, occupation to establish demographics)
  - 1 display + 1+ question  ('Answer these questions three!!', 'what is you favorite color?', 'what is the capital of Assyria?', 'what is average flight speed of a laden swallow?')

Argonaut Next Question Operation:


name $next-q

id argonaut-next-q

name Argonaut Next Question Operation

parameters:

in/out:

qa-pairs: 0..*  The previous completed question-answer pairs. If there is no group then the operation is initiating an adaptive-q and the first question/group is returned by the service.

  sequence: 1..1 posInteger The sequence number of the of the question/group answer pair.  The sequence of questions is important for scoring and for determining the next question.

  url: 1..1 url The url that is associated with the previous Questionnaire.
  answer[x]: 0..1 string|Coding|... The answer associated with the question identified in the q-id parameter.

  score: 0..1 Quantity The calculated score that was returned by the service for the question/group.  This value is used only for prior questions and returned to the service in a stateless model.  When an input it is empty for the current qa pair.  Cumulative/Final scores use the cum-score parameter

out:

  cum-score: 0..1 Quantity The cumulative/total score for the adaptive questionnaire.  Individual scores for each question use the q-score parameter

  q: 0..1 Resource The Argo-Adaptive-Questionnaire profile of the Questionnaire resource representing the next question/group.  If this parameter is not returned, the adaptive questionnaire is complete.

<!--------- INIT ------------>

### Initiate Adaptive Questionnaire

Launch the adaptive questionnaire by getting first question at its FHIR endpoint - just a regular FHIR RESTful GET to the introductory question.  This may be only a display

**request**

`GET ../Questionnaire/adaptive-first-question`

**response**

~~~
{
  "resourceType": "Questionnaire",
  "id": "first-question-example",
  "url": "https\://acme.org/questionnaire/1",
  ...
  //assuming a single question item for Q1//
  "item":{
  ...
  "type":"choice"
  "text":"blah1"
  ...
  }
~~~

<!--------- NEXT Q - 1 ------------>

### Get Next Question

Client ...renders, stores question 1, answer 1... and gets next question using by POSTing the operation $next-q to the service Questionnaire endpoint and supplying the parameters from the prior question

**request**

`POST ../Questionnaire/$next-q`

**payload**

~~~
  {
    "resourceType": "Parameters",
    "id": "next-question-example",
    "parameter": [
      {
        "name": "qa-pairs",
        "part": [
          {
           // first question  = Q-1 answered "foo", with no score returned yet so no score is available.
            "sequence": "1",
            "url": "https\://acme.org/questionnaire/1",
            "answerString": "foo",
          }
        ]
      }
    ]
  }
~~~

**response**

~~~
{
  "resourceType": "Parameters",
  "id": "next-question-example",
  "parameter": [
    {
      "name": "qa-pairs",
      "part": [
        {
         // first question  = Q-1 answered "foo", with no score returned yet so no score is available.
          "sequence": "1",
          "url": "https\://acme.org/questionnaire/1",
          "answerString": "foo",
          "score": {
              "value" : 17,
              "unit" : "points"}
              }
        }
      ],
      "cum-score": 17,
      'q': {
        "resourceType": "Questionnaire",
        "id": "first-question-example",
        "url": "https\://acme.org/questionnaire/4",
        ...
        //assuming a single question item for Q4//
        "item":{
        ...
        "type":"choice"
        "text":"blah4"
        ...
        }

    }
  ]
}
~~~

<!--------- NEXT Q - 2 ------------>

### Get Next Question

Client renders, stores question 4, answer 2, score 1 and
gets next question using by POSTing the operation $next-q to the service Questionnaire endpoint and supplying the parameters from the prior question

**request**

`POST ../Questionnaire/$next-q`

**payload**

~~~
    {
      "resourceType": "Parameters",
      "id": "next-question-example",
      "parameter": [
        {
          "name": "qa-group",
          "part": [
            {
             // first question  = Q-1 answered "foo", with an intermediate score of 17 returned
              "sequence": "1",
              "url": "https\://acme.org/questionnaire/1",
              "answerString": "foo",
              "score": {
                  "value" : 17,
                  "unit" : "points"}
                  },
              {
              // second question  = Q-4 answered "bar", with an intermediate score of 11 returned
              "sequence": "2",
              "q-url": "https\://acme.org/questionnaire/4",
              "answerString": "bar"
            }
          ]
        }
      ]
    }
~~~

**response**

    {
      "resourceType": "Parameters",
      "id": "next-question-example",
      "parameter": [
        {
          "name": "qa-group",
          "part": [
            {
             // first question  = Q-1 answered "foo", with an intermediate score of 17 returned
              "sequence": "1",
              "url": "https\://acme.org/questionnaire/1",
              "answerString": "foo",
              "score": {
                  "value" : 17,
                  "unit" : "points"}
                  }
                },
              {
              // second question  = Q-4 answered "bar", with an intermediate score of 11 returned
              "sequence": "2",
              "q-url": "https\://acme.org/questionnaire/4",
              "answerString": "bar",
              "score": {
                  "value" : 11,
                  "unit" : "points"}
                  }
                }
          ],
          "cum-score": 28,
          'q': {
            "resourceType": "Questionnaire",
            "id": "first-question-example",
            "url": "https\://acme.org/questionnaire/9",
            ...
            //assuming a single question item for Q9//
            "item":{
            ...
            "type":"choice",
            "text":"blah9"
            ...
            }
        }
      ]
    }

    client
    ...render, store question 4, answer 2, score 1...

### Finished

Get next question using by POSTing the operation $next-q to the service Questionnaire endpoint and supplying the parameters from the prior question

**request**

`POST ../Questionnaire/$next-q`

**payload**

~~~
    {
      "resourceType": "Parameters",
      "id": "next-question-example",
      "parameter": [
        {
          "name": "qa-group",
          "part": [
            {
             // first question  = Q-1 answered "foo", with an intermediate score of 17 returned
              "sequence": "1",
              "url": "https\://acme.org/questionnaire/1",
              "answerString": "foo",
              "score": {
                  "value" : 17,
                  "unit" : "points"}
                  },
              // second question  = Q-4 answered "bar", with an intermediate score of 11 returned
              "sequence": "2",
              "q-url": "https\://acme.org/questionnaire/4",
              "answerString": "bar",
              "q-score": {
                  "value" : 11,
                  "unit" : "points"}
                  },
              // third question  = Q-9 answered "baz", with no intermediate score since this is the current qa
              "sequence": "3",
              "q-url": "https\://acme.org/questionnaire/9",
              "answerString": "baz"
              }
            ]
          }
        ]
      }
~~~

**response**

~~~
{
  "resourceType": "Parameters",
  "id": "next-question-example",
  "parameter": [
    {
      "name": "qa-group",
      "part": [
        {
         // first question  = Q-1 answered "foo", with an intermediate score of 17 returned
          "sequence": "1",
          "url": "https\://acme.org/questionnaire/1",
          "answerString": "foo",
          "score": {
              "value" : 17,
              "unit" : "points"}
              },
          // second question  = Q-4 answered "bar", with an intermediate score of 11 returned
          "sequence": "2",
          "q-url": "https\://acme.org/questionnaire/4",
          "answerString": "bar",
          "q-score": {
              "value" : 11,
              "unit" : "points"}
              },
          // third question  = Q-9 answered "baz", with no intermediate score since this is the current qa
          "sequence": "3",
          "q-url": "https\://acme.org/questionnaire/9",
          "answerString": "baz",
          "q-score": {
              "value" : 3,
              "unit" : "points"}
              },

          }
        ],
        "cum-score": 31
        //When the adaptive questionnaire is complete the service returns a payload that does not have a q parameter which signals to the client that the Questionnaire is complete.
      }
    ]
  }
~~~

###  QuestionnaireResponse and Scoring

When the adaptive questionnaire is complete the service returns a payload that does not have a q parameter which signals to the client that the Questionnaire is complete.

The client creates a QuestionnaireResponse with a contained Questionnaire based on the questions it was returned by the service.
The client may also create an Observation to represent the cumulative or intermediate scores.


---

{% include link-list.md %}
