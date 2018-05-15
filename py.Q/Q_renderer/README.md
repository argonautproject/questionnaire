# FHIR-FlaskApp
Test python flask application that acts as an intermediate server for FHIR Searches and Operations.  Fetches resources from the FHIR reference server.

Works best with Postman or Fiddler.

#### The FHIR endpoint is: `http://testpy-env.us-west-2.elasticbeanstalk.com`

Examples

Get a Patient by id:

`GET http://testpy-env.us-west-2.elasticbeanstalk.com/Patient?_id=101`

![Screenshot](Flask-ss1.png)
