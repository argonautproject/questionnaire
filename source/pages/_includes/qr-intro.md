{% assign id = {{page.id}} %}
source file: source/pages/\_includes/{{id}}-intro.md

{{site.data.structuredefinitions.[id].description}}

#### Scope and Usage

The Argonaut QuestionnaireResponse resource supports:

- The completed Answer to an assessment form
- Links to questions and assiociated scores for question-answer/answer choice
- Because of it standardized data structure, it  is shareable across systems enabling data aggregation and analysis.

(out of scope)
Can be transformed to other FHIR resources (out of scope)


The Argonaut Questionnaire resource supports:

### Mandatory Data Elements and Terminology

The following data-elements are mandatory:

**Each Questionnaire must have:**

1. A status (Mandatory in base)
1. A link to the question being answered (Mandatory in base)
1. A reference to the form being answered  (Mandatory in SDC)
1. A Patient (Mandatory in SDC)
1. A datetime (Mandatory in SDC)

**The system [Must Support] if available:**

1. QuestionnaireResponse.identifier
1. QuestionnaireResponse.author
1. QuestionnaireResponse.source
1. QuestionnaireResponse.item
1. QuestionnaireResponse.item.definition
1. QuestionnaireResponse.item.text
1. QuestionnaireResponse.item.answer
1. QuestionnaireResponse.item.answer.value[x]
1. QuestionnaireResponse.item.answer.item
1. QuestionnaireResponse.item.item


**Additional Profile specific implementation guidance:**

#### Examples


<!-- {% raw %} {% include list-simple-questionnaires.xhtml %}{% endraw %} -->
- [PHQ-9 Response](QuestionnaireResponse-questionnaireresponse-example-phq9.html)
- [AUDIT Response](QuestionnaireResponse-questionnaireresponse-example-audit.html)
- [DAST Response](QuestionnaireResponse-questionnaireresponse-example-dast.html)
- [Housing Response](QuestionnaireResponse-questionnaireresponse-example-housing.html)
- [ASQ3 Response](QuestionnaireResponse-questionnaireresponse-example-asq3.html)


{%include link-list.md %}
