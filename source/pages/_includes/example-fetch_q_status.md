

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?status=active

User-Agent: python-requests/2.20.0
Accept: application/fhir+json
Content-Type: application/fhir+json
[other headers]
~~~

**Response**

~~~
Response Code: 200 (OK)
Content-Type: application/fhir+json; charset=utf-8
Content-Location: http://sqlonfhir-stu3.azurewebsites.net/fhir/Bundle/urn:uuid:abcbf2f079c74fab991edf1ad77cdbc6
[other headers]

    
{
   "resourceType": "Bundle",
   "id": "urn:uuid:abcbf2f079c74fab991edf1ad77cdbc6",
   "meta": {
      "lastUpdated": "2019-02-13T08:38:59.852+00:00"
   },
   "type": "searchset",
   "total": 23,
   "link": [
      {
         "relation": "self",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?status=active&_snapshot=636856439398527001"
      },
      {
         "relation": "first",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?status=active&_snapshot=636856439398527001"
      },
      {
         "relation": "next",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?status=active&_snapshot=636856439398527001&_page=1"
      },
      {
         "relation": "last",
        ...[snipped for brevity]....
      
~~~
