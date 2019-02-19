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

The Argonaut Questionnaire Implementation Guide defines a series of interactions which cover the basic workflow for the creation, discovery and retrieval of "**computer adaptive forms**" using FHIR Questionnaire and QuestionnaireResponse andbutton
 the FHIR API.  The reader is encouraged to familiarize herself with the capabilities of the Questionnaire and QuestionnaireResponse Response resources by reviewing the guidance given in the FHIR specification and the guidance in [Static Forms Use Case].

Argonaut Questionnaire Adaptive forms are dynamic forms that adjust what questions are asked based on previous answers. This is also known as Computerized Adaptive Testing (CAT). The logic to determine the questions are defined external to the Questionnaire resource.[^5]   Responses to questions are iteratively submitted to a FHIR API [FHIR operation] and the contained Questionnaire and QuestionnaireResponse resources are updated on the fly.  A score based on responses may calculate and recorded separately (e.g., a FHIR [Observation]) or as part of the QuestionnaireResponse

See the [HealthMeasures] website for further background, theory and use cases for adaptive forms.

## Assumptions and Precondition

1. The Adaptive Questionnaire Service is treated as a **“Black Box”**. It contains the logic for determination of next question and scoring. Form Fillers make RESTful FHIR transactions on Service using a *FHIR operation* and pass QuestionnaireResponse with [contained] Questionnaire as the payload to capture the data needed between the Form Filler and Service
1. Transactions are Stateless.  The Form Filler constructs a record of the transaction which is passed to service and the service adds to record and passed it back to Form Filler.  The Form Filler and service are free of keeping track of the session and a previously disrupted session can be restored if the session token expires.
1. The Questionnaire may expire and the form may not be valid. Time limits for completion of a questionnaire or individual question can be defined and the Form Filler Application can record the start and stop date-times using the [Argonaut Questionnaire Time Limit Extension] and [Argonaut QuestionnaireResponse Response Period Extension].  Note that either Form Filler or Service could determine if the response is within a time limit. How this information modifies the behavior of the Form-filler or interpretation of results is an implementation detail outside of scope of this Implementation Guide.
1. The assessment  are short - e.g., PROMIS forms have up to 12 transactions  (on average 4-12).
1. The service may calculated and record score in the QuestionnaireResponse resource as "answers" to a "score" question itme in the Questionnaire.  The score item is flagged as [`readOnly`] and may be marked as 'hidden' using the [Questionnaire Hidden Extension] to direct the Form Filler that the item should not be displayed to the user.
  - To assist in calculating scores the standard [Valuset Ordinal Value Extension] and [Questionnaire Ordinal Value Extension] may be used on items. *NOTE: This implementation quide extends the context of the Questionnaire Ordinal Value Extension to elements beyond that defined in the FHIR Specification.*
  - How and when scoring is done is an implementation detail and outside the scope of this guide.
1.  The [Argonaut Questionnaire Item Order Extension] and conceptOrder] extension may be used by the service to ensure the relative order of Questionnaire items is maintained between transactions.
1. There are no constraints on the nesting of item groups and there are several possible items and item groupings including:
    - *a single* question ('what is the capital of Assyria?') or
    - *a single* display  ('Answer these questions three!!') or
    - *a single* item group of *multiple* display + *multiple* questions  ( 'what is you favorite color?', 'what is the capital of Assyria?', 'what is average flight speed of a laden swallow?')
      - or a group containing the question-score pairs when transmitting an individual score for each item.
    - *a single* item group of: *multiple* item groups ('Answer these questions three!!', 'what is you favorite color?', 'what is the capital of Assyria?', 'what is average flight speed of a laden swallow?')


## Workflow Steps

The following sections provide a detailed description of workflow and API guidance for the Adaptive Forms Use Case.

### Discovery of Adaptive Questionnaire

The discovery process yields a url that identifies the the set of questions for a particular adaptive questionnaire.  The url is included in the *contained* Questionnaire data so that the Adaptive Questionnaire Service is able to identify which set of questions are being requested.

How the discovery and preview of the service's adaptive questionnaire is done is out of scope.  It may be done out of band or using the standard [FHIR RESTful search API].

<!--------- INIT ------------>

### Initiate Adaptive Questionnaire

{% include img-narrow.html img="aw-step1.jpg" %}

To launch the adaptive questionnaire the Form Filler POSTs the operation `$next-question` to the Adaptive Questionnaire Service (“Black Box”) instance endpoint.  A QuestionnaireResponse with a *contained* Questionnaire representing only the resource metadata is provided as payload data.

{% include img-narrow.html img="Slide1.png" %}

The Service updates the contained Questionnaire with the first item and returns the QuestionnaireResponse in the payload.

{% include img-narrow.html img="Slide2.png" %}


