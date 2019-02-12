#! /usr/bin/env python3.4

# ========================== imports =========================
from flask import Flask, request, render_template, Markup, url_for, session, redirect, flash
from werkzeug.contrib.cache import SimpleCache
import requests
import json
from datetime import datetime
from pdb import set_trace as bp
import fhirtemplates as f
import aq_gets as aq
import fhirclient.models.questionnaire as Q
import fhirclient.models.questionnaireresponse as QR
import fhirclient.models.valueset as VS
import fhirclient.models.fhirdate as FD
import fhirclient.models.quantity as QT
# import fhirclient.models.codeableconcept as CC
import fhirclient.models.coding as C
import fhirclient.models.fhirreference as Ref
import fhirclient.models.extension as Ext
import fhirclient.models.period as P
import logging
from logging.handlers import RotatingFileHandler

from fhirclient.models.fhirabstractbase import FHIRValidationError

# from googletrans import Translator # unavailable for 3.4 as a pip install


application = Flask(__name__)
application.secret_key = 'you-will-never-guess'

# -=================== globals constants used across sessions=============================
cache = SimpleCache()
# ref_server = 'http://test.fhir.org/r3/' # fhir reference serv≠er
ref_server = 'http://sqlonfhir-stu3.azurewebsites.net/fhir/'
ref_server_name = 'Telstra'
quantity = QT.Quantity()  # for Quantity type answers
no_answer = [[''],[],None,['0'],['0', '']]
# item.type to valueType conversion
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
    'attachment': 'valueAttachment',
    'reference': 'valueReference',
    'quantity': 'valueString',  # TODO need to fix this
    'choice': 'valueCoding',
    'open-choice': 'valueCoding'  # TODO need to fix this
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


# note choice can be many types  and open-choice can be a value string too do string for now  TODO add other types

# ==================== defs =================================

def reset_variables(): # reset session reset_variables for new questionnaire
    reset_q_cache()
    reset_aqr_cache()


def reset_q_cache(): # reset ALL session variables for new questionnaire
    session['t_score'] = 0
    session['std_dev'] = 0.0
    session['responses'] = ''
    session['narr_list'] = []




def reset_aqr_cache(): # reset session variables for new adaptive questionnaire
    session['q_num'] = 0
    session['name'] = 'Initialize AQ'
    session['intro'] = ''
    session['narr_list'] = []
    session['current_aqr'] = {}
    session['step'] = 0


def t0(arg):
    pass
    return(arg)

def t1(arg):
    return(arg == 'True')


def t2(arg):
    try:
        arg = arg.split(".")[0]
    except AttributeError:
        pass
    try:
        return(int(arg))
    except ValueError:
        return('not a number')


def t3(arg):
    try:
        return(float(arg))
    except ValueError:
        return('not a decimal')


def t4(arg):
    try:
        return(FD.FHIRDate.with_json(arg))
    except:
        return('not a date')


def t9(arg):
    quantity.value = t3(arg)
    return()


def t10(arg):
    quantity.unit = arg
    return()


def hidden(item):
    try:
        for ext in item.extension:
            if ext.url == 'http://hl7.org/fhir/StructureDefinition/questionnaire-hidden' and ext.valueBoolean == True:
                return(True)
    except TypeError:
        pass
    return(False)

def set_narr(xhtml,**kwargs): #  generate narrative list for text element
    l = session['narr_list']
    l.append(xhtml.format(**kwargs))
    session['narr_list'] = l


def pop_to_front():  #resort narrative so score elements first
    l = session['narr_list']
    if len(l) > 4:
        for i in reversed(range(4)):
            l[i]=l.pop()
    return()


def record_score(aqr): # and std_dev in item[0] and [1]
    item_list = aq.get_item_list(aqr.contained[0], 0) # get cq item
    get_qr_items(session['t_score'], item_list, aqr.item, 0) # get score
    item_list = aq.get_item_list(aqr.contained[0], 1) # get cq item
    get_qr_items(session['std_dev'],  item_list, aqr.item, 1) # get std_dev
    return()



def calc_score(score, std_dev):
    try:
        session['t_score'] = session['t_score'] + int(score)
        session['std_dev'] = round(session['t_score']/10.0, 2)

    except (TypeError, ValueError):  # not a number or no extension
        pass
    return()


