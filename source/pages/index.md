---
title: Argonaut Questionnaire HomePage
layout: default
active: home
topofpage: true
---

<!-- TOC  the css styling for this is \pages\assets\css\project.css under 'markdown-toc'-->

* Do not remove this line (it will not be displayed)
{:toc}


<!-- end TOC -->

##  Introduction

The goal of the Argonaut Questionnaire Project is to develop guidance to support interchange of simple forms based on [FHIR Version 3.0.1] and specifically the [Questionnaire] and [QuestionnaireResponse] resources.  This implementation guide provides implementers with FHIR RESTful APIs and guidance to create, use and share between organizations standard assessment forms and the assessment responses.
The requirements were developed and defined by the Argonaut Questionnaire project team and tested through pilot implementations, Argonaut virtual connectathons and HL7 sponsored connectathons.

This implementation Guide is organized as follows:

- The use case, scope, preconditions and workflow are described in the following sections
- Detailed guidance on using the Argonaut Questionnaire FHIR artifacts such as profiles and extensions can be found on the [Scenario 1] page.
- FHIR profiles and extensions are listed on the [Profiles] page.
- Implementation Guide specific value sets, and code systems on the [Terminology]  page.
- Conformance requirements for the systems that claim conformance to this guide are found in the [Assessment-Bank], [Answer-Bank], [Provider EHR] and [Adaptive Questionnaire Service] CapabilityStatements.
- The [Downloads] page contains many downloadable files to help with implementation of this specification.

## Scope
Clinical Assessment used in healthcare can be very sophisticated and complex tools and there are many facets to them. (for example, automatic pre-population of fields, rendering,  and interactive UIs).  However,
there is clearly a need for a common form standard with a focus on simple assessments.  Clinical Assessments that are hand crafted lead to non standard responses and limited reuse.   Forms should be shareable between systems and across organizational boundaries. With this in mind, the Argonaut Questionnaire Project's focus and scope is on *simple* clinical assessments for the provider with general applicability and question sets that are mostly unstructured in systems today.  The  following table summarizes the scope of this implementation's guide:

<div class="row">
<div class="col-sm-4" markdown="1" style="background-color: Lightcyan;">

**In Scope**

---

- Simple assessments
    -  Text based questions
    -  scoring
-  Any content provider or source of questions
- Basic workflow for discovery and sharing of forms

---
</div>

<div class="col-sm-4" markdown = "1" style="background-color: WhiteSmoke;">
**Out of Scope**

---

- Complex “structured assessments“
    - Embedded logic for "dynamic" question trees
    - Pre-population and rendering (up to the application)
    - Graphs, flow sheets, charts, video
- CIMI and openEHR-like modeling efforts
- How to elevate response data into structured data
- Data sharing workflow considerations

---

</div>

</div>

### Prior and Concurrent Work
The [SDC (Structured Data Capture)] implementation guide based on [FHIR Version 4.0.0] provides a set of guidance around the use of Questionnaire and QuestionnaireResponse for more advanced implementation of Questionnaires including:
 - Advanced Rendering
 - Advanced Form behavior
 - Importation of Data into Forms
 - Extraction of Data from Forms

It also overlaps with some of the content covered in this guide including adaptive form.  Efforts have been made to align this guide with SDC wherever possible.

The Patient Reported Outcomes (PRO) implementation guide focus on capturing and exchanging patient reported outcome data electronically using the FHIR standard. The PRO FHIR IG does not define any specific new profiles, but rather uses the profiles defined by SDC.

## Actors

1. **[Adaptive Questionnaire Service]**:  A System that is capable of providing questions in response to requests and contains logic for determination of the next question and calculation of the score for an [Adaptive Questionnaire].  For this Implementation Guide, this service is treated as a **“[Black Box]”**.
1. **[Assessment-Bank]**[^1]: A form repository for the collection of the assessments. It is accessible to both the providers and form editors as a FHIR Questionnaire endpoint.
1. **[Answer-Bank]**[^2]: A repository for the collection of the completed assessments ('answers'). It is accessible to the providers  as a FHIR QuestionnaireResponse endpoint.  It may be internal or external to the **[Provider EHR]**.
1. **Form Author/Editor**: A system or person authorized to create update and deprecate assessments forms.
1. **Client Application**: The software application interacting with the user to get answers for a questionnaire.  It can be integrated into the Provider EHR or an external patient portal or third party app.
1. **Practitioner**: A healthcare provider authorized to administer the assessment to a subject.
1. **Provider administrator**: A practitioner or staff member authorized to fill out an assessment on behalf of a subject or with input from a subject.
1. **[Provider EHR]**[^3]: Also Referred to as "Form Filler". A System that is capable of retrieving, rendering and displaying the assessment to a subject or a provider to fill out.  
1. **Subject**: The patient or individual who is the focus of the assessment.  For example, a patient.

