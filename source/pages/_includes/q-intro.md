{% assign id = {{page.id}} %}
source file: source/pages/\_includes/{{id}}-intro.md

{{site.data.structuredefinitions.[id].description}}

#### Scope and Usage

The Argonaut Questionnaire resource supports:

- Instructions for Subjects (“form filler outers”)
- Instructions for the Providers (e., Scoring instructions)
- Text based questions
  - Including standardized concepts like LOINC
- Answers
  - T/F, multiple choice (Including standardized concepts like LOINC)
  - hort answer, narrative, etc
- Provisions for scoring of answers
  - Textual based description how to calculate the total scores
  - Associated scores for each question-answer/answer choice
- Other Details like whether required or not, Provider instructions hidden or not, etc.`

#### Mandatory Data Elements and Terminology

The following data-elements are mandatory (i.e data MUST be present). blah blah blah

**must have:**

1. blah
1. blah
1. blah

**Additional Profile specific implementation guidance:**

#### Examples

{% include list-simple-questionnaires.xhtml %}

- [PHQ-9](Questionnaire-questionnaire-example-phq-9.html)
- [AUDIT](Questionnaire-questionnaire-example-audit.html)
- [DAST](Questionnaire-questionnaire-example-dast.html)
