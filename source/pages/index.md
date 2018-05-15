---
title: Argonaut Questionnaire HomePage
layout: default
active: home
topofpage: true
---

{% include publish-box.html %}


<!-- TOC  the css styling for this is \pages\assets\css\project.css under 'markdown-toc'-->

* Do not remove this line (it will not be displayed)
{:toc}


<!-- end TOC -->

##  Introduction

The goal of the Argonaut Questionaire Project is to develop guidance to support interchange of simple forms based on [FHIR Version 3.0.1] and specifically the [Questionnaire] and [QuestionnaireResponse] resources.  This implementation guide provides implementers with FHIR RESTful APIs and guidance to create, use and share between organizations standard assessment forms and the assessment responses.
The requirements were developed and defined by the Argonaut Questionnaire project team and tested through pilot implementations, Argonaut virtual connectathons and HL7 sponsored Connectathons.

This implementation Guide is organized as follows:

- The use case, scope, preconditions and workflow are described in the following sections
- Detailed guidance on using the Argonaut Questionnaire FHIR artifacts such as profiles and extensions can be found on the [Scenario 1] page.
- FHIR profiles and extensions are listed on the [Profiles] page.
- Implementation Guide specific value sets, and code systems on the [Terminology]  page.
- Conformance requirements for both a server and client that claim conformance to this guide are found in the [server] and [client] CapabilityStatements.
- The [Downloads] page contains many downloadable files to help with implementation of this specification.

## Scope
Clinical Assessment used in healthcare can be very sophisticated and complex tools and there are many facets to them. (for example, automatic prepopulation of fields, rendering,  and interactive UIs).  However,
there is clearly a need for a common form standard with a focus on simple assessments.  Clinical Assessments that are hand crafted lead to non standard responses and limited reuse.   Forms should be shareable between systems and across organizational boundaries. With this in mind, the Argonaut Questionaire Poject's focus and scope is on *simple* clinical assessments for the provider with general applicability and question sets that are mostly unstructured in systems today.  The  following table summarizes the scope of this implementation's guide:

<div class="row">
<div class="col-sm-4" markdown="1">

**In Scope**

---

- Simple assessments
    -  Text based questions
    -  scoring
-  Any content provider or source of questions
- Basic workflow for discovery and sharing of forms

---
</div>

<div class="col-sm-4" markdown = "1" >
**Out of Scope**

---

- Complex “structured assessments“
    - Embedded logic for "dynamic" question trees
    - Pre-population and rendering (up to the application)
    - Graphs, flow sheets, charts, video
- CIMI and openEHR-like modelling efforts
- How to elevate response data into structured data
- Data sharing workflow considerations

---

</div>


</div>

## Actors

1. **[Argonaut Questionnaire Profile]**
1. **[Argonaut QuestionnaireResponse Profile]**
1. **"Assessment-Bank"**[^1]: A form repository for the collection of the assessments. It is accessible to both the providers and form editors as a FHIR Questionnaire endpoint.
1. (Optionally) **"Answer-Bank"**[^2]: A repository for the collection of the completed assessments ('answers'). It is accessible to both the providers and form editors as a FHIR QuestionnaireResponse endpoint.  ...TODO: discus...
1. **Provider EHR**[^3]: The System that is capable of retrieving, rendering and displaying the assessment to a subject or a provider to fill out.  This may be the same system as in the Answers section below.
1. **Form Author/Editor**: A system or person authorized to create update and deprecate assessments forms.
1. **Practitioner**: A healthcare provider authorized to administer the assessment to a subject.
1. **Provider administrator**: A practitioner or staff member authorized to fill out an assessment on behalf of a subject or with input from a subject.
1. **Subject**: The patient or individual who is the focus of the assessment.  For example, a patient.


## Assumptions and Preconditions
- The Assessment is completed directly by the subject or by a "provider administer" on behalf of the subject or with input from the subject.
- Patient consent management is out of scope.
- Forms are created and shared within and across organizations
- The questions, answers/answer choices and scoring information are agreed upon across all users of the assessment.
- The appropriate copyright/licensing issues have been addressed.
- This guides supports the [four uses cases] defined for Phase 1 of the [Argonaut Project]:
  - Patients apps that launch standalone
  - Patient apps that launch from a portal
  - Provider apps that launch standalone
  - Provider apps that launch from a portal
- If the patient Subject/Patient Administrator logs in via a third-party application or logged into an EHR’s patient portal, the subject ID is returned or known
  - User level login and trust exists between the EHR and a third party application.
      - A client application has been authorized by the health system and uses [SMART on FHIR] authorization for apps that connect to EHR data.