def get_score(item, choice=None):
    if choice is None:  # look for score in item
        application.logger.info('===========look for scoring at {}  =========== '.format(item))
        return(get_decimal(item))
    else:  # look for scoring on choices
        application.logger.info('===========look for scoring at {}  =========== '.format(choice))
        for item_option in item.option:
            try:
                if choice.startswith(item_option.valueCoding.display):
                    decimal_score = get_decimal(item_option)
                    application.logger.info('=========== decimal_score =={}  =========== '.format(decimal_score))
                    if decimal_score is None:
                        application.logger.info('=========== score == None , try extension on valueCoding =========== ')
                        return(get_decimal(item_option.valueCoding))
                    else:
                        return(decimal_score)
            except AttributeError:
                if choice == item_option.valueString:
                    return(get_decimal(item_option))
    application.logger.info('=========== score == None  =========== ')
    return()


def get_decimal(item):
    try:
        for ext in item.extension:
            if ext.url == 'http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/extension-score':
                    application.logger.info('===========ext = {}  score = {} =========== '.format(ext.url,ext.valueDecimal))
                    return(ext.valueDecimal)
            elif ext.url == 'http://hl7.org/fhir/StructureDefinition/valueset-ordinalValue':
                    application.logger.info('===========ext = {}  score = {} =========== '.format(ext.url,ext.valueDecimal))
                    return(ext.valueDecimal)
    except TypeError:
        logging.info('===========no extensions ===========')
    logging.info('===========no scores ===========')
    # no explicit return so will be None


def get_uncoded_results(answer, value_type, score, std_dev): #get answers base on results
    # type conversion operations
    type_conversion = {
         'valueString': t0,
         'valueUri': t0,
         'valueBoolean': t1,
         'valueInteger': t2,
         'valueDecimal': t3,
         'valueDate': t0,
         'valueDateTime': t0,
         'valueTime': t0,
         'valueQuantity': t0, # TODO fix
         'valueUnits': t10
         }
    application.logger.info('=========== {} = {} = {} = {} =========== '.format(value_type,answer,score, std_dev))

    answer = type_conversion[value_type](answer) #convert answer
    qr_answer = QR.QuestionnaireResponseItemAnswer({value_type : answer})
    application.logger.info('=========== qr_answer = {}=========== '.format(qr_answer.as_json()))
    session['responses'] = '{r}<strong>Response:</strong> {a}<br />'.format(r=session['responses'], a=answer) # get gen narrative info
    set_narr('<strong>Response:</strong> {a}<br />',a=answer) # create narrative text elements as a cached list to join later
    calc_score(score, std_dev)
    return(qr_answer)


def get_coded_results(answer, score, std_dev):
    application.logger.info('=========== try to split =========== ')

    try:
        display, system, code = answer.split('|')
        qr_answer = QR.QuestionnaireResponseItemAnswer({'valueCoding':{'code':code, 'system':system, 'display':display} })
        application.logger.info('=========== qr_answer = {}=========== '.format(qr_answer.as_json()))
        session['responses'] = '{r}<strong>Response:</strong> {d} ( code = {c}, codesystem = {s})<br />'.format(r=session['responses'], d=display, c=code, s=system) # get gen narrative info
        set_narr('<strong>Response:</strong>  {d} ( code = {c}, codesystem = {s})<br />',d=display, c=code, s=system) # create narrative text elements as a cached list to join later
        calc_score(score, std_dev)

        return(qr_answer)

    except ValueError: # default to string
        application.logger.info('=========== {} is a string! =========== '.format(answer))
        return(get_uncoded_results(answer, 'valueString', score, std_dev))


