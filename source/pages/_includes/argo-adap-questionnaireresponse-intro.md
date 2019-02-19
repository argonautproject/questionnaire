
{% assign id = {{page.id}} %}


{{site.data.structuredefinitions.[id].description}}


**Additional Profile specific implementation guidance:**

See the [Argonaut QuestionnaireResponse Profile] for a description of the constraints on the data elements.

If a question is marked as `repeats` = true, then multiple answers can be provided for the question in the corresponding QuestionnaireResponse. The responses should not be posted to the Service until after all the responses are entered.


#### Examples

- [Adaptive Sampler Response](QuestionnaireResponse-adaptive-questionnaireresponse-example-sampler.html) Completed adaptive questionnaire based on the [Sampler](Questionnaire-questionnaire-example-sampler.html) example
- [Adpative PHQ-9 Response](QuestionnaireResponse-adaptive-questionnaireresponse-example-phq9.html) Completed adaptive questionnaire based on the [PHQ-9](Questionnaire-questionnaire-example-phq9.html) example
- [Adaptive AUDIT-C Response](QuestionnaireResponse-adaptive-questionnaireresponse-example-audit-c.html) Completed adaptive questionnaire based on the [AUDIT-C](Questionnaire-questionnaire-example-audit-c.html) example
- [Adaptive DAST Response](QuestionnaireResponse-adaptive-questionnaireresponse-example-dast.html) Completed adaptive questionnaire based on the [DAST](Questionnaire-questionnaire-example-dast.html) example

<br />

{%include link-list.md %}
