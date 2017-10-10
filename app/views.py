from hug import get, post, put, delete, http
import hug

from jinja2 import Environment, PackageLoader, select_autoescape

from .models import TestData, ID

env = Environment(
        loader=PackageLoader('app', 'templates'),
        autoescape=select_autoescape(['html', 'xml']),
        )


@get('/', output=hug.output_format.html)
def _():
    return env.get_template('list.html').render(**locals(), **globals())


@get('/{id:int}/detail', output=hug.output_format.html)
def _(id: ID):
    return env.get_template('detail.html').render(id=id, detail=get_testdata(id)['data'])


@get('/add', output=hug.output_format.html)
def _():
    return env.get_template('add.html').render(**locals(), **globals())


@post('/')
def _(request, response, body: TestData):
    new_id = TestData.add(body)
    if request.user_agent and 'Mozilla' in request.user_agent:  # browser
        response.status = hug.HTTP_303
        response.location = f'/{new_id}/detail'
    else:  # o.w.
        response.status = hug.HTTP_201
        response.location = f'/{new_id}'


@get('/{id:int}')
def get_testdata(id: ID):
    testdata = TestData.instances[id]
    return testdata.to_dict()


@put('/{id:int}')
def _(id: ID, body: TestData):
    TestData.instances[id] = body


@delete('/{id:int}')
def _(id: ID):
    del TestData.instances[id]


