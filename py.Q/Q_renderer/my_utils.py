from json import load, dumps
from requests import get, post, put
from fhirclient.models import questionnaireresponse as QR
import logging
# logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')


out_path = '/Users/ehaas/Documents/FHIR/Argo-Questionnaire/source/examples/'

def write_file(name, data, path=out_path): # write file
    with open('{}{}.json'.format(path,name), 'w') as f:
        f.write(data)
        logging.info('wrote {} to {}'.format(name, path))



# *********************** update Resource on FHIR Server  ********************************
def update_to_server(r_json, type, profile, qr_id=None):

    fhir_test_server = 'http://sqlonfhir-stu3.azurewebsites.net/fhir'

    headers = {
            'Accept':'application/fhir+json',
            'Content-Type':'application/fhir+json'
            }
    params = {
    'profile': profile
    }
    if qr_id == None:
        #   r = requests.post('https://httpbin.org/post', data = {'key':'value'})
        r = post('{}/{}'.format(fhir_test_server,type),
                params = params,
                headers = headers,
                data = r_json )
        # print(r.status_code)
        # view  output
    else:
        #   r = requests.post('https://httpbin.org/post', data = {'key':'value'})
        r = put('{}/{}/{}'.format(fhir_test_server,type,qr_id),
                params = params,
                headers = headers,
                data = r_json )
        # print(r.status_code)
        # view  output
    return r


if __name__ == "__main__": # test
    write_file(path=out_path,name ='SamplerResponse-containedPatient',data = 'foo')
    update_to_server(r_json='foo', type='QuestionnaireResponse', profile = 'profile')
