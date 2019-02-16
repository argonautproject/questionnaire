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
  - Short answer, narrative and other answer types.

- Provisions for

  - Associating numeric scores for each group of questions or each question or each answer choice.  (How to calculate the total scores can be described as provider instructions )
  -  Whether the question is required
  -  Whether the answer choice is excludes other choices ( for example, a choice of 'none of the above').
  -  Whether the item (for example, provider instructions is hidden)
  -  Indication for how much time is allowed for the questionnaire, group of questions or each question.

### Mandatory Data Elements and Terminology

The following data-elements are mandatory:

**Each Questionnaire must have:**

1. An absolute URI that is used to identify this assessment form when it is referenced by a response (required by SDC )
1. A human friendly title
1. The form's status (base specification requirement)
1. An identifier to link to the response in a QuestionnaireResponse resource  (base specification requirement)
1. A questions type including if a display only  question grouping elements (base specification requirement)

**The system [Must Support] if available:**

1. [Questionnaire Ordinal Value Extension] for use on all answer types and choices.
1. [Argonaut Questionnaire Time Limit Extension] for indicating the duration allowed for all or parts of the assessment.
1. [Questionnaire Hidden Extension] for indicating that the item should not be displayed to the user.
1. [Questionnaire Option Exclusive Extension] A [modifier extension] for indicating that if this option is selected, no other options may be selected.
1. [Argonaut Questionnaire Item Order Extension] for representing the order of questions within Questionnaires groups, groups within groups and groups within questions and the order of answer choices for questions.
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

<!--

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

-->

**Additional Profile specific implementation guidance:**

1. All ValueSets referenced by the `.options` element are [contained] resources in the Questionnaire and require a `ValueSet.expansion`.  This ensures that the Questionnaire will not adopt a new version of the referenced value set without revising the Questionnaire to point to that new version - putting the author of the Questionnaire in control of any changes.

1. `boolean` vs `choice` - In a scenario where the end user has to select simple true/false or active/inactive states the `boolean`item answer type (e.g, a checkbox control) is appropriate.  Where two alternative answers can't be handled with a simple checkbox then a `choice` item answer type is needed. For example, for assigning numeric score values to the individual yes or no answers.
1. `text` vs `string` item types  - `string` item answer types are typically limited to a single line and correspond to the the HTML5 `<input>` element type "text".  The Questionnaire `text` item answer types are intended for multiline answers and correspond to the HTML5 `<textarea>` form attribute.


### Examples

These examples are designed to demonstrate all the supported elements and the extensions defined in the Argonaut Questionnaire Profiles.  *Note that they are for educational and testing purposes, see the form copyright statement and do not redistribute without expressed permission from the form author.*

<!-- {% raw %} {% include list-simple-questionnaires.xhtml %}{% endraw %} -->
- [Sampler](Questionnaire-questionnaire-example-sampler.html) - a Sample form using all the supported question types
- [Sampler with contained Patient](Questionnaire-questionnaire-example-sampler.html) - a Sample form using all the supported question types with a *contained* de-identified patient resource.
- [PHQ-9](Questionnaire-questionnaire-example-phq9.html) - An example demonstrating the use of *contained* value sets for answer choices, decimal scores associated with each value within the valueset.
- [AUDIT-C](Questionnaire-questionnaire-example-audit-c.html) - An example multiple choice form demonstrating the use of *contained* value sets for answer choices, decimal scores associated with each value within the valueset.
- [DAST](Questionnaire-questionnaire-example-dast.html) - An example multiple choice form demonstrating the use of inline codings for answer choices, decimal scores associated with each coding.
- [Housing](Questionnaire-questionnaire-example-housing.html) - An example multiple choice form demonstrating the use of inline strings for answer choices, and 'any of' choice option with the the *exclusive* extension for one of the choices.



{%include link-list.md %}
