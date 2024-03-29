#! /usr/bin/env python3.4

# ========================== imports =========================
import json
import random
from datetime import datetime
from pdb import set_trace as bp
import fhirtemplates as f
import fhirclient.models.questionnaire as Q
import fhirclient.models.questionnaireresponse as QR
import fhirclient.models.fhirdate as FD
import fhirclient.models.quantity as QT
# import fhirclient.models.codeableconcept as CC
import fhirclient.models.fhirreference as Ref
import fhirclient.models.extension as Ext
from fhirclient.models.fhirabstractbase import FHIRValidationError

import logging
# logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
logging.debug('Start of program')
logging.info('The logging module is working.')

intro = '''<div xmlns=\"http://www.w3.org/1999/xhtml\">
    <h3>{t} Adaptive View</h3>
    <p><em>NOTE: These examples are for educational and testing purposes,
     see the form copyright statement and do not redistribute without expressed
     permission from the form author.</em></p>
    <p>This simulates is a simple adaptive questionnaire implementation.
     After answering and submitting the first question another question is randomly
     returned from the selected questionnaire. This is repeated two more times and
     then the adaptive questionnaire will finish by changing the status to completed
     and returning a score. Note that although these questionnaires are designed as forms and
     are not really appropriate for the adaptive questionnaire use case,  they are used here to
      demonstrate a proof of concept implementation.<br />
    <strong>Questionnaire URL:</strong> {q}<br />
    <strong>Date Completed:</strong> {d}<br /><br />
    <em>Copyright: {c}</em></p>
    <hr />'''

qr = QR.QuestionnaireResponse(f.qr_templ)
t_score = ''

answer_type = {
    'boolean': 'valueBoolean',
    'decimal': 'valueDecimal',
    'integer': 'valueInteger',
    'date': 'valueDate',
    'dateTime': 'valueDateTime',
    'time': 'valueTime',
    'string': 'valueString',
    'text': 'valueString',
    'url': 'valueUri',
    'choice': 'valueCoding',
    'open-choice': 'valueCoding', # TODO need to fix this
    'attachment': 'valueAttachment',
    'reference': 'valueReference',
    'quantity': 'valueString',  # TODO need to fix this
}

header = {
    'group': 'Group',
    'display': 'Display',
    'boolean': 'Question',
    'decimal': 'Question',
    'integer': 'Question',
    'date': 'Question',
    'dateTime': 'Question',
    'time': 'Question',
    'string': 'Question',
    'text': 'Question',
    'url': 'Question',
    'attachment': 'Question',
    'reference': 'Question',
    'quantity': 'Question',
    'choice': 'Question',
    'open-choice': 'Question'
}
# note open-choice can be a value string too


def get_aqr_score():
    return(t_score)

def none_filter(input):
    if input == None:
        return('')
    else:
        return(input)


def get_item_list(cq,i):
    item = cq.item[i]
    return([item])


def pop_pop(item,n):  # pop n times
    for i in range(n):
        item.pop(-1)
    return(item)


def get_hidden_score(cq_item):
    q_item = Q.QuestionnaireItem({'linkId': 'score', 'type': 'integer'})
    q_item.text = 'Cumulative Score is ...'
    q_item.repeats = False
    q_item.readOnly = True
    q_item.extension = []
    q_item.extension.append(getextension('http://hl7.org/fhir/StructureDefinition/questionnaire-hidden', 'valueBoolean', True))  # fhirextension
    q_item.extension.append(getextension('http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/extension-itemOrder',
                        'valueInteger', 1))  # fhirextension
    cq_item.append(q_item)
    return()

def get_hidden_stddev(cq_item):
    q_item = Q.QuestionnaireItem({'linkId': 'std_dev', 'type': 'decimal'})
    q_item.text = 'Standard Deviation is ...'
    q_item.repeats = False
    q_item.readOnly = True
    q_item.extension = []
    q_item.extension.append(getextension('http://hl7.org/fhir/StructureDefinition/questionnaire-hidden', 'valueBoolean', True))  # fhirextension
    q_item.extension.append(getextension('http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/extension-itemOrder',
                    'valueInteger', 2))  # fhirextension
    cq_item.append(q_item)
    return()