- System level trust exists between a scheduling server and am external provider system for high volume data exchange - for example, retrieving completed assessments for all patients.
    - Supports the [use case 5] defined for Phase 1 of the Argonaut Project.
    - One solution is to use access FHIR resources by requesting access tokens from OAuth 2.0 compliant authorization servers using [SMART Backend Services].
- [US Core General Guidance] and conventions apply to this guide.

## Workflow Overview

**See [Scenario 1] for a detailed description of workflow and API guidance.**

In the basic workflow outlined below., an EHR system retrieves a standardized assessment represented by the Questionaire resource from an assessment bank.  The Questionnaire is rendered/displayed to the end user - either the subject or provider administrator.  The end user enters responses to the assessment questions and these responses are captured and represented using the QuestionnaireResponse resource.  The response may be processed (scored, aggregated, etc) and shared or stored by other systems.

{% include img.html img="workflow.png" caption="Basic Argonaut Questionnaire Workflow" %}

{:.grid}
|step|Description|
|---|---|
|1|An EHR system retrieves a standardized assessment represented by the Questionnaire resource from an assessment bank.|
|2|The Questionnaire is rendered/displayed to the end user - either the subject or provider administrator.|
|3|The end user enters responses to the assessment questions and these responses are captured and represented using the QuestionnaireResponse resource.|
 |4|The response may be processed (scored, aggregated, etc) and shared or stored by other systems.|

## Security

For general security consideration refer to the [Security section] in the US Core Implementation Guide. See the [Assumptions] section above for a discussion of login and trust.

## Outstanding issues/Future scope

- Management of versioning of assessments
- Intellectual Property and Copyright issues
- Saving/retrieving half completed forms ?
- Supporting retrieval of standard concepts from external repository like VSAC?  ( example: nursing forms)
- preference to contain or include return bundle
- Defining a single way to do X?  e.g choice questions.  (there is more than one way!)
- Scoring -  Currently formal logic is not in scope.



## Jekyll Site Variables  (remove when publish)

These are the site variables defined [here](http://wiki.hl7.org/index.php?title=IG_Publisher_Documentation#Jekyll):

- IG Business version specification (defined in ig.json)- {% raw %}{{site.data.fhir.ig.version}} {% endraw %} = {{site.data.fhir.ig.version}}

- IG status (defined in ig.xml)- {% raw %}{{site.data.fhir.ig.status}} {% endraw %} = {{site.data.fhir.ig.status}}

- Whether is experimental IG (defined in ig.xml) - {% raw %}{{site.data.fhir.ig.experimental}} {% endraw %} = {{site.data.fhir.ig.experimental}}

- IG Publisher name (defined in ig.xml) - {% raw %}{{site.data.fhir.ig.publisher}} {% endraw %} = {{site.data.fhir.ig.publisher}}

- dependency url - e.g. "uscore" : Base url of a dependency implementation Guide (defined in ig.json) -  {% raw %} {{site.data.fhir.uscore}} {% endraw %}= {{site.data.fhir.uscore}}

- igName : Title of the implementation Guide (defined in ig.xml) -  {% raw %} {{site.data.fhir.igName}} {% endraw %}= {{site.data.fhir.igName}}

- path : path to the main FHIR specification (defined in ig.json)-  {% raw %} {{site.data.fhir.path}} {% endraw %}= {{site.data.fhir.path}}

- canonical : canonical path to this specification (defined in ig.json)-  {% raw %} {{site.data.fhir.canonical}} {% endraw %} = {{site.data.fhir.canonical}}

- errorCount : number of errors in the build file (not including HTML validation errors) -  {% raw %} {{site.data.fhir.errorCount}} {% endraw %} = {{site.data.fhir.errorCount}}

- version : version of FHIR -  {% raw %} {{site.data.fhir.version}} {% endraw %} = {{site.data.fhir.version}}

- revision : revision of FHIR -  {% raw %} {{site.data.fhir.revision}} {% endraw %} = {{site.data.fhir.revision}}

- versionFull : version-revision -  {% raw %} {{site.data.fhir.versionFull}} {% endraw %} = {{site.data.fhir.versionFull}}

- totalFiles : total number of files found by the build -  {% raw %} {{site.data.fhir.totalFiles}} {% endraw %} = {{site.data.fhir.totalFiles}}

- processedFiles : number of files genrated by the build -  {% raw %} {{site.data.fhir.processedFiles}} {% endraw %} = {{site.data.fhir.processedFiles}}

- genDate : date of generation (so date stamps in the pages can match those in the conformance resources) -  {% raw %} {{site.data.fhir.genDate}} {% endraw %} = {{site.data.fhir.genDate}}

<br />

---

{%include link-list.md %}