def get_answers(item, qr_item): # q item: need type and linkId and answer list?
    if qr_item.answer == None:
        qr_item.answers =[]
    # For choice and open-choice assume coding and except for string, look up scores based on Qid
    try:
        value_type = answer_type[item.type]
        answers = request.form.getlist(item.linkId)

        session['responses'] = '{r}<br /> <strong>Question:</strong> (linkID={l}) {q}<br />'.format(r=session['responses'], l=qr_item.linkId, q=qr_item.text ) # get gen narrative info
        set_narr('<br /> <strong>Question:</strong> (linkID={l}) {q}<br />',l=qr_item.linkId, q=qr_item.text ) # get gen narrative info


        application.logger.info('=========== answers = {}=========== type = {}'.format(answers, value_type))

        if answers in no_answer:
            application.logger.info('=========== not an answer! =========== ')
        elif value_type == 'valueCoding':  # get checkbox and radio button answers
            application.logger.info('=========== is a coding! =========== ')
            for answer in answers:
                application.logger.info('=========== get next answer! =========== ')
                # score = get_score(item, answer)
                # application.logger.info('=========== score = =========== '.format(score))
                qr_item.answer.append(get_coded_results(answer, get_score(item, answer)))
                # application.logger.info('=========== calc score =========== ')
                # calc_score(item,answer)

        else:
            application.logger.info('=========== not an  coded answer! =========== ')
            for answer in answers:
                # score = get_score(item, answer)
                # application.logger.info('=========== score = =========== '.format(score))
                qr_item.answer.append(get_uncoded_results(answer, value_type, get_score(item)))
                application.logger.info('=========== calc score =========== ')
                # calc_score(item)
    except KeyError: # not a question typei
        if item.type != 'group':
            session['responses'] = '{r}<br /><strong>{d}</strong><br />'.format(r=session['responses'], d=qr_item.text, ) # get gen narrative info
            set_narr('<br /> <strong>Question:</strong> (linkID={l}) {q}<br />',l=qr_item.linkId, q=qr_item.text) # get gen narrative info)


def get_qr_items(results, item_list, qr_item_list, position=None):  #render QR.item based on Q.item  loop through each item group and nested item using recursion and copy structure and display

    for item in item_list:
        qr_item = QR.QuestionnaireResponseItem(strict=False)
        qr_item.linkId = item.linkId
        qr_item.definition = item.definition
        # display if present and indicate if should be hidden.
        if hidden(item):
            qr_item.text = '{} (this is hidden text/should not be displayed to the user)'.format(item.text)
        else:
            qr_item.text = item.text



        # For choice and open-choice assume coding and except for string, look up scores based on Qid
        try:
            value_type = answer_type[item.type]
            session['responses'] = '{r}<br /> <strong>Question:</strong> (linkID={l}) {q}<br />'.format(r=session['responses'], l=qr_item.linkId, q=qr_item.text, ) # get gen narrative info
            set_narr('<br /> <strong>Question:</strong> (linkID={l}) {q}<br />', l=qr_item.linkId, q=qr_item.text ) # get gen narrative info

            qr_item.answer = []
            try:
                answers = results.getlist(item.linkId)
            except AttributeError:
                answers = [results]

            application.logger.info('=========== answers = {}=========== type = {}'.format(answers, value_type))

            if answers in no_answer:
                application.logger.info('=========== not an answer! =========== ')
            elif value_type == 'valueCoding':  # get checkbox and radio button answers
                application.logger.info('=========== is a coding! =========== ')
                for answer in answers:
                    application.logger.info('=========== get next answer! =========== ')
                    # score = get_score(item, answer)
                    # application.logger.info('=========== score = =========== '.format(score))
                    qr_item.answer.append(get_coded_results(answer, get_score(item, answer), session['std_dev']))
                    application.logger.info('=========== calc score =========== ')
                    # calc_score(item,answer)

            else:
                application.logger.info('=========== not an  coded answer! =========== ')
                for answer in answers:
                    # score = get_score(item, answer)
                    # application.logger.info('=========== score = =========== '.format(score))
                    qr_item.answer.append(get_uncoded_results(answer, value_type, get_score(item), session['std_dev']))
                    application.logger.info('=========== calc score =========== ')
                    # calc_score(item)i

        except KeyError: # not a question type
            if item.type != 'group':
                session['responses'] = '{r}<br /><strong>{d}</strong><br />'.format(r=session['responses'], d=qr_item.text, ) # get gen narrative info
                set_narr('<br /><strong>{d}</strong><br />',d = qr_item.text) # get gen narrative info

        try:  # replace item in list
            qr_item_list[position]=qr_item
        except  (IndexError,TypeError):
            qr_item_list.append(qr_item)  # append item object to qr_item_list
            application.logger.info('***************item.linkId = {}\n ***************item.type = {}\n ***************qr_item.as_json() = {}\n ***************qr_item_list={}\n\n'.format(item.linkId, item.type, qr_item.as_json(), qr_item_list))

        try:
            qr_item.item = [] # init item object to qr_item_list
            get_qr_items(results, item.item, qr_item.item)  # get subitems
        except TypeError:
            pass
    return()


