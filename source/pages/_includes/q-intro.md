{% assign id = {{page.id}} %}
source file: source/pages/\_includes/{{id}}-intro.md

{{site.data.structuredefinitions.[id].description}}

### Scope and Usage

The Argonaut Questionnaire resource supports:

- Instructions for Subjects/Provider administrator
- Instructions for the Providers (e.g, Scoring instructions)
- Text based questions
  - Including standardized concepts like [LOINC]
- Answers
  - T/F, multiple choice (Including standardized concepts like LOINC)
  - hort answer, narrative, etc
- Provisions for scoring of answers
  - Textual based description how to calculate the total scores
  - Associated scores for each question-answer/answer choice
- Other Details like whether required or not, Provider instructions hidden or not, etc.

### Mandatory Data Elements and Terminology

The following data-elements are mandatory:

**Each Questionnaire must have:**



1. An absolute URI that is used to identify this assessment form when it is referenced by a response (required by SDC )
1. A human friendly title
1. The form's status (base specification requirement)
1. An identifier to link to the response in a QuestionnaireResponse resource  (base specification requirement)
1. A questions type including if a display only  question grouping elements (base specification requirement)

**The system [Must Support] if available:**

1. [Argonaut Questionnaire Score] *Extension* for use on all answer types and choices (not just codings).
1. [Argonaut Questionnaire Time Limit] *Extension* for indicating the duration allowed for all or parts of the assessment.
1. A version of the assessment
1. A description of the assessment
1. A standard concept code (e.g., LOINC) for the question or questions
1. Text for:
    1. the Question (including prefixes such as numbering or lettering)
    1. Instructions to the Subject/Provider administrator and or scorer
1. A required flag
1. A repeat flag
1. Choice list:
   1. as a [contained] valueset of standard concepts
   1. or as an enumerated list
1. Nesting or grouping of questions
1. the questionnaire's context for categorizing and grouping for searches

**What about these?**

- Questionnaire.identifier
- Questionnaire.date
- Questionnaire.publisher
- Questionnaire.jurisdiction
- Questionnaire.contact
- Questionnaire.copyright
- Questionnaire.code
- Questionnaire.item.definition
- Questionnaire.item.readOnly
- Questionnaire.item.maxLength
- Questionnaire.item.initial[x]

Extensions:

- [questionnaire-maxOccurs]
- [questionnaire-minOccurs]


**Additional Profile specific implementation guidance:**

All ValueSets referenced by the `.options` element are [contained] resources in the Questionnaire.  This ensures that the Questionnaire will not adopt a new version of the referenced value set without revising the Questionnaire to point to that new version - putting the author of the Questionnaire in control of any changes.

### Examples

<!-- {% raw %} {% include list-simple-questionnaires.xhtml %}{% endraw %} -->
- [PHQ-9](Questionnaire-questionnaire-example-phq9.html)
- [AUDIT](Questionnaire-questionnaire-example-audit.html)
- [DAST](Questionnaire-questionnaire-example-dast.html)
- [Housing](Questionnaire-questionnaire-example-housing.html)
- [ASQ3](Questionnaire-questionnaire-example-asq3.html)

{%include link-list.md %}
