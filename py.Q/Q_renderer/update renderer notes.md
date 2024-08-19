


First steps: 
1. updated to FHIR R4 using fhir.resource library ( note to add R4B to all models  when importing  like this `import fhir.resources.R4B.task as T` )
1.  create CSV in `static/my_data.csv` √
1. - import pandas √
1. Post a Task to the form filler just a simple json {'task': '<base_url>Task/<id>'} format for now √
   - create test Task as Gist and reference Test Questionnaire in Gist too.
     - Q: https://gist.githubusercontent.com/Healthedata1/af831e374f818d34ebb25dcdf4b795eb/raw/147e38c6afa7e9c6997c7095d7a93d8069798cde/cdex-test-questionnaire.json
     - Taks: https://gist.githubusercontent.com/Healthedata1/1df23ea72d53f97a3dd8e4771b3de451/raw/ca5ae605df53dc0f6610ee4ff819a0100d87260d/test-cdex-launch-context-task.json
   - Then move to Foundry Servers as load steps and tear down steps.... ( already done? )
   - later mimic the smart app launch see: https://hl7.org/fhir/smart-app-launch/app-launch.html1.launch-app-ehr-launch

    questions:
    - how do you know the base URL for patient and task? from header or from the launch sequence request  - safer to send absolute addresses or use authorization details?
    - What other parameters belong in the fhir Context?



{"need_patient_banner":true,"smart_style_url":"https://smart.argo.run/smart-style.json","patient":"123","fhirContext":[{"reference":"Task/123"}],"token_type":"Bearer","scope":"launch, launch/patient launch/task patient/*.rs patient/Task.u patient/QuestionnaireResponse.cu","expires_in":3600,"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuZWVkX3BhdGllbnRfYmFubmVyIjp0cnVlLCJzbWFydF9zdHlsZV91cmwiOiJodHRwczovL3NtYXJ0LmFyZ28ucnVuLy9zbWFydC1zdHlsZS5qc29uIiwicGF0aWVudCI6Ijg3YTMzOWQwLThjYWUtNDE4ZS04OWM3LTg2NTFlNmFhYjNjNiIsInRva2VuX3R5cGUiOiJiZWFyZXIiLCJzY29wZSI6ImxhdW5jaC9wYXRpZW50IHBhdGllbnQvT2JzZXJ2YXRpb24ucnMgcGF0aWVudC9QYXRpZW50LnJzIiwiY2xpZW50X2lkIjoiZGVtb19hcHBfd2hhdGV2ZXIiLCJleHBpcmVzX2luIjozNjAwLCJpYXQiOjE2MzM1MzIwMTQsImV4cCI6MTYzMzUzNTYxNH0.PzNw23IZGtBfgpBtbIczthV2hGwanG_eyvthVS8mrG4","refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb250ZXh0Ijp7Im5lZWRfcGF0aWVudF9iYW5uZXIiOnRydWUsInNtYXJ0X3N0eWxlX3VybCI6Imh0dHBzOi8vc21hcnQuYXJnby5ydW4vL3NtYXJ0LXN0eWxlLmpzb24iLCJwYXRpZW50IjoiODdhMzM5ZDAtOGNhZS00MThlLTg5YzctODY1MWU2YWFiM2M2In0sImNsaWVudF9pZCI6ImRlbW9fYXBwX3doYXRldmVyIiwic2NvcGUiOiJsYXVuY2gvcGF0aWVudCBwYXRpZW50L09ic2VydmF0aW9uLnJzIHBhdGllbnQvUGF0aWVudC5ycyBvZmZsaW5lX2FjY2VzcyIsImlhdCI6MTYzMzUzMzg1OSwiZXhwIjoxNjY1MDY5ODU5fQ.Q41QwZCEQlZ16M7YwvYuVbUP03mRFJoqRxL8SS8_ImM"}

1. fetch the Task √
   - change from tasks to Task endpoint √
2. read the Task to get the Q URL and title √
  - ignore session id for now.
3. Save the Q URL locally  and title( csv for now /  database later ) √
  - add status field of active/complete or completed flag
  - session_id as timestamp for uniqueness.
4. use the form filler to select the Q  √
   - source Q_renderer/templates/q_menu.html
   - update to use for loop to list all questionnaires in csv in value field
   - cannot pass panda df to jinja templates need to convert to json struct like list of tuples or dicts
   - only single questionnaire for now  -  todo update to latest version of CDex or allow for both versions
   - could display more meta data like the requester, date, status
   - add pop up to display task
   - add required to prevent no option
5. fetch the Q and save locally
 - select q triggers the app def q_view() function √
 - assume the q_url is resolvable...( only absolute urls sent to form filler ) create warning to try again √
 - need to save form, working_q and form_url as separately
   -  session["form_url"]
   -  cache.get(session['form_url']
   - form_url is key to q in cache
   - what is working_q and how is this different? this will continue to bite me!!
 - save to CSV √
   - how do know the session_id ?
   - use form_url use that for indexing instead
   - caching not being saved when start over from home page  - need check if already saved...
 - fix choice rendering √
 - fix json view √, remove xml view for now √
6. fill out the Q and save the QR locally
    -  fill out get error validation error.line pydantic errors. in qr_view using f.qr_templ
    -  fix json display using qr.json()  ( add a yaml button!)
    - sve tp CSV using form_url to start but that may not be unique so Task URL should be unique...except for testing :-?
    - need the Task for patient and source data in QR ...(or save in session?)
    - easier to remove the profile and id before creation and add in later if needed.

7. Post the QR to provider server and update the Task <<<NEXT UP>>>  qr_view
   - how it this transmitted in SMART - ask Josh after a search - need a base_url.
   - for now use the task_url as base url. for dev hard coded as reference server
     - see how works now ... stuggling with typing make all sameeither obj, dict, or json string  easiest to read csv as json
     - save to csv  new 
     - Patch in Task using template  - new 
   - updates
     -  the Task to come from a FHIR endpoint
        -  load to Provider server using Scenario 3 Collection (create a new bundle) √
           1. patient  ("Member123") = identifier
           2. provider ("9941339100") = identifier
           3. organization ("1234567893")  = identifier
           4. Task = dynamically discover id {collection variable}
        -  load to Payer server using Scenario 3 Collection (create a new bundle) √
           1. Patient 
           2. Claim "Claim123"
           3. Questionnaire  (http://example.org/cdex-questionnaire-example1)  for use the gist url to fetch (later in collection dynamically update the url to base_url + id)
        -  serve up from server √
        -  save Task to CSV √
        -  use author and subject from Task and save in session for QR  ( set session vars in when >>>>>REPLACE form_url with unique request_id = timestamp and use csv to look up the url <<<
              -  create a unique session ID = timestamp √
              -  rename session "form_url" to "session_id"
              -  lookup q_urls and task_js in CSV based on session_id
              -  update cache until decide if replace with CSV
              -  
     - get QR path
     - update Task output on server using patch coded!
     - update CSV as completed coded!
 
8. session for temporary data - capture session_id or form_url

9. 
10. fix caching
11. clean up logging
12. figure out how to host multiuser sessions  understand the sessions in Flask
13. Host remotely...Foundry