import hug
from hug import get, post, put, delete, http
from hug.output_format import html as html_format

from jinja2 import Environment, PackageLoader, select_autoescape

from app.models import TestData, Id
from app.utils import _v, _t

# TODO: Clean `render` arguments to avoid `locals` and `globals`.
env = Environment(
        loader=PackageLoader('app', 'templates'),
        autoescape=select_autoescape(['html', 'xml']),
        )


@get('/', output=html_format)
def _():
    return env.get_template('list.html').render(**locals(), **globals())


@get('/{id:uuid}/detail', output=html_format)
def _(id: Id):
    return env.get_template('detail.html').render(id=id, detail=get_testdata(id)['data'])


@get('/add', output=html_format)
def _():
    return env.get_template('add.html').render(**locals(), **globals())


@post('/')
def _(body: TestData.post_schema, request, response):
    td = body
    td.save()
    if request.user_agent and 'Mozilla' in request.user_agent:  # browser
        response.status = hug.HTTP_303
        response.location = f'/{td.id}/detail'
    else:  # o.w.
        response.status = hug.HTTP_201
        response.location = f'/{td.id}'


@get('/{id:uuid}')
def get_testdata(id: Id):
    # TODO: Error handler with HTTP status code (eg: 404)
    return TestData.objects.get(id).to_json()


@put('/{id:uuid}')
def _(id: Id, body: TestData.post_schema):
    # TODO: Error handler with HTTP status code (eg: 404)
    td = TestData.objects.get(id)
    # TODO: It is about Python CouchDB API, `dict(body)` will fail, thus
    #       cannot simply code `td.update(body)`.
    td.update(body.items())
    td.save()


@delete('/{id:uuid}')
def _(id: Id):
    # TODO: Error handler with HTTP status code (eg: 404)
    TestData.objects.delete(id)
