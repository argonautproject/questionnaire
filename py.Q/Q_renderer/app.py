
# Python 3.7.2
# Updated to FHIR R4 usomg fhir.resources  √
# Provider Smart Launchs with Task context
# Inspect the Task from Provider
# Fetch Q based on the URL from Payer
# Render simple Q for user to complete
# Create QR
# upload to provider server 
# update the provider Task
# 
# to kill process use 'netstat -vanp tcp | grep 5000" to find process id then 'kill -9 ,PID>'
# ========================== imports =========================
from flask import Flask, request, render_template, Markup, url_for, session, redirect, flash, jsonify, abort, make_response
from cachelib import SimpleCache
from datetime import datetime
import pandas as pd
from pathlib import Path
import requests
import json
import io  # don't need?  update to PathLib if needed
from pdb import set_trace as bp
import my_utils
import fhirtemplates as f
# import aq_gets as aq  #>>>>>> DISABLE for now <<<<<<<,
import fhir.resources.R4B.questionnaire as Q
import fhir.resources.R4B.questionnaireresponse as QR
import fhir.resources.R4B.task as T
import fhir.resources.R4B.valueset as VS
# import fhir.resources.R4B.fhirdate as FD
import fhir.resources.R4B.quantity as QT
# import fhir.resources.R4B.codeableconcept as CC
import fhir.resources.R4B.coding as C
import fhir.resources.R4B.reference as Ref
import fhir.resources.R4B.extension as Ext
import fhir.resources.R4B.period as P
import logging
from logging.handlers import RotatingFileHandler
from fhir.resources.R4B.fhirtypesvalidators import ValidationError as FHIRValidationError

# from googletrans import Translator # unavailable for 3.4 as a pip install


app = Flask(__name__)
app.secret_key = 'you-will-never-guess'
app.logger.info(f'=========== Here we go !  =========== ')
app.logger.info(f'=========== cwd  = {Path().cwd()}  =========== ')

# -=================== globals constants used across sessions=============================
cache = SimpleCache()
#ref_server = 'http://test.fhir.org/r3/' # fhir reference server
ref_server = 'https://cdex-payer-server.davinci.hl7.org/fhir/'  #  ! need backslash
ref_server_name = 'CDex Payer'
my_csv_path = Path().cwd() / 'Q_renderer' /'static' / 'my_data.csv'
app.logger.info(f'===========my_csv_path at {my_csv_path}  =========== ')
app.logger.info(f'===========my_csv_path = {pd.read_csv(my_csv_path).head()}  =========== ') 
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
    session['qr_id'] = ''  # this is for saving my examples
    session['profile'] = ''
    df=pd.read_csv(my_csv_path)
    session['q_list'] =  [(r.session_id,r.task_url, r.q_url, r.q_title) for i,r in df.iterrows()]



def reset_aqr_cache(): # reset session variables for new adaptive questionnaire
    session['q_num'] = 0
    session['name'] = 'Initialize AQ'
    session['intro'] = ''
    session['narr_list'] = []
    session['current_aqr'] = {}
    session['step'] = 0
    session['qr_id'] = ''  # this is for saving my examples
    session['profile'] = ''

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
        app.logger.info('===========look for scoring at {}  =========== '.format(item))
        return(get_decimal(item))
    else:  # look for scoring on choices
        app.logger.info('===========look for scoring at {}  =========== '.format(choice))
        for item_option in item.answerOption:
            try:
                if choice.startswith(item_option.valueCoding.display):
                    decimal_score = get_decimal(item_option)
                    app.logger.info('=========== decimal_score =={}  =========== '.format(decimal_score))
                    if decimal_score is None:
                        app.logger.info('=========== score == None , try extension on valueCoding =========== ')
                        return(get_decimal(item_option.valueCoding))
                    else:
                        return(decimal_score)
            except AttributeError:
                if choice == item_option.valueString:
                    return(get_decimal(item_option))
    app.logger.info('=========== score == None  =========== ')
    return()


