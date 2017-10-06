import hug

@hug.get('/c/b')
def b(): return 2

@hug.extend_api('/c')
def c():
    import hug_route_c
    return [hug_route_c]

@hug.get('/c/a')
def a(): return 1

