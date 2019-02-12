---
title: Static Forms
layout: default
active: guidance
topofpage: true
---

{:.no_toc}

<!-- TOC  the css styling for this is \pages\assets\css\project.css under 'markdown-toc'-->

* Do not remove this line (it will not be displayed)
{:toc}

## Introduction

The Argonaut Questionnaire Implementation Guide defines a series of interactions which cover the basic workflow for the creation, discovery and retrieval of simple static text-based forms using FHIR Questionnaire and QuestionnaireResponse and the FHIR API..

Each assessment tool (i.e., set of questions and answer choices) is created once as FHIR Questionnaires and centrally stored in an “Assessment Bank” which can be accessed by the provider EHRS. The provider can then render the form for the end user to complete.  The form responses are captured and processed by the provider EHRS and can be stored using the QuestionnaireResponse in an "Answer Bank and subsequently retrieved by the providers for review. Although out of scope for this guide, these results can be aggregated and shared within or across systems.

These basic workflow steps and API are detailed below.  This guidance covers more basic scenarios, but can be scaled up towards more complex scenarios ( for example, see [Structured Data Capture Initiative]).

## Example Scenario

This simple scenario serves as an effective means to describe the Argonaut Questionnaire basic workflow and API

~~~ text
A Jurisdiction (e.g, state or region) publicly funds a program to improve population health.  The program is instituted and a set of standard assessments are to filled out by the program participants (“subjects”) periodically in order to monitor the program’s success or failure.

Example list of Assessment Categories:

Demographic information
Physical health review
Substance use review
Housing assessment  
Suicide risk assessment  
Universal screening using depression screening (PHQ 2 & 9)
...

Each assessment tool (i.e., set of questions and answer choices) is created once as FHIR Questionnaires and centrally stored in an “Assessment Bank” which can be accessed the program participants (provider EHRS). The provider can then use them to create online questionnaires for their patients.  The responses are captured and processed by the provider EHRS and retrieved by the providers for review. These results are shared with the Agency overseeing the program.
~~~

## Workflow Steps

### Form Author Creates Assessment

Before an assessment can retrieved it must be created.  This step MAY include updating or deprecation of an assessment.  The Form Author/Editor creates a Questionnaire resource based on a set of assessment questions and answers and associated scores as defined by the program coordinators.  The Questionnaire conforms to the [Argonaut Questionnaire Profile].  How these questions and answer and scores are defined and how the Questionnaire is created are out of scope.  ( note: there are several tools available for authoring fhir resources. )

### Form Author Posts to Assessment Bank

The Author/Editor is able to upload the Questionnaires to a FHIR server which serves as a repository where all the program participants can search and download the standard assessment when they need them.  Multiple version of each assessment may be available. [see issues]

<!-- {% raw %}>{% include img.html img="diagrams/Slide30.png" caption="Appointment Availability Discovery and Search" %}{% endraw %} -->

This transaction use the standard [FHIR RESTful API] to created, update, and delete Questionnaires from the Assessment bank:

#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Questionnaire Profile]**.

#### Usage
{:.no_toc}

To create a Questionnaire:

`POST [base]/Questionnaire/...`

To update a Questionnaire:

`PUT [base]/Questionnaire/[id]`

to delete a Questionnaire:

`DELETE [base]/Questionnaire/[id]`

{% include examplebutton.html example="example-step1" %}

###  Provider EHRSs Fetches Form


When it is time to perform an assessment of the program participants(subjects), the Provider EHR fetches the appropriate Questionnaire(s) from the Assessment-Bank.  

<!-- {% raw %}>{% include img.html img="diagrams/Slide30.png" caption="Appointment Availability Discovery and Search" %}{% endraw %} -->

The standard [FHIR RESTful search API] is used with the following *mandatory* search parameters:

- `_id`
- `url`
- `status`
- `title`

and the following *optional* search parameters

- `version`
- `context-type` ([Custom search parameters])
- `context-value`([Custom search parameters])

(others?... discuss)

(multiple version of each assessment may be available. [see issues])

#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Questionnaire Profile]**.

Note that all ValueSets used are [contained] resources within the Questionnaire


#### Usage
{:.no_toc}

Fetching a *single* Questionnaire:

- based on its id:

    `GET [base]/Questionnaire/[id]`

- based on its url (note the QuestionnaireResponse uses the url to reference the assessment upon which it is based):

    `GET [base]/Questionnaire?url=[uri]`

- based on its title (the supplied parameter can  equals or starts with the title ):

    `GET [base]/Questionnaire?title=[title]`