def get_decimal(item):
    try:
        for ext in item.extension:
            if ext.url == 'http://fhir.org/guides/argonaut-questionnaire/StructureDefinition/extension-score':
                    app.logger.info('===========ext = {}  score = {} =========== '.format(ext.url,ext.valueDecimal))
                    return(ext.valueDecimal)
            elif ext.url == 'http://hl7.org/fhir/StructureDefinition/valueset-ordinalValue':
                    app.logger.info('===========ext = {}  score = {} =========== '.format(ext.url,ext.valueDecimal))
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
    app.logger.info('=========== {} = {} = {} = {} =========== '.format(value_type,answer,score, std_dev))

    answer = type_conversion[value_type](answer) #convert answer
    qr_answer = QR.QuestionnaireResponseItemAnswer.parse_obj({value_type : answer})
    app.logger.info('=========== qr_answer = {}=========== '.format(qr_answer.json()))
    session['responses'] = '{r}<strong>Response:</strong> {a}<br />'.format(r=session['responses'], a=answer) # get gen narrative info
    set_narr('<strong>Response:</strong> {a}<br />',a=answer) # create narrative text elements as a cached list to join later
    calc_score(score, std_dev)
    return(qr_answer)


def get_coded_results(answer, score, std_dev):
    app.logger.info('=========== try to split =========== ')

    try:
        display, system, code = answer.split('|')
        qr_answer = QR.QuestionnaireResponseItemAnswer.parse_obj({'valueCoding':{'code':code, 'system':system, 'display':display} })
        app.logger.info('=========== qr_answer = {}=========== '.format(qr_answer.json()))
        session['responses'] = '{r}<strong>Response:</strong> {d} ( code = {c}, codesystem = {s})<br />'.format(r=session['responses'], d=display, c=code, s=system) # get gen narrative info
        set_narr('<strong>Response:</strong>  {d} ( code = {c}, codesystem = {s})<br />',d=display, c=code, s=system) # create narrative text elements as a cached list to join later
        calc_score(score, std_dev)

        return(qr_answer)

    except ValueError: # default to string
        app.logger.info('=========== {} is a string! =========== '.format(answer))
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


        app.logger.info('=========== answers = {}=========== type = {}'.format(answers, value_type))

        if answers in no_answer:
            app.logger.info('=========== not an answer! =========== ')
        elif value_type == 'valueCoding':  # get checkbox and radio button answers
            app.logger.info('=========== is a coding! =========== ')
            for answer in answers:
                app.logger.info('=========== get next answer! =========== ')
                # score = get_score(item, answer)
                # app.logger.info('=========== score = =========== '.format(score))
                qr_item.answer.append(get_coded_results(answer, get_score(item, answer)))
                # app.logger.info('=========== calc score =========== ')
                # calc_score(item,answer)

        else:
            app.logger.info('=========== not an  coded answer! =========== ')
            for answer in answers:
                # score = get_score(item, answer)
                # app.logger.info('=========== score = =========== '.format(score))
                qr_item.answer.append(get_uncoded_results(answer, value_type, get_score(item)))
                app.logger.info('=========== calc score =========== ')
                # calc_score(item)
    except KeyError: # not a question typei
        if item.type != 'group':
            session['responses'] = '{r}<br /><strong>{d}</strong><br />'.format(r=session['responses'], d=qr_item.text, ) # get gen narrative info
            set_narr('<br /> <strong>Question:</strong> (linkID={l}) {q}<br />',l=qr_item.linkId, q=qr_item.text) # get gen narrative info)


def get_qr_items(results, item_list, qr_item_list, position=None):  #render QR.item based on Q.item  loop through each item group and nested item using recursion and copy structure and display

    for item in item_list:
        qr_item = QR.QuestionnaireResponseItem.construct()
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

            app.logger.info('=========== answers = {}=========== type = {}'.format(answers, value_type))

            if answers in no_answer:
                app.logger.info('=========== not an answer! =========== ')
            elif value_type == 'valueCoding':  # get checkbox and radio button answers
                app.logger.info('=========== is a coding! =========== ')
                for answer in answers:
                    app.logger.info('=========== get next answer! =========== ')
                    # score = get_score(item, answer)
                    # app.logger.info('=========== score = =========== '.format(score))
                    qr_item.answer.append(get_coded_results(answer, get_score(item, answer), session['std_dev']))
                    app.logger.info('=========== calc score =========== ')
                    # calc_score(item,answer)

            else:
                app.logger.info('=========== not an  coded answer! =========== ')
                for answer in answers:
                    # score = get_score(item, answer)
                    # app.logger.info('=========== score = =========== '.format(score))
                    qr_item.answer.append(get_uncoded_results(answer, value_type, get_score(item), session['std_dev']))
                    app.logger.info('=========== calc score =========== ')
                    # calc_score(item)i

        except KeyError: # not a question type
            if item.type != 'group':
                session['responses'] = '{r}<br /><strong>{d}</strong><br />'.format(r=session['responses'], d=qr_item.text, ) # get gen narrative info
                set_narr('<br /><strong>{d}</strong><br />',d = qr_item.text) # get gen narrative info

        try:  # replace item in list
            qr_item_list[position]=qr_item
        except  (IndexError,TypeError):
            qr_item_list.append(qr_item)  # append item object to qr_item_list
            app.logger.info('***************item.linkId = {}\n ***************item.type = {}\n ***************qr_item.json() = {}\n ***************qr_item_list={}\n\n'.format(item.linkId, item.type, qr_item.json(), qr_item_list))

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
        if item.answerOptions.reference.startswith('#'):
            # get contained contained VS
            for ci in q.contained:
                app.logger.info('contained item = '.format(ci))

                if '#{}'.format(ci.id) == item.answerOptions.reference:
                    vs = ci  # get contained VS
        else:
            vs_url = '{}{}'.format(ref_server, item.answerOptions.reference)  # external VS
            vs = VS.ValueSet(get_res(vs_url))  # get VS from reference server
        item.answerOptions = None  # remove options from item
        item.answerOption = []
        for contain in vs.expansion.contains:
            app.logger.info('contain = {}'.format(contain.json()))
            valuecoding = getcoding(contain.code, contain.system, contain.display, contain.extension)
            option = Q.QuestionnaireItemOption({'valueCoding': valuecoding.json()})  # add extensions # TODO:
            item.answerOption.append(option)
        return(item.answerOption)