#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Next Question Operation]**
- **[Argonaut Adaptive QuestionnaireResponse Profile]**

#### Usage
{:.no_toc}

To initiate an  adaptive questionnaire:

`POST [base]/Questionnaire/$next-question`

{% include examplebutton_default.html example="example-aq-initiate" b_title="Example: $next-question Operation Initiates Adaptive Questionnaire and Returns First Group Item" %}


<!--------- NEXT Q - 1 ------------>

### Get Next Question

{% include img-narrow.html img="aw-step2.jpg" %}

The Form Filler renders the item, presents it to the end-user and records the response in the QuestionnaireResponse.  The Form Filler POSTs the operation `$next-question` to the Service to retrieve the next question.

{% include img-narrow.html img="Slide3.png" %}

As result of the operation, the Service updates the Questionnaire and returns it to the Form Filler.  It identifies the adaptive questionnaire items by their  `definiton` or `linkID` elements and determines the next question based on the responses.  It may also calculate intermediate and/or cumulative scores. The Service updates the contained Questionnaire with the next question and scores if scoring is done and returns it within the QuestionnaireResponse.

{% include img-narrow.html img="Slide4.png" %}

 This step is repeated until the adaptive questionnaire is done or the Questionnaire has timed out or another error has occured.


#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Next Question Operation]**
- **[Argonaut Adaptive QuestionnaireResponse Profile]**


#### Usage
{:.no_toc}

To retrieve the next question:

`POST [base]/Questionnaire/$next-question`

{% include examplebutton_default.html example="example-aq-next1" b_title="Example: $next-question Operation Returns Next Question" %}

{% include examplebutton_default.html example="example-aq-next2" b_title="Example: $next-question Operation Returns Next Question and scoring" %}

<!--------- done ------------>

### Adaptive Questionnaire is Complete

{% include img-narrow.html img="aw-step3.jpg" %}


The Form Filler repeats the process to get the next question as [described above].

{% include img-narrow.html img="Slide7.png" %}

The Service repeats the process [described above]. However, if it determines that the adaptive questionnaire is complete, instead of updating the Questionnnaire with the next question, it updates the QuestionnaireResponse status to ‘completed'. The Service may update the contained Questionnaire with scores if scoring is done. The status of ‘completed’ is a signal to the Form Filler that the adaptive Questionnaire is done!

{% include img-narrow.html img="Slide8.png" %}

#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Next Question Operation]**
- **[Argonaut Adaptive QuestionnaireResponse Profile]**


#### Usage
{:.no_toc}

To retrieve the finished adaptive questionnaire:

`POST [base]/Questionnaire/$next-question`

{% include examplebutton_default.html example="example-aq-done" b_title="Example: $next-question Operation Returns Completed Adaptive Questionnaire" %}


###  QuestionnaireResponse and Scoring

When the adaptive questionnaire is complete, the Form Filler processes the QuestionnaireResponse with a contained Questionnaire based on the questions it was returned by the service.  The Form Filler may represent the cumulative or intermediate scores as answers within the QuestionnaireResponse or as separate Observations.  The Form Filler may post the responses to an Answer Bank and perform searches on the QuestionnaireResponse as described in the [Static Forms Use Case].


### Examples and Reference Implementation

Examples of completed Adaptive QuestionnaireResponses which demonstrate use of all the extensions and support elements as well as many of the question types can be found on the [Argonaut Adaptive QuestionnaireResponse Profile] page.  In addition, the [Argonaut Questionnaire Test Renderer] simulates the adaptive form workflow.

### Amending and Revising Adaptive Forms

#### End User wishes to go back and revise an answer to Question
{:.no_toc}
For adaptive forms it needs to be emphasized that it is a *stateless* process for both the “black box” service and the Form Filler.  That means that the service processes the entire question-answer tree each time from the beginning and the Form Filler re-render the informations each time.  So any question-answer pair or calculated results can change until the form is completed.  The black box may mark some question-answer pairs as [`readOnly`] which instruct the Form Filler that they can not be subsequently altered.   If not marked as a `readOnly`item any response can be changed at any time by the Form Filler and the service will process normally and may remove subsequent question-answers as necessary based on its logic.   The Form Filler will be presented with the presented with question-answer pairs and render it anew as well -i.e., it can not retained the previous information.

#### Answer in Error and Needs to be Reentered
{:.no_toc}

For adaptive forms refer to the FHIR API.  An OperationOutcome with the location of the error represented in the ‘expression element’ and a human readable error message should be returned.

#### Technical Error
{:.no_toc}
Technical errors are typically handled by lower level protocols or manual processes. Typically the Form Filler or Service would simply resubmit the  QuestionnaireResponse.


<br />

---

{% include link-list.md %}
