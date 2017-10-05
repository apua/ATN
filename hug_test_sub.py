import hug

#sub = hug.route.API(__name__)

#@sub.get()
@hug.get()
def index():
    return 'sub-index'

def home(a, b):
    return f'{a} - {b}'


