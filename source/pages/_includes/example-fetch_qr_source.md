

**Request**

~~~
GET http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse?source=prov-admin1

User-Agent: python-requests/2.20.0
Accept: application/fhir+json
Content-Type: application/fhir+json
[other headers]
~~~

**Response**

~~~
Response Code: 200 (OK)
Content-Type: application/fhir+json; charset=utf-8
[other headers]


{
   "resourceType": "Bundle",
   "id": "urn:uuid:f32aa17a75c8422199796e30761b5c47",
   "meta": {
      "lastUpdated": "2019-02-13T11:34:49.427+00:00"
   },
   "type": "searchset",
   "total": 1,
   "link": [
      {
         "relation": "self",
         "url": "http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse?source=prov-admin1&_snapshot=636856544894273541"
      }
   ],
   "entry": [
      {
         "fullUrl": "http://sqlonfhir-stu3.azurewebsites.net/fhir/QuestionnaireResponse/05b19f1aa2bb42049e0876912ec7880b",
         "resource": {
            "resourceType": "QuestionnaireResponse",
            "id": "05b19f1aa2bb42049e0876912ec7880b",
            "meta": {
               "versionId": "1",
               "lastUpdated": "2019-02-13T11:28:34.913+00:00",
               "profile": [

        ...[snipped for brevity]....

          "authored": "2019-02-13T00:39:38.320181Z",
          "author": {
              "reference": "Practitioner/prov-admin1"
          },
          "source": {
              "reference": "Practitioner/prov-admin1"
          },

        ...[snipped for brevity]....



~~~
