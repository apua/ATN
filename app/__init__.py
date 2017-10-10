import hug

from . import views

#hug.API(__name__).extend(views, '/testdata')
hug.API(__name__).extend(views)

#@extend_api('/testdata')
#def _():
#    from . import views as testdata
#    return [testdata]
