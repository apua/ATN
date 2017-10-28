#from app.models import TestData, TestResult, Id
#from app.test_execution import execute

#from app.utils import _v, _t


class Id(str):
    def __new__(cls, uuid: __import__('uuid').UUID):
        print("DEBUG:", type(uuid), uuid)
        if isinstance(uuid, str):
            return super().__new__(cls, uuid)
        else:
            return super().__new__(cls, uuid.hex)


# CouchDB wrapper
# ===============

from .couch_wrap import *


# View and Routing
# ================

"""
+---------------------------------+--------------+--------------------------------------+
|                                 | Payload      | usage                                |
+=================================+==============+======================================+
| GET    /                        |              | Get a page listing all suites        |
| GET    /add                     |              | Get a page to add suite              |
| POST   /suite                   | Suite object | Create a new suite                   |
| GET    /suite/{id}              |              | Get the suite detail or detail page  |
| PUT    /suite/{id}              | Suite object | Update the suite and return rev 204  |
| DELETE /suite/{id}?rev={rev_id} |              | Delete the suite and return 200      |
| POST   /suite/{id}?rev={rev_id} |              | Submit a test and return 202         |
| GET    /log/{id}                |              | Get log page of the result           |
+---------------------------------+--------------+--------------------------------------+
"""


import hug
from hug.output_format import html


@hug.get('/', output=html)
def _():
    return env.get_template('list.html').render(suites=list_suites())

@hug.get('/add', output=html)
def _():
    from textwrap import dedent
    return env.get_template('add.html').render(example=dedent('''\
            ***test cases***
            1st Case
                log_to_console  suite 1
            '''))

@hug.post('/suite')
def _(body, request, response):
    if 'id' in body and 'rev' in body:
        suite = Suite(**body)
    else:
        suite = new_suite(body)
    put2db(suite)

    if request.user_agent and 'Mozilla' in request.user_agent:  # browser
        response.status = hug.HTTP_303
    else:
        response.status = hug.HTTP_201
    response.location = f'/suite/{suite.id}'

@hug.get('/suite/{id:uuid}')
def _(id: Id, request, response):
    http = hug.API(__name__).http.routes['']['/suite/{id:uuid}']['GET'][None]
    if request.user_agent and 'Mozilla' in request.user_agent:  # browser
        http.outputs = hug.output_format.html
        response.set_header('content-type', 'text/html')  # a workaround ?
        return env.get_template('detail.html').render(suite=get_suite(id),
                                                      results=list_results(id))
    else:
        http.outputs = hug.output_format.json
        response.set_header('content-type', 'application/json')
        return {'results': list_results(id), **get_suite(id)._asdict()}

@hug.put('/suite/{id:uuid}')
def _(id: Id, body):
    return put2db(Suite(**body))

@hug.delete('/suite/{id:uuid}')
def _(id: Id, rev):
    return delete_suite(id, rev).json()

@hug.post('/suite/{id:uuid}')
def _(id: Id, rev=None):
    submit.delay(id)

@hug.get('/log/{id:uuid}', output=html)
def _(id: Id):
    return get_result(id).log


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