def get_responseperiod_x(start,end):

    responseperiod_x = Ext.Extension()
    responseperiod_x.url = 'http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/extension-responsePeriod'
    responseperiod_x.valuePeriod = P.Period()
    responseperiod_x.valuePeriod.start = FD.FHIRDate(start)
    responseperiod_x.valuePeriod.end = FD.FHIRDate(end)
    return responseperiod_x


def pop_option(q, item):
        if item.options.reference.startswith('#'):
            # get contained contained VS
            for ci in q.contained:
                application.logger.info('contained item = '.format(ci))

                if '#{}'.format(ci.id) == item.options.reference:
                    vs = ci  # get contained VS
        else:
            vs_url = '{}{}'.format(ref_server, item.options.reference)  # external VS
            vs = VS.ValueSet(get_res(vs_url))  # get VS from reference server
        item.options = None  # remove options from item
        item.option = []
        for contain in vs.expansion.contains:
            application.logger.info('contain = {}'.format(contain.as_json()))
            valuecoding = getcoding(contain.code, contain.system, contain.display, contain.extension)
            option = Q.QuestionnaireItemOption({'valueCoding': valuecoding.as_json()})  # add extensions # TODO:
            item.option.append(option)
        return(item.option)


def get_options(q):  # get contained or external valuesets and populate option.valueCoding  assuming the codes are in the expansion only gos two layers deep
    for item in q.item:
        application.logger.info('item = {}'.format(item.as_json()))
        try:
            item.option = pop_option(q, item)
        except AttributeError:
            pass
        try:
            for sub_item in item.item:
                try:
                    sub_item.option = pop_option(q, sub_item)
                except AttributeError:
                    pass
        except TypeError:
            pass
    return(q)


def getcoding(code, system, display, extension):  # fhircoding
    coding = C.Coding()
    # attempt to fix this using the standard Argo extension made more difficult. easier to support both especially when contained vs.
    try:
        for ext in extension:
            if ext.url == 'http://hl7.org/fhir/StructureDefinition/valueset-ordinalValue':
                ext.url = 'http://hl7.org/fhir/StructureDefinition/valueset-ordinalValue'
        coding.extension = extension
    except TypeError:  # extension missing
        pass
    try:
        coding.code = code
        coding.display = display
        coding.system = system
    except TypeError:  # coding missing
        pass
    return(coding)


def set_cache(cache_id,value):  # get Q  from FHIR Server save as python model (published version) and working version
    cache.set(cache_id, value, timeout=5 * 60)  # add to cache
    application.logger.info('{} now in cache!'.format(cache_id))
    return()  # TODO add trys to catch exceptions


def get_q(request):
    form_url = request.form['options']
    session['form_url'] = form_url
    application.logger.info('form_url = {} '.format(form_url ))
    application.logger.info('get cache = {} '.format(cache.get(form_url)))
    if not cache.get(form_url):  # cache value is empty
        r = requests.get(form_url, headers=f.headers, params={})
        q =Q.Questionnaire(r.json())
        set_cache(form_url,q)  # get questionnaire from server as json and display create a link to the main menu how to return to main menu
        # q = translate_res(q,request.form.get('translate', None)) # translate q to the language in translate code. not available in 3.4 for AWS deployment
        q = get_options(cache.get(form_url))  # if options from external or contained VS then need to fetch valuesets and populate option.coding with the values...
        set_cache('{}_wq'.format(form_url), q)  # get questionnaire from server as json and display create a link to the main menu how to return to main menu
    # application.logger.info('=================\n q = {} \n============='.format(q.as_json()))
    # application.logger.info('title = {} and qs = {}'.format(q.title, q.item))
    # bp()  # this is a break
    return()


