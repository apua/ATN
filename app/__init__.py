#from app.models import TestData, TestResult, Id
#from app.test_execution import execute

#from app.utils import _v, _t


class Id(str):
    def __new__(cls, uuid: __import__('uuid').UUID):
        return super().__new__(cls, uuid.hex)


# CouchDB wrapper
# ===============

from .couch_wrap import *


# View and Routing
# ================

# /      -> landing page, list all test suites and reports
# /add   -> adding page
# /api/* -> provide CRUD and executio


import hug
from hug.output_format import html as html_format


@hug.get('/', output=html_format)
def _():
    return env.get_template('list.html').render(suites=list_suites())


@hug.get('/{suite_id:uuid}', output=html_format)
def _(suite_id: Id):
    return env.get_template('detail.html').render(suite=get_suite(suite_id),
                                                  results=list_results(suite_id))

@hug.get('/{suite_id:uuid}/result/{result_id:uuid}', output=html_format)
def _(suite_id: Id, result_id: Id):
    return get_result(result_id).log

@hug.get('/add', output=html_format)
def _():
    from textwrap import dedent
    return env.get_template('add.html').render(example=dedent('''\
            ***test cases***
            1st Case
                log_to_console  suite 1
            '''))


@hug.post('/api')
def _(body, request, response):
    if 'id' in body and 'rev' in body:
        suite = Suite(**body)
    else:
        suite = new_suite(body)
    put2db(suite)
    if request.user_agent and 'Mozilla' in request.user_agent:  # browser
        response.status = hug.HTTP_303
        response.location = f'/{suite.id}'
    else:
        response.status = hug.HTTP_201
        response.location = f'/api/{suite.id}'


@hug.get('/api/{suite_id:uuid}')
def _(suite_id: Id):
    return get_suite(suite_id)


@hug.post('/api/{suite_id:uuid}')
def _(suite_id: Id):
    submit.delay(suite_id)
    #suite = get_suite(suite_id)
    #print(type(suite))
    #submit.delay(suite)
    #submit.apply_async((suite,))
    #submit.apply_async(args=(suite,))
    #submit.s(suite).apply_async()


@hug.put('/api/{suite_id:uuid}')
def _(suite_id: Id, body):
    return put2db(Suite(**body))


@hug.delete('/api/{suite_id:uuid}')
def _(suite_id: Id, rev):
    return delete_suite(suite_id, rev).json()


# Template render engine
# ======================

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
        loader=PackageLoader('app', 'templates'),
        autoescape=select_autoescape(['html', 'xml']),
        )

env.globals['flower_host'] = '10.30.99.3:5555'
env.globals['flower_host'] = 'localhost:5555'


# Task manager
# ============

from celery import Celery

from .test_execution import execute, DataError

queue = Celery('A___________A', backend='rpc://', broker='pyamqp://')

@queue.task
def submit(suite_id):
    suite = get_suite(suite_id)
    try:
        log_html = execute(suite.data)
    except DataError as e:
        import traceback
        log_html = f'<pre>{ "".join(traceback.format_exc()) }</pre>'
    put2db(new_result(log_html, suite.id, suite.rev))