def get_options(q):  # get contained or external valuesets and populate option.valueCoding  assuming the codes are in the expansion only gos two layers deep
    for item in q.item:
        app.logger.info('item = {}'.format(item.json()))
        try:
            item.answerOption = pop_option(q, item)
        except AttributeError:
            pass
        try:
            for sub_item in item.item:
                try:
                    sub_item.answerOption = pop_option(q, sub_item)
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


def set_cache(cache_id,value):
    '''get Q from FHIR Server save as python model (published version) and working version'''
    cache.set(cache_id, value, timeout=5 * 60)  # add to cache
    app.logger.info('{} now in cache!'.format(cache_id))
    return()  # TODO add trys to catch exceptions


def update_csv(index,row,column,data):
    '''update csv cell with data at row column and save'''
    app.logger.info(f'''update csv cell with data at row = {row} and column = {column} and save''')
    df=pd.read_csv(my_csv_path, index_col=index)
    df.loc[[row],[column]] = data
    app.logger.info(df.loc[[row],[column]])
    df.to_csv(my_csv_path, encoding='utf-8', header=True)


def get_q(request):
    '''Save the form_url in the session object. Convert the questionnaire to FHIR object and save to local cache.'''
    # convert to using CSV instead of cache?
    form_url = request.form['options']
    session['form_url'] = form_url
    app.logger.info('form_url = {} '.format(form_url ))
    app.logger.info('cache.get(form_url) = {} '.format(cache.get(form_url)))
    if not cache.get(form_url):  # cache value is empty
        app.logger.info('cache value is empty')
        r = requests.get(form_url, headers=f.fhir_headers, params={})
        app.logger.info(f'status = {r.status_code}')

        if r.status_code != 200:
            return 'no_fetch'

        q = Q.Questionnaire.parse_obj(r.json())
        #save to cache
        set_cache(form_url,q)  # get questionnaire from server as json and display create a link to the main menu how to return to main menu
        # q = translate_res(q,request.form.get('translate', None)) # translate q to the language in translate code. not available in 3.4 for AWS deployment
        q = get_options(cache.get(form_url))  # if options from external or contained VS then need to fetch valuesets and populate option.coding with the values...
        set_cache('{}_wq'.format(form_url), q)  # get questionnaire from server as json and display create a link to the main menu how to return to main menu
        # save to csv use form_url to get row, may need unique id in future
        update_csv(index='q_url',row=form_url,column='q_js',data=q.json())

    # app.logger.info('=================\n q = {} \n============='.format(q.json()))
    # app.logger.info('title = {} and qs = {}'.format(q.title, q.item))
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
#       app.logger.info('Hola mi amigos : translate {} to {}'.format(t_source, t_target))
#       return(t_target)
#   except TypeError:
#       return(t_source)
#
#
#
#def translate_res(res, code):  # translate to language code
#   app.logger.info("translate to {} !!!".format(code))
#   if code: # translate
#       app.logger.info("translate to {} !!!".format(code))
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
#                       for sub_item_choice in sub_item.answerOption:
#                           sub_item_choice.valueString = translate_element(sub_item_choice.valueString)
#                   except TypeError:
#                       pass
#           except TypeError:
#                   pass

