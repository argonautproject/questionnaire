# FHIR-FlaskApp

The test python flask application demonstrates the implementation of the Argonaut questionnaire implementation guide.  It fetches a questionnaire from a FHIR reference server, renders them as online forms using HTML5 and Flask based templatesm and displays the completed forms.  Both single page forms and adaptive forms are demonstrated.  In addition to rendering questionnaires and results, the application calculates scores, self documents each step and renders the relevent FHIR artifacts in serialized JSON.  

It is based on python 3.4 Flask library and functionally as a "FHIR Facade" interacting with a FHIR STU3 reference server retrieving and storing data to the server using FHIR RESTful interactions.

Application is currently down and undergoing maintenance

