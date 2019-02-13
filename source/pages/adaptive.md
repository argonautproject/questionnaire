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

Argonaut Questionnaire Adaptive forms are dynamic forms that adjust what questions are asked based on previous answers. This is also known as Computerized Adaptive Testing (CAT). The logic to determine the questions are defined external to the Questionnaire resource.[^5]  Responses to questions are iteratively submitted to a FHIR API [FHIR operation] and The form and Questionnaire and QuestionnaireResponse resources are updated on the fly.  A scores based on responses may calculate and recorded separately (e.g., a FHIR [Observation]) or as part of the QuestionnaireResponse

See the [HealthMeasures] website for further background, theory and use cases for adaptive forms.

## Assumptions and Precondition

1. The Adaptive Questionnaire Service is treated as a **“Black Box”**. It contains the sometimes proprietary logic for determination of next question and scoring. Clients make RESTful FHIR transactions on Service using a *FHIR operation* and pass QuestionnaireResponse with *contained* Questionnaire as the payload to capture the data needed between the Client and Service
1. Transactions are Stateless.  The client constructs a record of the transaction which is passed to service and the service adds to record and passed it back to client.  The client and service are free of keeping track of the session and a previously disrupted session can be restored if the session token expires.
1. Client/Form Filler can be a:
  - EHR-S
  - Patient Portal
  - Third Party App
1. The Questionnaire may expire and the form may not be valid. Time limits for completion of a questionnaire or individual question can be defined and the Form Filler can record the start and stop date-times using the [Argonaut Questionnaire Time Limit Extension] and [Argonaut QuestionnaireResponse Response Period Extension].  Note that either Client or Service could determine if the response is within a time limit. How this information modifies the behavior of the Form-filler or interpretation of results is an implementation detail outside of scope of this Implementation Guide.
1. Operationally need to keep the assessment short - e.g., PROMIS forms have up to 12 transactions  (on average 4-12).
1. Calculated Scores can be recorded as [`readOnly`] question and a pre-populated value as an answer.  These items may be marked as 'hidden' using the [Questionnaire Hidden Extension] to direct the Form Filler indicates that the extended item should not be displayed to the user.
  - To assist in calculating scores the standard [Valuset Ordinal Value Extension] and [Questionnaire Ordinal Value Extension] may be used on items. *NOTE: This implementation quide extends the context of the Questionnaire Ordinal Value Extension to elements beyond that defined in the FHIR Specification.*
  - How and when scoring is done is an implementation detail and outside the scope of this guide.
1. There are no constraints on the nesting of item groups and there are several possible items and item groupings including:
    - *a single* question ('what is the capital of Assyria?') or
    - *a single* display  ('Answer these questions three!!') or
    - *a single* item group of *multiple* display + *multiple* questions  ( 'what is you favorite color?', 'what is the capital of Assyria?', 'what is average flight speed of a laden swallow?')
      - or a group containing the question-score pairs when transmitting an individual score for each item.
    - *a single* item group of: *multiple* item groups ('Answer these questions three!!', 'what is you favorite color?', 'what is the capital of Assyria?', 'what is average flight speed of a laden swallow?')


## Workflow Steps

The following sections provide a detailed description of workflow and API guidance for the Adaptive Forms Use Case.

<!-- Discovery of Adaptive Questionnaire --->

### Discovery of Adaptive Questionnaire

The discovery and preview of the service's adaptive questionnaire is out of scope.  It may be done out of band or using the standard [FHIR RESTful search API].


<!--------- INIT ------------>

### Initiate Adaptive Questionnaire

{% include img-narrow.html img="aw-step1.jpg" %}

Launch the adaptive questionnaire by getting first group item (typically the first question) from the Adaptive Questionnaire Service (“Black Box”) by POSTing the operation `$next-question` to the Service's Questionnaire instance endpoint and supplying a QuestionnaireResponse with a *contained* Questionnaire representing only the resource metadata.

{% include img-narrow.html img="slide1.png" %}

The Service updates the contained Questionnaire with the first item and returns the QuestionnaireResponse in the payload.

{% include img-narrow.html img="slide2.png" %}


#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Next Question Operation]**
- **[Argonaut Adaptive QuestionnaireResponse Profile]**

#### Usage
{:.no_toc}

To initiate an  adaptive questionnaire:

`POST [base]/Questionnaire/[id]/$next-question`

{% include examplebutton.html example="example-aq-initiate" b_title="Example: $next-question Operation Initiates Adaptive Questionnaire and Returns First Group Item" %}


<!--------- NEXT Q - 1 ------------>

### Get Next Question

{% include img-narrow.html img="aw-step2.jpg" %}

Client renders/stores/processes the item and gets the next group item by POSTing the operation $next-question to the service Questionnaire instance endpoint and supplying a1 in the QuestionnaireResponse and q1 in the contained Q.

{% include img-narrow.html img="slide3.png" %}

As result of the operation, the Service updates the QuestionnaireResponse and returns it to the Client.

{% include img-narrow.html img="slide4.png" %}

The Service identifies the adaptive questionnaire group item by the contained Questionnaire `definiton` or `linkID` element may add intermediate and cumulative score to the QuestionnaireResponse based on the preceding item(s) and updates the contained Questionnaire with the next question.  This process step is repeated until the adaptive questionnaire is done or the Questionnaire has timed out or another error has occured.


#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Next Question Operation]**
- **[Argonaut Adaptive QuestionnaireResponse Profile]**


#### Usage
{:.no_toc}

To initiate an  adaptive questionnaire:

`POST [base]/Questionnaire/[id]/$next-question`

{% include examplebutton.html example="example-aq-next1" b_title="Example: $next-question Operation Returns Next Question" %}

{% include examplebutton.html example="example-aq-next2" b_title="Example: $next-question Operation Returns Next Question and scoring" %}

<!--------- done ------------>

### Adaptive Questionnaire is Complete

{% include img-narrow.html img="aw-step3.jpg" %}


The Client renders, stores the  question-answer pair and optionally the previous scores and gets the next item group as described above.

{% include img-narrow.html img="slide7.png" %}

When the adaptive questionnaire is  successfully completed, the Service updates the QuestionnaireResponse with intermediate and cumulative scores, updates status to ‘completed’ and returns it to the Client.  The status of ‘completed’ is a signal to the Client that the adaptive Questionnaire is done!

{% include img-narrow.html img="slide8.png" %}

#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Next Question Operation]**
- **[Argonaut Adaptive QuestionnaireResponse Profile]**


#### Usage
{:.no_toc}

To initiate an  adaptive questionnaire:

`POST [base]/Questionnaire/[id]/$next-question`

{% include examplebutton.html example="example-aq-done" b_title="Example: $next-question Operation Returns Completed Adaptive Questionnaire" %}


###  QuestionnaireResponse and Scoring

When the adaptive questionnaire is complete, the client processes the QuestionnaireResponse with a contained Questionnaire based on the questions it was returned by the service.  The client may represent the cumulative or intermediate scores as answers within the QuestionnaireResponse or as separate Observations.  The Client may post the responses to an Answer Bank and perform searches on the QuestionnaireResponse as described in the [Static Forms Use Case].


### Additional Examples and Reference Implementation

Complete examples of the Adaptive QuestionnaireResponse can be found on the [Argonaut Adaptive QuestionnaireResponse Profile] page.  In addition the [Argonaut Questionnaire Test Renderer] is available to simulation the adaptive form workflow.

### Amending and Revising Adaptive Forms

#### End User wishes to go back and revise an answer to Question
{:.no_toc}
For adaptive forms it needs to be emphasized that it is a *stateless* process for both the “black box” service and the client.  That means that the service processes the entire question-answer tree each time from the beginning and the client re-render the informations each time.  So any question-answer pair or calculated results can change until the form is completed.  The black box may mark some question-answer pairs as [`readOnly`] which instruct the client that they can not be subsequently altered.   If not marked as a `readOnly`item any response can be changed at any time by the client and the service will process normally and may remove subsequent question-answers as necessary based on its logic.   The client will be presented with the presented with question-answer pairs and render it anew as well -i.e., it can not retained the previous information.

#### Answer in Error and Needs to be Reentered
{:.no_toc}

For adaptive forms refer to the FHIR API.  An OperationOutcome with the location of the error represented in the ‘expression element’ and a human readable error message should be returned.

#### Technical Error
{:.no_toc}
Technical errors are typically handled by lower level protocols or manual processes. Typically the client or server would simply resubmit the  QuestionnaireResponse.


<br />

---

{% include link-list.md %}