#          create an extension on the element o wait I can't :-( since it is a primitivo.
#    return(res)
# ==========================================================================================


@app.route('/')
def index():
    reset_variables()
    return render_template('index.html', q_list = session['q_list'])
    
@app.route('/q_view', methods=['GET', 'POST'])  # decorator to map to form view
def q_view():
    session['q_starttime'] = '{}Z'.format(datetime.utcnow().isoformat()) # start-time as FHIRdate
    error = None
    # q = None  # for local file to start
    app.logger.info('request.form.get("adaptive", None) = {} request.values = {}'.format(request.form.get('adaptive', None),request.values))
    for k,v in request.form.items():
        app.logger.info(f"request.form key:value = {k}:{v}")
    if request.method == 'POST':
        if get_q(request) == "no_fetch":
            flash('Unable to fetch this form. Please choose another one') #flash error
            return redirect(url_for('index'))
        if request.form.get('adaptive', None):
            if session['form_url'] == 'http://sqlonfhir-stu3.azurewebsites.net/fhir/Questionnaire/questionnaire-example-housing':
                flash('Unable to create and adaptive questionnaire with this form. Please try again!') #flash error
                return redirect(url_for('index'))
            return aq_view()
        else:
            working_q = '{}_wq'.format(session['form_url'])
            q = cache.get(working_q)
            app.logger.info(f'q = {q.resource_type}')
            app.logger.info(f'session["form_url"]={session["form_url"]}' )
            #render static q
            return render_template('q_view.html', q = q)
    reset_aqr_cache()
    working_q = '{}_wq'.format(session['form_url'])
    q = cache.get(working_q)
    return render_template('q_view.html', q = q)


@app.route('/qjson_view', methods=['GET', 'POST'])  # decorator to map json
def qjson_view():
    q = cache.get(session['form_url'])
    # app.logger.info(f"q = cache.get(session['form_url']) = {cache.get(session['form_url'])}")
    return render_template('qjson_view.html',  q=q.json(indent = 4))

# currently not available in fhir.resources
# @app.route('/qxml_view', methods=['GET', 'POST'])  # decorator to map xml
# def qxml_view():
#     q = cache.get(session['form_url'])
#     return render_template('qxml_view.html',  q= q.xml(pretty_print=True))

@app.route('/qr-view', methods=['GET', 'POST'])  # decorator to map to answers
def qr_view():
    working_q = '{}_wq'.format(session['form_url'])
    qr_working_q = cache.get(working_q)

    reset_q_cache()
    # results = request.form  # this is multiDict structure - can only retrieve the first element or use the get list method
    app.logger.info('results = {}'.format(request.form))
    # bp()  # ***************** this is a break******************

    # split out linkId and text to create answers create a QR resource use a template for the meta for now

    qr = QR.QuestionnaireResponse.parse_obj(f.qr_templ)
    qr.questionnaire = qr_working_q.url # update the questionnaire canonical
    qr.id = qr_working_q.url.rsplit('/')[-1].replace('questionnaire', 'questionnaireresponse')  # update the QR id
    dt = '{}Z'.format(datetime.utcnow().isoformat())  # == stop time
    # qr.extension = [get_responseperiod_x(session['q_starttime'],dt)]    # add extension for FHIRDates start and stoptime
    qr.authored = f'{datetime.utcnow().isoformat()}Z'  # update datetime
    # app.logger.info(json.dumps(qr.json(), indent=4, sort_keys=True))
    # qr.subject.reference = session["subject"] 
    # qr.author.reference = session["author"]
    # qr.source.reference = session["source"]  !!! no source
    qr.item = []
    get_qr_items(request.form, qr_working_q.item, qr.item)

    #app.logger.info(json.dumps(qr.json(), indent=4, sort_keys=True))

    # ---create narrative---
    qr.text.div = '''<div xmlns=\"http://www.w3.org/1999/xhtml\">
    <h3>Response Summary</h3>
    <strong>Questionnaire URL:</strong> {q}<br />
    <strong>Date Completed:</strong> {d}<br />
    <hr /> {r} <br /><br />
    </div>'''.format(q=qr.questionnaire, d=qr.authored, r=''.join(session['narr_list']))

    #scrub id for user POST and save as session qr
    qr.identifier.value = qr.id
    session['qr_id'] = qr.id  # this is for saving my examples
    session['profile'] = qr.meta.profile[0]  # this is for uploads if validate by profile
    # qr.id = None # TODO comment out for user posting to server
    set_cache(qr.identifier.value, qr ) # cache as object instead of string
    app.logger.info(f'line 641 cache.get(qr_id) = {cache.get(qr.id)}')
    app.logger.info(f'line 642 type(cache.get(qr_id)_ = {type(cache.get(qr.id))}')
    # save to csv use form_url to get row, may need unique id in future
    form_url = session["form_url"]
    app.logger.info(f'line 643 form_url = {session["form_url"]}')
    update_csv(index='q_url',row=form_url,column='qr_js',data=qr.json())

   

    app.logger.info(json.dumps(f'line 648 qr = {qr.json(indent=2)}'))
    # bp()  # ***************** this is a break******************
    return render_template('qr_view.html', qr=qr, adaptive=False )


