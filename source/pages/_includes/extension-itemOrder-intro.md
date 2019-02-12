{{site.data.structuredefinitions.[page.id].description}}

**Context of Use:**  {{site.data.structuredefinitions.[page.id].contexts[0].type}}, {{site.data.structuredefinitions.[page.id].contexts[1].type}}


**Implementation Guidance:**
Note that a the order within an array *SHALL* be maintained in conformant FHIR implementation.  However, this is impossible to validate.  An explicit order element for Questionnaires/QuestionaireResponses item groups and answer choices helps the renderer to maintain the proper order as well as when the resource instance is reassembled from an application's internal format.  When using a contained value set representing permitted answers for a 'choice' or 'open-choice' question use the standard FHIR extension [valueset-conceptOrder](http://hl7.org/fhir/STU3/extension-valueset-conceptorder.html) to indicate the order.



---
[^4]: <http://hl7.org/fhir/STU3/json.html#xml>

{% include link-list.md %}