def get_itemorder(cq_item, o_num):
    try: #assume already has itemOrder
        for ext in cq_item.extension:
            if ext.url == "http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/extension-itemOrder":
                ext.valueInteger = o_num
                ordered = True
        if not ordered:
            cq_item.extension.append(getextension('http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/extension-itemOrder',
                        'valueInteger', 3))  # fhirextension
    except AttributeError:
        cq_item.extension.append(getextension('http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/extension-itemOrder',
                        'valueInteger', 3))  # fhirextension




def get_q_items(q_items, q_items_list=None):  # list of all item with a linkId containing '.q'
    if q_items_list is None:
        q_items_list = []
    for q_item in q_items:
        # print(q_item.linkId)
        if header[q_item.type] == "Question":
            # print(q_item.linkId)
            q_items_list.append(q_item)
        try:
            get_q_items(q_item.item, q_items_list)
        except TypeError:
            pass
    return(q_items_list)


def getextension(url, valuetype, value):  # fhirextension
    ext = Ext.Extension({'url': url, valuetype: value})
    return(ext)  # note this returning as a list!! TODO fix this


def get_next_q_item(q_url, q_items, check_list):  # assuming no nesting to make sure is unique question
    cq_item = random.choice(get_q_items(q_items))
    logging.info('cq_item = {}'.format(cq_item))
    if  cq_item.linkId not in check_list:
        cq_item.definition = '{}-{}'.format(q_url, cq_item.linkId)
        return(cq_item)
    else:  # try again
        return get_next_q_item(q_url, q_items, check_list)


def get_next_q(q, aqr, score=0):  # assuming no nesting
    cq = aqr.contained[0]
    if cq.item is None:  # create first response
        cq.item = []  # use first item
        get_hidden_score(cq.item)  # add score as item 0
        # add score as item 0
        get_hidden_stddev(cq.item)  # add stddev as item 1
        q_item = get_q_items(q.item)[0]
        q_item.definition = '{}-{}'.format(q.url, q_item.linkId)
        # logging.info(q_item.prefix)
        cq.item.append(q_item) # use first question
        get_itemorder(cq.item[2],3)
        cq.copyright = q.copyright
        dt = '{}Z'.format(datetime.utcnow().isoformat())
        cq.date = FD.FHIRDate(dt)
        cq.id = 'contained-adaptive-{}'.format(q.id)
        cq.extension = q.extension
        #cq.title = 'Contained Adaptive {}'.format(q.title)
        #cq.url = q.url
        cq = aqr.contained[0]
        aqr.text.div = intro.format(t=cq.title, c=cq.copyright, q=cq.url, d=cq.date.as_json())  # render intro
    elif len(cq.item) < 5:  # check number of q is < 5 add a new q
        logging.info('cq.item = {}'.format(cq.item))
        check_list =[x.linkId for x in cq.item]
        logging.info('check_list = {}'.format(check_list))
        next_cq_item = get_next_q_item(q.url, q.item, check_list)
        logging.info('next_cq_item = {}'.format(next_cq_item))
        get_itemorder(next_cq_item,len(cq.item)+1)
        cq.item.append(next_cq_item)

    else:
        # done change the status of the QR to complete and add score as a hidden # QUESTION:
        aqr.status = 'completed'


    return(aqr)


def init_aqr(q):
    aqr = QR.QuestionnaireResponse(f.aqr_templ(q.url), strict=False) # resets aqr and contained q
    aqr.questionnaire = Ref.FHIRReference({'reference': '#contained-adaptive-{}'.format(q.id)}) # update the questionnaire
    aqr.id = q.url.rsplit('/')[-1].replace('questionnaire', 'adaptive-questionnaireresponse')  # update the QR id
    dt = '{}Z'.format(datetime.utcnow().isoformat())  # start time...
    aqr.authored = FD.FHIRDate(dt)  # update datetime
    # application.logger.info(json.dumps(qr.as_json(), indent=4, sort_keys=True))
    # ---create narrative  only answered and static questions ---
    logging.info(aqr)
    # get_next_q(q, aqr)
    return(aqr)

def get_new_question(aqr): # assuming a flat list
    cq = aqr.contained[0]
    return(cq.item[-1])