## Artifacts

1. **[Argonaut Adaptive QuestionnaireResponse Profile]**
1. **[Argonaut Questionnaire Profile]**
1. **[Argonaut QuestionnaireResponse Profile]**
1. **[Argonaut Next Question Operation]**


## Assumptions and Preconditions

- The Assessment is completed directly by the subject or by a "provider administer" on behalf of the subject or with input from the subject.
- Patient consent management is out of scope.
- Forms are created and shared within and across organizations.
- The questions, answers/answer choices and scoring information are agreed upon across all users of the assessment.
- The appropriate copyright/licensing issues have been addressed.
- This guides supports the four uses cases defined for Phase 1 of the Argonaut Project.
- If the patient Subject/Patient Administrator logs in via a third-party application or logged into an EHR’s patient portal, the subject ID is returned or known.
  - User level login and trust exists between the EHR and a third party application.
      - A client application has been authorized by the health system and uses [SMART on FHIR] authorization for apps that connect to EHR data.
<!--
- System level trust exists between systems for high volume data exchange - for example, retrieving completed assessments for all patients.
    - Supports the [use case 5] defined for Phase 1 of the Argonaut Project.
    - One solution is to use access FHIR resources by requesting access tokens from OAuth 2.0 compliant authorization servers using [SMART Backend Services].
-->
- [US Core General Guidance] and conventions apply to this guide.

## Workflow Overview

### Static Forms

**See  the [Static Forms Use Case] for a detailed description of workflow and API guidance.**

In the basic workflow outlined below., an EHR system retrieves a standardized assessment represented by the Questionnaire resource from an assessment bank.  The Questionnaire is rendered/displayed to the end user - either the subject or provider administrator.  The end user enters responses to the assessment questions and these responses are captured.   The response may be processed (scored, aggregated, etc) and retrieved using the QuestionnaireResponse resource.

{% include img-portrait-med.html img="static_overview.svg" caption="Basic Argonaut Questionnaire Workflow" %}

{:.grid}
|step|Description|
|---|---|
|1|An EHR system retrieves a standardized assessment represented by the Questionnaire resource from an assessment bank.|
|2|The Questionnaire is rendered/displayed to the end user - either the subject or provider administrator.|
|3|The end user enters responses to the assessment questions and these responses are stored in the Answer Bank by POSTing a QuestionnaireResponse|
|4|An EHR system requests answers to an assessment for a particular subject|
|5|The QuestionnaireResponse is processed by the end user|


### Adaptive Forms

**See  the [Adaptive Forms Use Case] for a detailed description of workflow and API guidance.**

Adaptive Forms or Questionnaires such as [PROMIS] forms use a stateless model where a selection of items is presented on the computer to an end user based on the answers on the prior items. The server selects the following items optimized for the outcome of the assessment or testee's estimated ability or trait[^4]. This implementation guide provides the basic framework for using Questionnaire and QuestionnaireResponse to preserve the state of the Questionnaire as the client retrieves questions from a remote adaptive questionnaire service.

{% include img-portrait.html img="adaptive-workflow.jpg" caption="Basic Argonaut Questionnaire Workflow" %}

{:.grid}
|step|Description|
|---|---|
|1|​A Provider EHR may need to discover and review available Adaptive Questionnaire's (not shown).|
|2|The Form Filler initiates the Adaptive Questionnaire by posting to the Adaptive Questionnaire Service's endpoint.|
|3|Treated as a "Black Box", the Adaptive Questionnaire Service's returns the first question to the Form Filler.|
|4|The Questionnaire is rendered/displayed to the end user - either the subject or provider administrator.|
|5|The Form Filler returns the question and answer pair to the Adaptive Questionnaire Service's endpoint.|
|6|Based on the prior question and answer pair(s), the Adaptive Questionnaire Service returns the next question to the Form Filler.|
|7|Steps 5 and 6 are repeated until the questionnaire is done.|
|8|The Provider EHR may process the questions and answers.|

## Security and Privacy Considerations

For general security consideration refer to the [US Core Implementation Guide security section] and [FHIR Security] in core FHIR Specification. See the [Assumptions] section above for a discussion of login and trust.

Responses to Questionnaires may be stored in an external ‘answer bank’ that is shared and may not be in a trusted environment. Therefore careful consideration to determine whether posting a QuestionnaireResponse to a shared answer bank is risking the patient's privacy. Guidance on how to maintain patient privacy and still be able to search the responses effectively is provided in the section on [Patient Demographic Based Search].

---

{%include link-list.md %}
