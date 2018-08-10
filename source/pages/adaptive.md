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

The Argonaut Questionnaire Implementation Guide defines a series of interactions which cover the basic workflow for the creation, discovery and retrieval of "**computer adaptive forms**" using FHIR Questionnaire and QuestionnaireResponse and the FHIR API.

- Dynamic forms
- Adjust what questions are asked based on previous answers
- Logic defined external to Questionnaire
- Iteratively submit response to API (FHIR operations)
- Locally Questionnaire/QuestionnaireResponse updated on the fly
- Record total score as an Observation or a part of QuestionnaireResponse **Discuss**

<!--
Demonstration by Raheel Sayeed (Smart on FHIR Post-Doc)
EASIPRO: Northwestern, Harvard, USC, working on integration of PROMIS into the healthcare system.
-->

## Example Scenario

This simple scenario serves as an effective means to describe the Argonaut Questionnaire basic workflow and API

~~~ text
 ...todo...
~~~

## Assumptions and Precondition

- Client(Form Filler)
  - EHR-S
  - Patient Portal (Smart) App
  - Third Party (Smart) App too.
- Adaptive Questionnaire Service is a “Black Box”:
  - Contains logic for determination of next question and scoring
- Transactions are Stateless:
  - Client constructs a record of transaction which is passed to Server
  - Server adds to record and passed back to Client
  - Client and Server free of keeping track of session
  - A Previously disrupted session can be restored if session token expires.
- Client makes RESTful FHIR transactions on Server using a *FHIR operation*
- Use QuestionnaireResponse with contained Questionnaire as Parameters to capture the data needed between the Client and Server
- If Questionnaire timed out
   - Response can change over time and the Form is not valid
   - the whole session needs to be restarted
   - timing extensions - duration/time-limit?
      - either Client or Server could validate if within time limit
      - (OperationOutcome defined error code) **Discusse**
- Use QuestionnaireResponse with contained Questionnaire as Parameters to capture the data needed between the Client and Server
- Operationally need to keep assessment short.
  - e.g.,PROMIS up to 12 transactions  (on average 4-12))
- Calculated Scores as `readOnly` questions with `initial.valueQuantity` that cannot be changed
  - can be marked as hidden using the questionnair-hidden extension to prevent end user from viewing.

## Open issues for discussion

1. Using QuestionnaireResponse with contained Questionnaire as the "container" to pass information back and forth [7](https://github.com/argonautproject/questionnaire/issues/7)
    - other option would be simpler list of Paramters but the client will still have to build the QuestionnaireResponse with contained Questionnaire.
    - (complexity is just shifted around
1. limit the structural complexity (i.e. nesting of group items) of the contained Questionnaire? [8](https://github.com/argonautproject/questionnaire/issues/8)
    - *each* contained Questionnaire.item could be a:
        - *a single* question ('what is the capital of Assyria?') or
        - *a single* display  ('Answer these questions three!!') or
        - *a single* item group of *multiple* display + *multiple* questions  ( 'what is you favorite color?', 'what is the capital of Assyria?', 'what is average flight speed of a laden swallow?')
        - *a single* item group of: *multiple* item groups ('Answer these questions three!!', 'what is you favorite color?', 'what is the capital of Assyria?', 'what is average flight speed of a laden swallow?')
    -  What is the Service going to send in most cases?
       - We are assuming the adaptive questionnaire are going to be rather short so is this complexity warranted.
       - On the other hand other projects (SDC and ONC PROs project) are planning to build on this guidance so may be better to not overly constrain.
1.  What scoring capability is needed only at end or after each question? [9](https://github.com/argonautproject/questionnaire/issues/9)
    - cumulative(total score) score only at end or after each question ?
    - score for each q-a pair ?
    - what guidance if any should be given on how to store score?
      - as Observation
      - as question-answer pair  ( how is shown below )
      - both
1. Discovery of Adaptive Questionnaire? [10](https://github.com/argonautproject/questionnaire/issues/10)
   - see section below

## Workflow Steps

The following sections provide a detailed description of workflow and API guidance for the Adaptive Forms Use Case.


{% include img.html img="adaptive-workflow-steps.jpg" caption="Data Requirements Operation" %}


<!-- Discovery of Adaptive Questionnaire --->

### Adaptive Questionnaire Discovery

The discovery and preview of the service's adaptive questionnaire is out of scope.  It may be done out of band or using the standard [FHIR RESTful search API]. ( todo - discuss )


<!--------- INIT ------------>

### Initiate Adaptive Questionnaire

{% include img-narrow.html img="aw-step1.jpg" %}

Launch the adaptive questionnaire by getting first group item (either a display, question(s), or group + questions ) from the Server by POSTing the operation $next-q to the Server's Questionnaire instance endpoint and supplying a QuestionnaireResponse with a *contained** Questionnaire representing only the resource metadata.  The Server updates the contained Questionnaire with the first item and returns the QuestionnaireResponse in the payload.

#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Next Question Operation]**
- **[Argonaut Adaptive QR Profile]**


#### Usage
{:.no_toc}

To initiate an  adaptive questionnaire:

`POST [base]/QuestionnaireResponse/[id]/$next-q`

{% include examplebutton.html example="example-aq-initiate" b_title="Example: $next-q Operation Initiates Adaptive Questionnaire and Returns First Group Item" %}


<!--------- NEXT Q - 1 ------------>

### Get Next Question

{% include img-narrow.html img="aw-step2.jpg" %}

Client renders/stores/processes the item and gets the next group item by POSTing the operation $next-q to the service Questionnaire instance endpoint and supplying a1 in the QR and q1 in the contained Q.  As result of the operation, the Server updates the QR and returns it to the Client.

The Server identifies the adaptive questionnaire group item by the contained Questionnaire `definiton` element may add intermediate and cumulative score to the QR based on the preceding item(s) and updates the contained Questionnaire with the next question.  This process step is repeated until the adaptive questionnaire is done or the Questionaire has timed out (footnote?) or another error has occured.


#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Next Question Operation]**
- **[Argonaut Adaptive QR Profile]**


#### Usage
{:.no_toc}

To initiate an  adaptive questionnaire:

`POST [base]/QuestionnaireResponse/[id]/$next-q`

{% include examplebutton.html example="example-aq-next1" b_title="Example: $next-q Operation Returns Next Question" %}

{% include examplebutton.html example="example-aq-next2" b_title="Example: $next-q Operation Returns Next Question and scoring" %}

<!--------- done ------------>

### Adaptive Questionnaire is Complete

{% include img-narrow.html img="aw-step3.jpg" %}


The Client renders, stores the  question-answer pair and optionally the previous scores and gets the next item group as described above.  When the adaptive questionnaire is  successfully completed, the Server updates the QR with intermediate and cumulative scores, updates status to ‘complete’ and returns it to the Client.  The status of ‘complete’ is a signal to the Client that the adaptive Questionnaire is done!

#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Next Question Operation]**
- **[Argonaut Adaptive QR Profile]**


#### Usage
{:.no_toc}

To initiate an  adaptive questionnaire:

`POST [base]/QuestionnaireResponse/[id]/$next-q`

{% include examplebutton.html example="example-aq-done" b_title="Example: $next-q Operation Returns Completed Adaptive Questionnaire" %}


###  QuestionnaireResponse and Scoring

When the adaptive questionnaire is complete, the client processes the QuestionnaireResponse with a contained Questionnaire based on the questions it was returned by the service.  The client may represent the cumulative or intermediate scores as answers within the QuestionnaireResponse or as separate Observations.

<br />

---

{% include link-list.md %}