# ================================ POST Task  ==========================

@app.route('/Task', methods=['POST'])
def create_task():
    app.logger.info(f'session = {session}') # session is empty
    if not request.json or not 'task' in request.json:
        abort(400)
    app.logger.info(f'request.json = {request.json}')
    task_url = request.json['task']
    session["task_url"] = task_url  # used for updates to the csv later on
  
    app.logger.info(f' = {request.json}')
    try:
        #  Fetch the Task
        r = requests.get(task_url, headers=f.json_headers)
        app.logger.info(f'r.status_code = {r.status_code}')
        t = T.Task.parse_obj(r.json())
    except Exception as e:
        app.logger.error(f'fetch the task error = {e}')
        abort(500)

    else:
        app.logger.info(t.id, t.input[0])
        # add new row to csv with session id equal row number, task url, questionnaire URL, questionnaire title
        df = pd.read_csv(my_csv_path)
        q_url = [i.valueCanonical for i in t.input if i.type.coding[0].code == "questionnaire"][0]
        q_title = [i.valueCanonical__ext.extension[0].valueString for i in t.input if i.type.coding[0].code == "questionnaire"][0]
        session_id = datetime.now().astimezone().isoformat() # timestamp
        session["session_id"] = session_id # alternative way to keep track consider uuids ???
        new_row = {'session_id': session_id, 'task_url': task_url, 'task_js': t.json(), 'q_url': q_url, 'q_title': q_title}
        app.logger.info(f'new row = {new_row}')
        df = df.append(new_row, ignore_index=True)
        app.logger.info(f'new row = {df.tail(1)}')
        df.to_csv(my_csv_path, encoding='utf-8', index=False, header=True)
        
    return jsonify(request.json), 201


# ================================ POST to Answer Bank ==========================

@app.route('/post_answers', methods=['GET', 'POST'])  # decorator to post to answer bank
def a_bank():
    qr_id=session['qr_id']
    app.logger.info(f'line 706 qr_id = {qr_id}, cache.get(qr_id) = {cache.get(qr_id)}')
    qr = cache.get(qr_id)
    # qr = session.get('current_aqr') # cache is object and session is dict
    #!!!! struggle with typing here!!! unable to strip id and meta
    app.logger.info(f'line 711 qr type = {type(qr)} qr = {qr}')
 
    # strip id and profile for POST
    qr.id = None
    qr.meta = None # just pop meta for now need todo keep meta if other meta elements present.
    # my_utils.write_file(qr_id, qr) # save to out file for publishing Comment out when done

    r = my_utils.update_to_server(ref_server,qr.json(),'QuestionnaireResponse') # No id to post for other users
    app.logger.info('status code = {}\n headers = {}'.format(r.status_code,r.headers))# update QR to server return id.
    if r.status_code < 300:
        # update Task.output using Patch 
        app.logger.info( f'r.json()["id"] ={r.json()["id"]}')
        q_ref = r.json()["id"]
        patch_r = my_utils.patch_to_server(ref_server,f.task_patch,'Task',t_id)
        app.logger.info('line 725 patch_r status code = {}\n headers = {}'.format(patch_r.status_code,patch_r.headers))# update QR to server return id.
        if pr.status_code < 300:
            #update CSV as completed
            update_csv(index='session_id',row=session("id"),column='status',data="completed")

    return render_template('a_bank.html',ref_server_name = ref_server_name,
     ref_server = ref_server,
      r=r,
      qr_id = qr_id,
      posted_qr=json.dumps(r.json(),indent = 3, sort_keys=True)
    )
  

# ===================================View AQR ===================================

