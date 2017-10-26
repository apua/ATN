import hug
from hug import get, post, put, delete, http
from hug.output_format import html as html_format

from jinja2 import Environment, PackageLoader, select_autoescape

#from app.models import TestData, TestResult, Id
#from app.test_execution import execute

from app.utils import _v, _t


# TODO: Clean `render` arguments to avoid `locals` and `globals`.
env = Environment(
        loader=PackageLoader('app', 'templates'),
        autoescape=select_autoescape(['html', 'xml']),
        )

# /      -> landing page, list all test suites and reports
# /add   -> adding page
# /api/* -> provide CRUD and executio


@get('/', output=html_format)
def _():
    testsuites=((obj.id, obj.data) for obj in TestData.objects.all())
    return env.get_template('list.html').render(testsuites=testsuites)


@get('/{id:uuid}', output=html_format)
def _(id: Id):
    return env.get_template('detail.html').render(**locals(), **globals())


@get('/add', output=html_format)
def _():
    from textwrap import dedent
    example = dedent("""\
            ***test cases***
            1st Case
                log_to_console  suite 1
            """)
    return env.get_template('add.html').render(**locals(), **globals())


@post('/add')
def _(body: TestData.post_schema, request, response):
    td = body
    td.save()
    response.status = hug.HTTP_303
    response.location = f'/{td.id}/detail'


@post('/api')
def _(body: TestData.post_schema, request, response):
    td = body
    td.save()
    if request.user_agent and 'Mozilla' in request.user_agent:  # browser
        response.status = hug.HTTP_303
        response.location = f'/{td.id}/detail'
    else:  # o.w.
        response.status = hug.HTTP_201
        response.location = f'/{td.id}'


@get('/api/{id:uuid}')
def _(id: Id):
    return TestData.objects.get(id).to_json()


@put('/api/{id:uuid}')
def _(id: Id, body: TestData.post_schema):
    td = TestData.objects.get(id)
    # TODO: It is about Python CouchDB API, `dict(body)` will fail, thus
    #       cannot simply code `td.update(body)`.
    td.update(body.items())
    td.save()


@delete('/api/{id:uuid}')
def _(id: Id):
    TestData.objects.delete(id)


@post('/api/{id:uuid}/execute')
def _(id: Id, response):
    td = TestData.objects.get(id)
    #try:
    #    result = execute('invalid content')
    #except DataError as e:
    #    render = lambda e: {'message': e.message, 'details': e.details}
    #    result = render(e)
    result = "AAAAAA"
    tr = TestResult(result=result)
    tr.save()
    response.status = hug.HTTP_201
    response.location = f'/{id}/result/{tr.id}'


