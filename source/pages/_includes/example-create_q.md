

**Request**

~~~
POST http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire

User-Agent: python-requests/2.20.0
Accept: application/fhir+json
Content-Type: application/fhir+json
[other headers]
~~~

**Response**

~~~
Response Code: 201 (Created)
Content-Type: application/fhir+json; charset=utf-8
Content-Location: http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire/c644fc509ad84aebb8315b4c587bfcd0/_history/1
[other headers]

    
{
   "resourceType": "Questionnaire",
   "id": "c644fc509ad84aebb8315b4c587bfcd0",
   "meta": {
      "versionId": "1",
      "lastUpdated": "2019-02-13T08:03:46.927+00:00",
      "profile": [
         "http://fhir.org/guides/argonaut/questionnaire/StructureDefinition/argo-questionnaire"
      ]
   },
   "text": {
      "status": "generated",
      "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\r\n\t<b>Argonaut Questionnaire Sampler</b>\r\n\t<hr/>\r\n\t\t<span style=\"color: gray;\">Publisher:</span> Argonaut Project\r\n</div>\r\n"
   },
   "extension": [
      {
         "url": "http://fhir.org/guides/argonaut/questionnaire/StructureDefinition/extension-timeLimit",
         "valueDuration": {
            "value": 5,
            "unit": "minute",
        ...[snipped for brevity]....
      
~~~
