{{site.data.structuredefinitions.[page.id].description}}

**Context of Use:**  {{site.data.structuredefinitions.[page.id].contexts[0].type}}, {{site.data.structuredefinitions.[page.id].contexts[1].type}}


**Implementation Guidance:**
Note that a the order within an array *SHALL* be maintained in conformant FHIR implementation.  However in practice, this can be difficult to validate and maintain. An explicit order element for Questionnaires item groups and answer choices helps the renderer to preserve the proper order.  For example when the resource instance is split up and then reassembled from an application's internal format.

When using a contained value set representing permitted answers for a 'choice' or 'open-choice' question use the standard FHIR extension [valueset-conceptOrder](http://hl7.org/fhir/STU3/extension-valueset-conceptorder.html) to indicate the order rank in the same manner as with this extension.



---
[^4]: <http://hl7.org/fhir/STU3/json.html#xml>

{% include link-list.md %}