-  based on its title and version:

    `GET [base]/Questionnaire?title=[title]&version=[version]``

Searching for *all* the active Questionnaires:

  `GET [base]/Questionnaire?status=active`

Searching for a *collection* of Questionnaires based on context-type and context-value(think category):

  `GET [base]/Questionnaire?context-code=[code]&context-value=[value]`

{% include examplebutton.html example="example-step2" %}


### Form Filler Renders And Displays The Form


 The assessment is rendered and displayed to the end user (for example, as an online form ) to be completed by the subject or the provider administrator.   How the form is rendered and displayed are out of scope for this guide.

<!-- {% raw %}>{% include img.html img="diagrams/Slide30.png" caption="Appointment Availability Discovery and Search" %}{% endraw %} -->

### End User Completes The Assessment

The responses to the assessment are captured by the Form Filler. It may also  calculate a scored based on the associated values associated with each item via the [Argonaut Questionnaire Score Extension].  How the score is calculated may be described within the Questionnaire, often as a hidden display item. The actual logic and calculation is an implementation detail outside of scope of this Implementation Guide.

The QuestionnaireResponse resource may be used to capture, exchange and persist the response data.  It represents the response data to the individual questions on the form and is ordered and grouped corresponding to the structure and grouping of the Questionnaire being responded to. How the QuestionnaireResponse gets populated is beyond the scope of this IG.

Time limits for completion of a questionnaire or individual question can be defined in the [Argonaut Questionnaire Time Limit Extension].  The Form Filler can record the start and stop date-times in the [Argonaut QuestionnaireResponse responsePeriod Extension] which can be used to determine whether the questionnaire or items were answered within the prescribed time limit.  How this information modifies the behavior of the Form-filler or interpretation of results is an implementation detail outside of scope of this Implementation Guide.

### Provider EHR Posts to Answer Bank

The responses captured as QuestionnaireResponse are are uploaded to an Answer Bank where they can be retrieved for subsequent use and analysis.  As is defined in the Argonaut QuestionnaireResponse Profile, a [contained] Patient resource may inserted in order to facilitate subsequent analysis as described below. The QuestionnaireResponse resource can be validated against the corresponding Questionnaire to verify that required groups and questions are answered and that answers fit constraints in terms of cardinality, data type, etc.

#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut QuestionnaireResponse Profile]**

#### Usage
{:.no_toc}

create a *single* QuestionnaireResponse:

  `POST [base]/QuestionnaireResponse`

update a *single* QuestionnaireResponse::

  `PUT [base]/QuestionnaireResponse/[id]`

create *multiple* QuestionnaireResponses using a [batch] transaction:

  `POST/[base]`


{% include examplebutton.html example="example-step6" %}


### Provider EHR Searches Answer Bank

Responses to the assessment are retrieved for a variety of purposes. QuestionnaireResponse can be searched using the standard QuestionnaireResponse search parameters listed below.  If the Answer Bank has access to the Questionnaire resource, searches may fetch the Questionnaire at the same time as well using the [`_include`] parameter.   **Note that individual responses are not directly searchable using the FHIR RESTful API**.  In order to search directly on responses, they must be "downloaded" into a searchable form - i.e. to a local  FHIR or non-FHIR data store such as a database or FHIR Observations.

#### Patient Demographic Based Searches

It is common to search for responses based on patient demographic information such as such as age, sex, race, location. There are three options for searching based on the subject demographics:

1. If the Answer Bank has access the subject's Patient resource, a [chained] query can be performed using the `subject` reference parameter as detailed below.

1. When the Answer Bank does not have access to the subject's Patient resource, a [contained] patient resource in the QuestionnaireResponse can be used to allow for searching on the Patient.  If the Answer Bank is in an untrusted environment such as a external shared server, the contained patient resource should only represent the minimum de-identified data necessary to perform the search -  e.g. a resource with month/year of birth, sex, race/ethnicity, and first two or three digits of US zip code.  The search syntax is detailed below.

1.  As stated above, individual responses to answers to questions like age, race, sex and location are not directly searchable through QuestionnaireResponse and can be converted to a searchable form for direct access.  This approach to search is outside the scope of this implementation guide.

<!-- {% raw %}>{% include img.html img="diagrams/Slide30.png" caption="Appointment Availability Discovery and Search" %}{% endraw %} -->

The standard [FHIR RESTful search API] is used with the following *mandatory* search parameters:

- `_id`
- `questionnaire`
- `patient` ( including chained parameters of (gender, birthdate, us-coreace, us-core ethnicity, address-postalcode ))
- `context`
- `status`

and the following *optional* search parameters:

- `author`
- `source`

and the following *optional* chained search parameters:

- patient.gender
- patient.birthdate (with support for date prefixes `le` and `ge`)
- patient.race
- patient.ethnicity
- patient.address-postalcode


For the convenience of the client, the Answer Bank may support including the Questionnaire using the following *optional* search parameter:

- `\_include`  Note that this path references a resource on the Assessment Bank server which is typically another server.

#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Questionnaire Profile]**.
- **[Argonaut QuestionnaireResponse Profile]**.

#### Usage
{:.no_toc}


Fetching a *single* QuestionnaireResponse:

- based on its id:

    `GET [base]/QuestionnaireResponse/[id]`

- based on its id and include the Questionnaire:

    `GET [base]/QuestionnaireResponse?_id=[id]&_include=QuestionnaireResponse:questionnaire`


Searching for *all* the completed QuestionnaireResponses

- based on particular assessment:

    `GET [base]/QuestionnaireResponse/?status=completed&questionnaire=[questionnaire url]`

- based on a patient encounter:

    `GET [base]/QuestionnaireResponse/?status=completed&patient=Patient/[patient]&context=Encounter/[encounter]`

Searching for *all* QuestionnaireResponses with any status

- based on who administered it:

    `GET [base]/QuestionnaireResponse/?source=Practitioner/[practitioner]`

    `GET [base]/QuestionnaireResponse/?author=Practitioner/[practitioner]`

Searching for all QuestionnaireResponses based upon patient demographics

- based on sex and age range:

    `GET [base]/QuestionnaireResponse/?patient.gender=[gender]&patient.birthdate=ge[date]{&patient.birthdate=lt[date]}`

- based on location:

    `GET [base]/QuestionnaireResponse/?patient.address-postalcode=[zip]`

- based on ethnicity:

    `GET [base]/QuestionnaireResponse/?patient.ethnicity=[ethnicity code]`

- based on race:

    `GET [base]/QuestionnaireResponse/?patient.race=[race code]`


{% include examplebutton.html example="example-step6" %}


---

{% include link-list.md %}
