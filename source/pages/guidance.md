---
title: Scenario 1
layout: default
active: guidance
topofpage: true
---

{:.no_toc}

<!-- TOC  the css styling for this is \pages\assets\css\project.css under 'markdown-toc'-->

* Do not remove this line (it will not be displayed)
{:toc}

## Introduction

The Argonaut Questionnaire Implementation Guide defines a series of interactions which cover the basic workflow for the creation, discovery and retrieval of simple text-based forms using FHIR Questionnaire and QuestionnaireResponse. By using a basic user Scenario that defines the Argonaut Questionnaire project, the basic workflow steps and API are detailed below.  This guidance covers more basic scenarios (for example, a form shared within and organization) and can be scaled up towards more complex scenarios ( for example, see [Structured Data Capture Initiative]).

## Scenario 1

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

Each assessment tool (i.e., set of questions and answer choices) is created once as FHIR Questionnaires and centrally stored in an “Assessment Bank” which can be accessed the program participants (provider EHRS). The provider can then use them to create online questionnaires for their patients.  The responses are captured and processed by the provider EHRS and retrieved by the providers for review. Although out of scope for this guide, these results are shared with the Agency overseeing the program.
~~~


### Form Author Editor Creates Or Updates Assessment
{:.no_toc}

Before an assessment can retrieved it must be created.  This step MAY include updating or deprecation of an assessment.  The Form Author/Editor creates a Questionnaire resource based on a set of assessment questions and answers and associated scores as defined by the program coordinators.  The Questionnaire conforms to the [Argonaut Questionnaire Profile].  How these questions and answer and scores are defined and how the Questionnaire is created are out of scope.  ( note: there are several tools available for authoring fhir resources. )

###  Form Author Editor Uploads The Assessments To The Assessment Bank
{:.no_toc}

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

###  Provider EHRSs Retrieve Standard Assessments From The Assessment Bank
{:.no_toc}

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

Issue:  when retrieval of a Questionnaire that has a choice of concept which reside in a Valueset  ( see Q.options ) should we support that the default action is to *include* the valueset in the bundle since then the EHR provider is not depending on a terminology server to expand the the choices when rendering.

Other options:  
1. prohibit use of external valuesets  ( always enumerate inline )
1. contain the valuesets within the Questionnaire
1. make includes optional

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


### The Provider Ehr Renders And Display The Standard Assessments To The End User
{:.no_toc}

 The assessment is displayed as an online form to be completed by the subject or the provider administrator.  (Printable form in scope?[see issues]) How the form is rendered and displayed are out of scope for this guide.

<!-- {% raw %}>{% include img.html img="diagrams/Slide30.png" caption="Appointment Availability Discovery and Search" %}{% endraw %} -->

###  The End User Completes The Assessment
{:.no_toc}

The responses to the assessment are captured by the Provider EHR. In addition to the recording the response, they are associated with the Assessment and the individual Question on the form.  The Provider EHR may calculate a scored based on the associated scores associated with each item.  How the score is calculated may be described in the Questionnaire, although the actual logic is left to the implementation.  The QuestionnaireResponse may be used to persist the response data.  How the QuestionnaireResponse gets populated is beyond the scope of this IG.  

###  The Practitioner Or Provider Administrator Retrieves The Assessment Responses
{:.no_toc}

The responses to the assessment are retrieved by the practitioner or provider administrator for review and possibly manual processing such as scoring.  The Form associated with the responses may be retrieved at the same time as well.  The QuestionnaireResponse is used to represent the response data in response to the query. In addition to the recording the responses, the responses are associated with the Assessment and the individual Question on the form.  The QuestionnaireResponse resource can be validated against the corresponding Questionnaire to verify that required groups and questions are answered and that answers fit constraints in terms of cardinality, data type, etc.


<!-- {% raw %}>{% include img.html img="diagrams/Slide30.png" caption="Appointment Availability Discovery and Search" %}{% endraw %} -->

<!-- TODO -->
*Discuss how to deal with incomplete or dupicate sets of answers by the same subject [see issues].*

The standard [FHIR RESTful search API] is used with the following *mandatory* search parameters:

- `_id`
- `questionnaire`
- `patient`
- `context`
- `status`

and the following *optional* search parameters:

- `author`
- `source`

*DISCUSS whether to add the following on call*

For the convenience of the client, the server may support including the Questionnaire using the following *optional* search parameter:

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

{% include examplebutton.html example="example-step6" %}

<!--

###  The Assessment Responses Are Analyzed And Shared Across Organizations
{:.no_toc}

The assessment responses are shared with the program administrators using the QuestionnaireResponse resource. By capturing the data in standard structured way, it can be readily processed.  The assessment may be reference to a Questionnaire resource that defines the questions as well as the constraints on the allowed answers.
-->
<!-- {% raw %}>{% include img.html img="diagrams/Slide30.png" caption="Appointment Availability Discovery and Search" %}{% endraw %} -->
<!--



Discuss - is this a push?    in scope?



#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Questionnaire Profile](optionally)**.
- **[Argonaut QuestionnaireResponse Profile]**.

#### Usage

{:.no_toc}

...todo...

{% raw %}{% include examplebutton.html example="example-step6" %}{% endraw %}

-->

###  Step
{:.no_toc}

[description]

<!-- {% raw %}>{% include img.html img="diagrams/Slide30.png" caption="Appointment Availability Discovery and Search" %}{% endraw %} -->

[optional more description]

#### APIs
{:.no_toc}

The following Argonaut Questionnaire artifacts are used in this transaction:

- **[Argonaut Questionnaire Profile]**.
- **[Argonaut QuestionnaireResponse Profile]**.
- **[Other]**.

#### Usage
{:.no_toc}

...todo...

{% include examplebutton.html example="example-step7" %}

---

{% include link-list.md %}
