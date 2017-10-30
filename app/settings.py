# CouchDB

user, password, host, port = 'apua', 'qwer1234', 'localhost', 9453
#user, password, host, port = 'apua', 'qwer1234', '10.30.99.3', 5984
db = 'poc'
url = f'http://{user}:{password}@{host}:{port}'


# Jinja2

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
        loader=PackageLoader('app', 'templates'),
        autoescape=select_autoescape(['html', 'xml']),
        )

#env.globals['flower_host'] = '10.30.99.3:5555'
env.globals['flower_host'] = 'localhost:5555'

get_template = env.get_template
