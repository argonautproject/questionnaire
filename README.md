# Welcome to the [Argonaut](http://argonautwiki.hl7.org/index.php?title=Main_Page) Argonaut Questionnaire Project Repository

See the simulation and test Questionnaire rendering tool at : http://gettingstarte-cjfwz-env.us-west-2.elasticbeanstalk.com/
    (2019-2-23 : Note is not current and needs to be updated)


**IG code:** `guides/argonaut/questionnaire`
<!--Proposed IG realm and code
What is the realm code (2-character country code or 'uv') and IG code to use for the path when the IG is published under http://hl7.org/fhir? E.g. us/ccda -->

**Short Description:** Guidance on creating and using basic FHIR Questionnaires for simple Assessments.
<!--1-2 sentences describing the purpose/scope of the IG for inclusion in the registry- this is the sentence that will be used here: http://www.fhir.org/guides/registry. This must describe the IG from the perspective of an implementer scanning a registry -->

**Long Description:** The goal of the Argonaut Questionnaire Project is to develop guidance to support interchange of simple forms based on [FHIR Version 3.0.1](http://hl7.org/fhir/STU3/) and specifically the [Questionnaire](http://hl7.org/fhir/STU3/questionnaire.html) and [QuestionnaireResponse](http://hl7.org/fhir/STU3/questionnaireresponse.html) resources.  This implementation guide provides implementers with FHIR RESTful APIs and guidance to create, use and share between organizations standard assessment forms and the assessment responses.  The requirements were developed and defined by the Argonaut Questionnaire project team and tested through pilot implementations, Argonaut virtual connectathons and HL7 sponsored connectathons.
<!-- 1(-2) paragraphs describing the purpose/scope of the IG in more detail for inclusion in the version history - this is content that will be used in your IG's equivalent of this: http://www.hl7.org/fhir/us/core/history.cfml. Again, this must describe the IG from the perspective of an implementer scanning a registry, it should not talk about the project and should NOT be copied from the PSS.  -->



Argonaut Lead: [Micky Tripathi](mtripathi@maehc.org)

Project Coordinator: [Jennifer Monahan](jmonahan@maehc.org)

FHIR SME and Facilitator: [Eric Haas](ehaas@healthedatainc.com)

FHIR SME and Facilitator: [Brett Marquard](brett@waveoneassociates.com)


## Scope of Work

Support Guidance on creating and using basic FHIR Questionnaires for simple Assessments.

## TimeLine

**April 2018**:

  - Argo Questionnaire Kickoff
  - Refine Scope
  - Define Content and technical Specifications for Draft Implementation Guide"
  
**Summer 2018**:

- Initial Connectathon for interested parties to start experimenting with proposed technical specification
- Publish and refine Draft IG"

**Sept 2018**:

- FHIR Connectathon events to refine and develop the technical specification

**Fall 2018**:

- Publish and refine Draft IG

**January 2019**:

- Published IG

## Repository Directory

## Directory Tree

~~~
├── README.md
├── base.html
├── definitions.csv
├── dependencies
│   └── uscore-vp
├── docs
│   ├──{xhtml output}
├── ex.html
├── format.html
├── framework
│   ├── _includes
│   ├── _layouts
│   └── assets
├── generated_output
│   ├── qa
│   ├── temp
│   └── txCache
├── ig.json
├── meeting-notes
├── sd-definitions.html
├── sd-mappings.html
├── sd.html
└── source
    ├── examples
    ├── pages
    └── resources

20 directories,

~~~
