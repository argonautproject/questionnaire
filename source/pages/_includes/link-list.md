[^1]: This is called the 'Form Manager' in the [Structured Data Capture Initiative] (SDC)
[^2]: This is called the 'Form Receiver/Archiver' in the [Structured Data Capture Initiative] (SDC)
[^3]: This is called the 'Form Filler' and/or 'Form Response Handler' in the [Structured Data Capture Initiative] (SDC)
[^4]: https://en.wikipedia.org/wiki/Questionnaire
[^5]: How to implement Questionnaire  to design forms that adjust what information is displayed and/or that perform calculations based on user input is covered in the [SDC (Structured Data Capture)] implementation Guide.
[Adaptive Questionnaire]: https://en.wikipedia.org/wiki/Computerized_adaptive_testing
[Adaptive Forms Use Case]: adaptive.html
[Answer-Bank]: CapabilityStatement-answerbank.html
[Argonaut Adaptive QuestionnaireResponse Profile]: StructureDefinition-argo-adap-questionnaireresponse.html "The Argonaut Adaptive QuestionnaireResponse Profile  is derived from the Argonaut QR profile requiring a containedArgonaut Questionnaire Profile to support the adaptive questionnaire use case."
[Argonaut Adaptive Questionnaire Profile]: StructureDefinition-argo-adaptive-questionnaire.html "The contained Argonaut Questionnaire Profile to support the adaptive questionnaire use case."
[Argonaut Next Question Operation]: OperationDefinition-next-question.html "The Argonaut Next Question Operation is used for adaptive questionnaires forms where the next question is based on previous answers."
[Argonaut Project]: http://argonautwiki.hl7.org/index.php?title=Main_Page
[Argonaut Questionnaire Profile]: StructureDefinition-argo-questionnaire.html "Argonaut Questionnaire Profile"
[Questionnaire Ordinal Value Extension]: {{site.data.fhir.path}}extension-questionnaire-ordinalvalue.html "A numeric value that allows the comparison (less than, greater than) or other numerical manipulation of a concept (e.g. adding up components of a score)."
[Argonaut Questionnaire Contained ValueSet Profile]: StructureDefinition-argo-questionnaire-valueset.html "The Argonaut Questionnaire Contained ValueSet Profile is contained within the Argonaut Questionnaire Profile"
[Argonaut Questionnaire Time Limit Extension]: StructureDefinition-extension-timeLimit.html
[Argonaut Questionnaire Item Order Extension]: StructureDefinition-extension-itemOrder.html
[Argonaut QuestionnaireResponse Response Period Extension]: StructureDefinition-extension-responsePeriod.html
[Argonaut QuestionnaireResponse Profile]: StructureDefinition-argo-questionnaireresponse.html  "Argonaut QuestionnaireResponse Profile"
[Assessment-Bank]: CapabilityStatement-assessmentbank.html
[Assumptions]: index.html#assumptions-and-preconditions  "Assumptions-and-Preconditions"
[Black Box]: https://en.wikipedia.org/wiki/Black_box
[client]: CapabilityStatement-client.html
[contained]: {{site.data.fhir.path}}references.html#contained
[Custom search parameters]: searchparameters.html
[Downloads]: downloads.html
[expansion]: {{site.data.fhir.path}}valueset.html#expansion "The list of codes that are actually in the value set under a given set of conditions ("extension")"
[FHIR RESTful API]: {{site.data.fhir.path}}http.html
[FHIR RESTful search API]: {{site.data.fhir.path}}search.html
[FHIR Version 3.0.1]: {{site.data.fhir.path}}index.html
[four uses cases]: http://argonautwiki.hl7.org/images/4/4c/Argonaut_UseCasesV1.pdf
[LOINC]: http://loinc.org
[Must Support]: {{site.data.fhir.uscore}}/guidance.html#must-support
[Valuset Ordinal Value Extension]: {{site.data.fhir.path}}extension-valueset-ordinalvalue.html "ValueSet ordinalvalue extension: A numeric value that allows numerical manipulation of a concept."
[Profiles]: profiles.html
[Provider EHR]: CapabilityStatement-server.html
[Questionnaire examples]: StructureDefinition-argo-questionnaire.html#examples
[Questionnaire Hidden Extension]: {{site.data.fhir.path}}extension-questionnaire-hidden.html "Questionnaire hidden extension: If true, indicates that the extended item should not be displayed to the user."
[Questionnaire Option Exclusive Extension]: {{site.data.fhir.path}}extension-questionnaire-optionexclusive.html "Questionnaire optionexclusive  modifier extension: If true, indicates that if this option is selected, no other options may be selected."
[Questionnaire]: {{site.data.fhir.path}}questionnaire.html "Questionnaire resource"
[QuestionnaireResponse]: {{site.data.fhir.path}}questionnaireresponse.html "QuestionnaireResponse resource"
[Observation]: {{site.data.fhir.path}}observation.html "Observation resource"
[Security section]: {{site.data.fhir.uscore}}security.html "US Core Security"
[server]: CapabilityStatement-server.html
[SMART Backend Services]: http://docs.smarthealthit.org/authorization/backend-services/
[SMART on FHIR]: http://docs.smarthealthit.org/authorization/
[Static Forms Use Case]: static.html
[Structured Data Capture Initiative]: http://build.fhir.org/ig/HL7/sdc/ "SDC"
[Terminology]: terminology.html "Defines expectations for sharing of Questionnaires and answers, including mechanisms for automatically populating portions of a questionnaire based on embedded mappings to underlying data elements"
[SDC (Structured Data Capture)]: http://hl7.org/fhir/us/sdc/history.html "Defines expectations for sharing of Questionnaires and answers, including mechanisms for automatically populating portions of a questionnaire based on embedded mappings to underlying data elements"
[US Core General Guidance]: {{site.data.fhir.uscore}}guidance.html "US Core General Guidance"
[use case 5]: http://argonautwiki.hl7.org/images/4/4c/Argonaut_UseCasesV1.pdf
[`_include`]: {{site.data.fhir.path}}search.html#revinclude
[FHIR operations]: {site.data.fhir.path}}operations.html
[PROMIS]: http://www.healthmeasures.net/explore-measurement-systems/promis "PROMIS® (Patient-Reported Outcomes Measurement Information System) is a set of person-centered measures that evaluates and monitors physical, mental, and social health in adults and children. It can be used with the general population and with individuals living with chronic conditions."
[FHIR Version 4.0.0]: http://hl7.org/fhir/R4/ "FHIR Release #4: First Normative Content"
[Patient Reported Outcomes (PRO)]: http://www.hl7.org/fhir/us/patient-reported-outcomes/history.cfml "Standardization in the creation, administration and sharing of PRO data"
 [HealthMeasures]: http://www.healthmeasures.net/index.php?option=com_content&view=category&layout=blog&id=164&Itemid=1133 "HealthMeasures (also known as the Person-Centered Assessment Resource) is a grant from the National Institutes of Health (NIH) to expand and automate use of four state-of-the-science measurement systems: PROMIS®, NIH Toolbox®, Neuro-QoL, and ASCQ-Me®."
 [`readOnly`]:{{site.data.fhir.path}}questionnaire-definitions.html#Questionnaire.item.readOnly  "An indication, when true, that the value cannot be changed by a human respondent to the Questionnaire."
 [Argonaut Questionnaire Test Renderer]: http://gettingstarte-cjfwz-env.us-west-2.elasticbeanstalk.com/
 [modifier extension]: {{site.data.fhir.path}}extensibility.html#modifierExtension "An extension that modifies the meaning of the element that contains it. Typically, this means information that qualifies or negates the primary meaning of the element that contains it."
 [described above]: #get-next-question