# ===================== Not available in python 3.4 for AWS deployment ===============
#def translate_element(t_source):
#   t = Translator()
#   '''
#   foo = t.translate('Hello',src='en', dest='es')
#   print(foo)
#   '''
#   try:
#       t_target = t.translate(t_source, src='en', dest='es').text
#       application.logger.info('Hola mi amigos : translate {} to {}'.format(t_source, t_target))
#       return(t_target)
#   except TypeError:
#       return(t_source)
#
#
#
#def translate_res(res, code):  # translate to language code
#   application.logger.info("translate to {} !!!".format(code))
#   if code: # translate
#       application.logger.info("translate to {} !!!".format(code))
#       # go through and add extensions for displayed text to language worry about the contained vs later
#       # start with the title
#       res.title = translate_element(res.title)
#       for item in res.item:
#
#           item.text = translate_element(item.text)
#           try:
#               for sub_item in item.item:
#                   sub_item.text = translate_element(sub_item.text)
#                   try:
#                       for sub_item_choice in sub_item.option:
#                           sub_item_choice.valueString = translate_element(sub_item_choice.valueString)
#                   except TypeError:
#                       pass
#           except TypeError:
#                   pass

#          create an extension on the element o wait I can't :-( since it is a primitivo.
#    return(res)
# ==========================================================================================


@application.route('/')
def index():
    reset_variables()
    return render_template('index.html', ref_server_name=ref_server_name, ref_server=ref_server)


@application.route('/q_view', methods=['GET', 'POST'])  # decorator to map to form view
def q_view():
    session['q_starttime'] = '{}Z'.format(datetime.utcnow().isoformat()) # start-time as FHIRdate
    error = None
    # q = None  # for local file to start
    application.logger.info('request.form.get("adaptive", None) = {} request.values = {}'.format(request.form.get('adaptive', None),request.values))
    if request.method == 'POST':
        get_q(request)
        if request.form.get('adaptive', None):
            if session['form_url'] == 'http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire/questionnaire-example-housing':
                flash('Unable to create and adaptive questionnaire with this form. Please try again!') #flash error
                return redirect(url_for('index'))
            return aq_view()
        else:
            working_q = '{}_wq'.format(session['form_url'])
            q = cache.get(working_q)
            return render_template('q_view.html', q = q)
    reset_aqr_cache()
    working_q = '{}_wq'.format(session['form_url'])
    q = cache.get(working_q)
    return render_template('q_view.html', q = q)


@application.route('/qjson_view', methods=['GET', 'POST'])  # decorator to map json
def qjson_view():
    q = cache.get(session['form_url'])
    return render_template('qjson_view.html', q=json.dumps(q.as_json(), indent=4, sort_keys=True))


@application.route('/qr-view', methods=['GET', 'POST'])  # decorator to map to answers
def qr_view():
    working_q = '{}_wq'.format(session['form_url'])
    qr_working_q = cache.get(working_q)

    reset_q_cache()
    # results = request.form  # this is multiDict structure - can only retreive the first element or use the get list method
    application.logger.info('results = {}'.format(request.form))
    # bp()  # ***************** this is a break******************

    # split out linkId and text to create answers create a QR resource use a template for the meta for now

    qr = QR.QuestionnaireResponse(f.qr_templ, strict=False)
    qr.questionnaire = Ref.FHIRReference({'reference': qr_working_q.url}) # update the questionnaire
    qr.id = qr_working_q.url.rsplit('/')[-1].replace('questionnaire', 'questionnaireresponse')  # update the QR id
    dt = '{}Z'.format(datetime.utcnow().isoformat())  # == stop time
    qr.extension = [get_responseperiod_x(session['q_starttime'],dt)]    # add extension for FHIRDates start and stoptime
    qr.authored = FD.FHIRDate(dt)  # update datetime
    # application.logger.info(json.dumps(qr.as_json(), indent=4, sort_keys=True))
    qr.item = []
    get_qr_items(request.form, qr_working_q.item, qr.item)

    #application.logger.info(json.dumps(qr.as_json(), indent=4, sort_keys=True))

    # ---create narrative---
    qr.text.div = '''<div xmlns=\"http://www.w3.org/1999/xhtml\">
    <h3>Response Summary</h3>
    <strong>Questionnaire URL:</strong> {q}<br />
    <strong>Date Completed:</strong> {d}<br />
    <hr /> {r} <br /><br />
    </div>'''.format(q=qr.questionnaire.reference, d=qr.authored.as_json(), r=''.join(session['narr_list']))

    # bp()  # ***************** this is a break******************
    return render_template('qr_view.html', qr=qr, qr_string=json.dumps(qr.as_json(), indent=4, sort_keys=True), adaptive=False )

