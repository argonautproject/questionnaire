{% assign id = {{page.id}} %}
source file: source/pages/\_includes/{{id}}-intro.md

{{site.data.structuredefinitions.[id].description}}

#### Scope and Usage

The Argonaut QuestionnaireResponse resource supports:

- The completed Answer to an assessment form
- Links to questions and assiociated scores for question-answer/answer choice
- Because of it standardized data structure, it  is shareable across systems enabling data aggregation and analysis
- **out of scope** Transforming the responses to other FHIR resources such as [Observation].


The Argonaut QuestionnaireResponse resource supports:

### Mandatory Data Elements and Terminology

The following data-elements are mandatory:

**Each QuestionnaireResponse must have:**

1. A status (Mandatory in base)
1. A link to the question being answered (Mandatory in base)
1. A reference to the form being answered  (Mandatory in SDC)
1. A Patient (Mandatory in SDC)
1. A datetime (Mandatory in SDC)

**The system [Must Support] if available:**
1. A [contained] patient resource
1. [QuestionnaireResponse Response Period Extension] to record the start and stop date-times for completing a questionnaire or a questionnnaire item or group
1. A business identifier
1. A reference to the envcounter
1. Who or what recorded the answers
1. Who answered the questions
1. Nesting or grouping of answers tha correspond to the structure and grouping of the Questionnaire
    1. The text of the question
    1. The actual response to the question



**Additional Profile specific implementation guidance:**

#### Examples


<!-- {% raw %} {% include list-simple-QuestionnaireResponses.xhtml %}{% endraw %} -->
- [Sampler Response](QuestionnaireResponse-questionnaireresponse-example-sampler.html)
- [PHQ-9 Response](QuestionnaireResponse-questionnaireresponse-example-phq9.html)
- [AUDIT Response](QuestionnaireResponse-questionnaireresponse-example-audit.html)
- [DAST Response](QuestionnaireResponse-questionnaireresponse-example-dast.html)
- [Housing Response](QuestionnaireResponse-questionnaireresponse-example-housing.html)
- [ASQ3 Response](QuestionnaireResponse-questionnaireresponse-example-asq3.html)


{%include link-list.md %}
