"""
+---------------------------------+--------------+--------------------------------------+
|                                 | Payload      | usage                                |
+=================================+==============+======================================+
| GET    /                        |              | Get a page listing all suites        |
| GET    /add                     |              | Get a page to add suite              |
| POST   /suite                   | Suite object | Create a new suite                   |
| GET    /suite/{id}              |              | Get the suite detail or detail page  |
| PUT    /suite/{id}?rev={rev_id} | Suite object | Update the suite and return rev      |
| DELETE /suite/{id}?rev={rev_id} |              | Delete the suite and return 200      |
| POST   /suite/{id}?rev={rev_id} |              | Submit a test and return 202         |
| GET    /log/{id}                |              | Get log page of the result           |
+---------------------------------+--------------+--------------------------------------+
"""


import hug

from .couch_wrap import (
        list_suites,
        list_results,
        get_suite,
        get_result,
        new_suite,
        put2db,
        delete_suite,
        )
from .tasks import submit
from .settings import get_template


def uuid_str(s):
    return hug.types.uuid(s).hex


@hug.get('/', output=hug.output_format.html)
def _():
    return get_template('list.html').render(suites=list_suites())

@hug.get('/add', output=hug.output_format.html)
def _():
    from textwrap import dedent
    return get_template('add.html').render(example=dedent('''\
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

@hug.get('/suite/{id}')
def _(id: uuid_str , request, response):
    http = hug.API(__name__).http.routes['']['/suite/{id}']['GET'][None]
    if request.user_agent and 'Mozilla' in request.user_agent:  # browser
        http.outputs = hug.output_format.html
        response.set_header('content-type', 'text/html')  # a workaround ?
        return get_template('detail.html').render(suite=get_suite(id),
                                                      results=list_results(id))
    else:
        http.outputs = hug.output_format.json
        response.set_header('content-type', 'application/json')
        return {'results': [r.id for r in list_results(id)], **get_suite(id)._asdict()}

@hug.put('/suite/{id}')
def _(id: uuid_str, rev, body):
    return put2db(Suite(id, rev, **body))

@hug.delete('/suite/{id}')
def _(id: uuid_str, rev):
    return delete_suite(id, rev).json()

@hug.post('/suite/{id}')
def _(id: uuid_str, rev=None):
    submit.delay(id)

@hug.get('/log/{id}', output=hug.output_format.html)
def _(id: uuid_str):
    return get_result(id).log
