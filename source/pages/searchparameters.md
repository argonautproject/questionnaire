---
title: Search Parameters defined as part of this Guide
layout: default
active: searchparameters
---
The following search parameters have been defined for the {{site.data.fhir.igName}} Implementation Guide.  For more information on the [FHIR RESTful search api] and the standard [Search Param Registry] see the FHIR specification.

Search Parameter

**Patient**
  - [birthdate](SearchParameter-patient-birthdate.html)

**Questionnaire**

  - [`_id`]
  - [`url`]
  - [`status` (Questionnaire)]
  - [`title`]
  - [`publisher`]
  - [`version`]
  - [`context`]
  - [`context-type`]
  - [`context-type-value`]

**QuestionnaireResponse**
  - [`_id`]
  - [`questionnaire`]
  - [`patient`]
  - [`context`]
  - [`status` (QuestionnaireResponse)]
  - [`author`]
  - [`source`]

<br />

{% include link-list.md %}
