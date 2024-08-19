from json import load, dumps
from requests import get, post, put, patch
from fhirclient.models import questionnaireresponse as QR
import logging

# logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

headers = {
            'Accept':'application/fhir+json',
            'Content-Type':'application/fhir+json'
            }

patch_headers = {
            'Content-Type': "application/json-patch+json"
            }


# fhir_test_server = 'http://sqlonfhir-stu3.azurewebsites.net/fhir'
out_path = '/Users/ehaas/Documents/FHIR/Argo-Questionnaire/source/examples/'

def write_file(name, data, path=out_path): # write file
    with open('{}{}.json'.format(path,name), 'w') as f:
        f.write(data)
        logging.info('wrote {} to {}'.format(name, path))



# *********************** update Resource on FHIR Server  ********************************
def update_to_server(fhir_server, r_json, type, profile=None, r_id=None):
    '''update or create FHIR object to FHIR server. 
       If no r_id then will POST (create).
       If r_id present then will PUT (update)
    '''
    try:
            params = {
        'profile': profile
        }
    except NameError:
            params = None

    if r_id == None:
        #   r = requests.post('https://httpbin.org/post', data = {'key':'value'})
        r = post('{}/{}'.format(fhir_server,type),
                params = params,
                headers = headers,
                data = r_json )
        # print(r.status_code)
        # view  output
    else:
        #   r = requests.post('https://httpbin.org/post', data = {'key':'value'})
        r = put('{}/{}/{}'.format(fhir_server,type,r_id),
                params = params,
                headers = headers,
                data = r_json )
        # print(r.status_code)
        # view  output
    return r

# *********************** Patch Resource on FHIR Server  ********************************
def patch_to_server(fhir_server, patch_json, type, r_id, profile=None, ):
    '''Patch FHIR object to FHIR server
    '''
    try:
        params = {
        'profile': profile
        }
    except NameError:
        params = None
        #   r = requests.patch(url, params={key: value}, args)
        r = patch(f'{fhir_server}/{type}/{r_id}',
                headers = patch_headers,
                patch = r_json )
        # print(r.status_code)
        # view  output
    return r


if __name__ == "__main__": # test
    write_file(path=out_path,name ='SamplerResponse-containedPatient',data = 'foo')
    update_to_server(r_json='foo', type='QuestionnaireResponse', profile = 'profile')
