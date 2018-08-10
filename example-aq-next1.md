

**request**

`POST ../Questionnaire/$next-q`

**payload**

~~~
  {
    "resourceType": "Parameters",
    "id": "next-question-example",
    "parameter": [
      {
        "name": "qa-pairs",
        "part": [
          {
           // first question  = Q-1 answered "foo", with no score returned yet so no score is available.
            "sequence": "1",
            "url": "https\://acme.org/questionnaire/1",
            "answerString": "foo",
          }
        ]
      }
    ]
  }
~~~

**response**

~~~
{
  "resourceType": "Parameters",
  "id": "next-question-example",
  "parameter": [
    {
      "name": "qa-pairs",
      "part": [
        {
         // first question  = Q-1 answered "foo", with no score returned yet so no score is available.
          "sequence": "1",
          "url": "https\://acme.org/questionnaire/1",
          "answerString": "foo",
          "score": {
              "value" : 17,
              "unit" : "points"}
              }
        }
      ],
      "cum-score": 17,
      'q': {
        "resourceType": "Questionnaire",
        "id": "first-question-example",
        "url": "https\://acme.org/questionnaire/4",
        ...
        //assuming a single question item for Q4//
        "item":{
        ...
        "type":"choice"
        "text":"blah4"
        ...
        }

    }
  ]
}
~~~
