

**Request**

~~~
http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire?_id=questionnaire-example-sampler

User-Agent: python-requests/2.20.0
Accept: application/fhir+json
Content-Type: application/fhir+json
...[other headers]...
~~~

**Response**

~~~
Response Code: 200
Content-Type: application/fhir+json; charset=utf-8
Content-Location: http://sqlonfhir-stu3.azurewebsites.net/fhir/Bundle/urn:uuid:5bf3f67eb3874358851cec9fd2b344fb
...[other headers]...

    
{
    "resourceType": "Bundle",
    "id": "ab6f9ad0-a72d-43e5-aa4d-3f5521d9dfbe",
    "meta": {
        "versionId": "1",
        "lastUpdated": "2019-02-12T22:00:07.666-05:00"
    },
    "type": "searchset",
    "total": 7,
    "link": [
        {
            "relation": "self",
            "url": "http://wildfhir.aegis.net/fhir3-0-1/Questionnaire"
        }
    ],
    "entry": [
        {
            "fullUrl": "http://wildfhir.aegis.net/fhir3-0-1/Questionnaire/questionnaire-cqif-example",
            "resource": {
                "resourceType": "Questionnaire",
                "id": "questionnaire-cqif-example",
                "meta": {
                    "versionId": "1",
                    "lastUpdated": "2017-12-08T13:41:48.148-05:00",
        ...[snipped for brevity]....
      
~~~
