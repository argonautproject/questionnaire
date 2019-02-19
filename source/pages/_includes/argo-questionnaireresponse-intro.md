
{{site.data.structuredefinitions.[id].description}}

#### Scope and Usage

The Argonaut QuestionnaireResponse resource supports:

- The completed Answer to an assessment form
- Links to questions and associated scores for question-answer/answer choice
- Because of it standardized data structure, it  is shareable across systems enabling data aggregation and analysis

### Mandatory Data Elements and Terminology

The following data-elements are mandatory:

**Each QuestionnaireResponse must have:**

1. A status *
1. A link to the question being answered *
1. A reference to the form being answered  **
1. A Patient **
1. A datetime **

\* Mandatory in the base FHIR QuestionnaireResponse resource

\** Mandatory in the SDC implementation guide


**The system [Must Support] if available:**
1. A [contained] patient resource
1. [Argonaut QuestionnaireResponse Response Period Extension] to record the start and stop date-times for completing a questionnaire or a questionnnaire item or group
1. A business identifier
1. A reference to the envcounter
1. Who or what recorded the answers
1. Who answered the questions
1. Nesting or grouping of answers tha correspond to the structure and grouping of the Questionnaire
    1. The text of the question
    1. The actual response to the question

<!---
**Additional Profile specific implementation guidance:**
-->


#### Examples


<!-- {% raw %} {% include list-simple-QuestionnaireResponses.xhtml %}{% endraw %} -->
- [Sampler Response](QuestionnaireResponse-questionnaireresponse-example-sampler.html) Response to the corresponding [Sampler](Questionnaire-questionnaire-example-sampler.html) example
- [Sampler Response with Contained Patient](QuestionnaireResponse-questionnaireresponse-example-sampler-contained-patient.html) Response to the corresponding [Sampler](Questionnaire-questionnaire-example-sampler.html) example with the subject reference as a contained patient
- [PHQ-9 Response](QuestionnaireResponse-questionnaireresponse-example-phq9.html) Response to the corresponding [PHQ-9](Questionnaire-questionnaire-example-phq9.html) example
- [AUDIT-C Response](QuestionnaireResponse-questionnaireresponse-example-audit-c.html) Response to the corresponding [AUDIT-C](Questionnaire-questionnaire-example-audit-c.html) example
- [DAST Response](QuestionnaireResponse-questionnaireresponse-example-dast.html) Response to the corresponding [DAST](Questionnaire-questionnaire-example-dast.html) example
- [Housing Response](QuestionnaireResponse-questionnaireresponse-example-housing.html) Response to the corresponding [Housing](Questionnaire-questionnaire-example-housing.html) example

<!--
- [ASQ3 Response](QuestionnaireResponse-questionnaireresponse-example-asq3.html)
-->

{%include link-list.md %}
