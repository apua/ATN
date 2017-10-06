from bottle import Bottle
app=Bottle()

@app.route('/index')
def index():
    return 'A___A'
