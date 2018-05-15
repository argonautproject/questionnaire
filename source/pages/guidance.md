---
title: Scenario 1
layout: default
active: guidance
---

{:.no_toc}

<!-- TOC  the css styling for this is \pages\assets\css\project.css under 'markdown-toc'-->

* Do not remove this line (it will not be displayed)
{:toc}

## Introduction

The Argonaut Questionnaire Implementation Guide defines a series of interactions which cover the basic workflow for the creation, discovery and retrieval of simple text-based forms using FHIR Questionnaire and QuestionnaireResponse. By using a basic user Scenario that defines the Argonaut Questionnaire project, the basic workflow steps and API are detailed below.  This guidance covers more basic scenarios (for example, a form shared within and organization) and can be scaled up towards more complex scenarios ( for example, see [Structured Data Capture Initiative]).

## Scenario 1

This simple scenario serves as an effective means to describe the Argonaut Questionnaire basic workflow and API

~~~ text
A Jurisdiction (e.g, state or region) publicly funds a program to improve population health.  The program is instituted and a set of standard assessments are to filled out by the program participants (“subjects”) periodically in order to monitor the program’s success or failure.

Example list of Assessment Categories:

Demographic information
Physical health review
Substance use review
Housing assessment  
Suicide risk assessment  
Universal screening using depression screening (PHQ 2 & 9)
...

Each assessment tool (i.e., set of questions and answer choices) is created once as FHIR Questionnaires and centrally stored in an “Assessment Bank” which can be accessed the program participants (provider EHRS). The provider can then use them to create online questionnaires for their patients.  The responses are captured as QuestionnaireResponse and are scored, stored, shared, aggregated and analyzed by the Agency overseeing the program.
~~~



example how to use a button to expand an inline example....

{% include examplebutton.html example="foo" %}


{%include link-list.md %}