@app.route('/aq_view' , methods=['GET', 'POST']) #decorator to view adaptive questionnaire
def aq_view(): # client view
    working_q = '{}_wq'.format(session['form_url'])
    q = cache.get(working_q)
    try:
        d=q.date.json()
    except AttributeError:
        d=None
    session['intro'] = aq.intro.format(t=q.title, q=q.url, d=d, c=q.copyright)
    # logging.info('intro={}'.format(intro))
    # global current_aqr  # current state of aqr as model ( this is not strictly a stateless implementation)
    # aqr = current_aqr #update local copy
    try:
        aqr = QR.QuestionnaireResponse.parse_obj(session['current_aqr'])
    except FHIRValidationError:  # if current state of aqr is empty (i.e., no status )i
        reset_q_cache() #reset the score and narrative
        name = "Initialize AQ"
        aqr = aq.init_aqr(q)
        #j = aq.get_new_question(aqr) #get new question to display
        session['current_aqr']=aqr.json() # update session
        session['step'] = session['step'] + 1
        return render_template('aq_view.html', aqr=json.dumps(aqr.json(), indent=4, sort_keys=True), j=None, narr =''.join(session['narr_list']))

    logging.info(json.dumps(aq.get_next_q(q,aqr,session['t_score']).json(), indent=3))  # ****DON'T REMOVE -- fetches the next q and updates the score
    if aqr.item == None:
        aqr.item = []
    record_score(aqr) # and std_dev
    app.logger.info('aqr as dict ={}'.format(aqr.json()))

    session['current_aqr']=aqr.json() # update session

    if aqr.status == 'completed':  # done!!!
        # add response period extension
        dt = '{}Z'.format(datetime.utcnow().isoformat())  # == stop time
        aqr.extension = [get_responseperiod_x(aqr.authored.json(),dt)]
        pop_to_front() # resort narrative
        session['step'] = session['step'] + 1
        # change this to join
        aqr.text.div = '{}<hr />{}</div>'.format(session['intro'],''.join(session['narr_list'])) # add q-as to narrative
        # aqr.text.div = '{i}{r}'.format(i=aqr.text.div,r=session['responses']) # add q-as to narrative
        #app.logger.info('aqr as dict ={}'.format(aqr.json()))

        #scrub id for user POST and save as session qr
        aqr.identifier.value = aqr.id
        session['profile'] = aqr.meta.profile[0]  # this is for uploads if validate by profile
        session['qr_id'] = aqr.id  # this is for saving my examples
        # aqr.id = None # TODO Comment out for user posting to server
        session['current_aqr']=aqr.json() # update session

        return render_template('qr_view.html', qr=aqr, qr_string=json.dumps(session['current_aqr'],indent =3, sort_keys=True), adaptive=True)
        # TODO use PRG pattern so doesn't update on refresh

    j = aq.get_new_question(aqr) #get new question to display
    pop_to_front() # resort narrative
    session['step'] = session['step'] + 1
    return render_template('aq_view.html', aqr=json.dumps(aqr.json(), indent=4, sort_keys=True), j=j, narr =''.join(session['narr_list']))

@app.route('/update_aqr',methods=['GET', 'POST'])  # decorator to update the aqr with the next answer
def update_aqr(): #server view
    aqr = QR.QuestionnaireResponse.parse_obj(session['current_aqr'])

    results = request.form  # get answer

    # add to aqr

    item_list = aq.get_item_list(aqr.contained[0], session['q_num']+2) # get cq item

    if aqr.item == None:
        aqr.item = []
    #record_score(aqr) # and std_dev

    get_qr_items(results,item_list,aqr.item)

    session['step'] = session['step'] + 1
    session['current_aqr']=aqr.json() # update session
    session['q_num'] = session['q_num'] + 1 # next question

    return render_template('aq_view.html', aqr=json.dumps(aqr.json(), indent=4, sort_keys=True), j=None, narr =''.join(session['narr_list']))

# return to aq view
    # return render_template('qr_view.html', qr=qr, qr_string=json.dumps(qr.json(), indent=4, sort_keys=True), t_score=session['t_score'] )

# run the app.i
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app
        # initialize the log handler
    logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)

    # set the log handler level
    logHandler.setLevel(logging.INFO)

    # set the app logger level
    app.logger.setLevel(logging.INFO)

    app.logger.addHandler(logHandler)

    app.logger.info('End of program')
    app.debug = True
    app.jinja_env.auto_reload = True
    app.run()
