

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?context-code=task&value=example

User-Agent: python-requests/2.20.0
Accept: application/fhir+json
Content-Type: application/fhir+json
[other headers]
~~~

**Response**

~~~
Response Code: 200 (OK)
Content-Type: application/fhir+json; charset=utf-8
Content-Location: http://sqlonfhir-stu3.azurewebsites.net/fhir/Bundle/urn:uuid:f43f23115d954cd28716556d7bb26287
[other headers]

    
{
   "resourceType": "Bundle",
   "id": "urn:uuid:f43f23115d954cd28716556d7bb26287",
   "meta": {
      "lastUpdated": "2019-02-13T08:39:00.883+00:00"
   },
   "type": "searchset",
   "total": 67,
   "link": [
      {
         "relation": "self",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?context-code=task&value=example&_snapshot=636856439408835095"
      },
      {
         "relation": "first",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?context-code=task&value=example&_snapshot=636856439408835095"
      },
      {
         "relation": "next",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?context-code=task&value=example&_snapshot=636856439408835095&_page=1"

        ...[snipped for brevity]....
      
~~~