@application.route('/post_answers', methods=['GET', 'POST'])  # decorator to post to answer bank
def a_bank():
    return render_template('a_bank.html',ref_server_name = ref_server_name, ref_server = ref_server)

@application.route('/aq_view' , methods=['GET', 'POST']) #decorator to view adaptive questionnaire
def aq_view(): # client view
    working_q = '{}_wq'.format(session['form_url'])
    q = cache.get(working_q)
    try:
        d=q.date.as_json()
    except AttributeError:
        d=None
    session['intro'] = aq.intro.format(t=q.title, q=q.url, d=d, c=q.copyright)
    # logging.info('intro={}'.format(intro))
    # global current_aqr  # current state of aqr as model ( this is not strictly a stateless implementation)
    # aqr = current_aqr #update local copy
    try:
        aqr = QR.QuestionnaireResponse(session['current_aqr'])
    except FHIRValidationError:  # if current state of aqr is empty (i.e., no status )i
        reset_q_cache() #reset the score and narrative
        name = "Initialize AQ"
        aqr = aq.init_aqr(q)
        #j = aq.get_new_question(aqr) #get new question to display
        session['current_aqr']=aqr.as_json() # update session
        session['step'] = session['step'] + 1
        return render_template('aq_view.html', aqr=json.dumps(aqr.as_json(), indent=4, sort_keys=True), j=None, narr =''.join(session['narr_list']))

    logging.info(json.dumps(aq.get_next_q(q,aqr,session['t_score']).as_json(), indent=3))  # ****DON'T REMOVE -- fetches the next q and updates the score
    if aqr.item == None:
        aqr.item = []
    record_score(aqr) # and std_dev
    application.logger.info('aqr as dict ={}'.format(aqr.as_json()))

    session['current_aqr']=aqr.as_json() # update session

    if aqr.status == 'complete':  # done!!!
        # add response period extension
        dt = '{}Z'.format(datetime.utcnow().isoformat())  # == stop time
        aqr.extension = [get_responseperiod_x(aqr.authored.as_json(),dt)]
        pop_to_front() # resort narrative
        session['step'] = session['step'] + 1
        # change this to join
        aqr.text.div = '{}<hr>{}'.format(session['intro'],''.join(session['narr_list'])) # add q-as to narrative
        # aqr.text.div = '{i}{r}'.format(i=aqr.text.div,r=session['responses']) # add q-as to narrative
        #application.logger.info('aqr as dict ={}'.format(aqr.as_json()))
        return render_template('qr_view.html', qr=aqr, qr_string=json.dumps(aqr.as_json(), indent=4, sort_keys=True), adaptive=True)
        # TODO use PRG pattern so doesn't update on refresh

    j = aq.get_new_question(aqr) #get new question to display
    pop_to_front() # resort narrative
    session['step'] = session['step'] + 1
    return render_template('aq_view.html', aqr=json.dumps(aqr.as_json(), indent=4, sort_keys=True), j=j, narr =''.join(session['narr_list']))

@application.route('/update_aqr',methods=['GET', 'POST'])  # decorator to update the aqr with the next answer
def update_aqr(): #server view
    aqr = QR.QuestionnaireResponse(session['current_aqr'])

    results = request.form  # get answer

    # add to aqr

    item_list = aq.get_item_list(aqr.contained[0], session['q_num']+2) # get cq item

    if aqr.item == None:
        aqr.item = []
    #record_score(aqr) # and std_dev

    get_qr_items(results,item_list,aqr.item)

    session['step'] = session['step'] + 1
    session['current_aqr']=aqr.as_json() # update session
    session['q_num'] = session['q_num'] + 1 # next question

    return render_template('aq_view.html', aqr=json.dumps(aqr.as_json(), indent=4, sort_keys=True), j=None, narr =''.join(session['narr_list']))

# return to aq view
    # return render_template('qr_view.html', qr=qr, qr_string=json.dumps(qr.as_json(), indent=4, sort_keys=True), t_score=session['t_score'] )

# run the application.i
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production application
        # initialize the log handler
    logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)

    # set the log handler level
    logHandler.setLevel(logging.INFO)

    # set the app logger level
    application.logger.setLevel(logging.INFO)

    application.logger.addHandler(logHandler)

    application.logger.info('End of program')
    application.debug = True
    application.jinja_env.auto_reload = True
    application.run()
