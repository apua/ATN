#from bottle import route as hug
from bottle import Bottle ; hug = Bottle()

@hug.route(r'/c/a')
def a(): return '1'

@hug.route(r'/c/b')
def b(): return '2'

hug.mount('/c', __import__('c').app)

hug.run(host='10.30.99.3', port=8000, debug=True)
