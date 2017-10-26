_v = lambda name, i=__import__('inspect'): print(f'DEBUG value: {name} -> %s' %
        (lambda f=i.getouterframes(i.currentframe())[1].frame: f.f_locals[name] if name in f.f_locals else f.f_globals[name])()
        )
_t = lambda name, i=__import__('inspect'): print(f'DEBUG type: {name} -> %s' %
        (lambda f=i.getouterframes(i.currentframe())[1].frame: f.f_locals[name] if name in f.f_locals else f.f_globals[name])()
        )


from requests import head, get, post, put, delete

user, password, host, port = 'apua', 'qwer1234', 'localhost', 9453
db = 'poc'
url = f'http://{user}:{password}@{host}:{port}'




def validate_query(params, **definition):
    r"""
    >>> number = lambda n: isinstance(n, int) and int(n) > 0
    >>> validate_query({'count': 10}, count=number)
    >>> validate_query({'count': '10'}, count=number)
    Traceback (most recent call last):
     ...
    TypeError
    >>> validate_query({'count': -1}, count=number)
    Traceback (most recent call last):
     ...
    TypeError
    """
    for k, v in params.items():
        if not (k in definition and definition[k](v)):
            raise TypeError

def validate_schema(*a, **kw): ...

number = lambda i: isinstance(i, int) and i > 0
ok = lambda s: isinstance(s, str) and s == 'ok'

def get_uuids(**params):
    path = f'/_uuids'
    validate_query(params, count=number)
    return get(f'{url}{path}', params=params)

def get_():
    path = f'/'
    return get(f'{url}{path}')

def get_all_dbs():
    path = f'/_all_dbs'
    return get(f'{url}{path}')

def head_db(db):
    path = f'/{db}'
    return head(f'{url}{path}')

def get_db(db):
    path = f'/{db}'
    return get(f'{url}{path}')

def put_db(db, **params):
    # TODO: validate db name - http://docs.couchdb.org/en/2.1.0/api/database/common.html#put--db
    path = f'/{db}'
    # NOTE: batch mode - http://docs.couchdb.org/en/2.1.0/api/database/common.html#batch-mode-writes
    #       will not consider POST method
    validate_query(params, batch=ok)
    return put(f'{url}{path}')

def delete_db(db):
    path = f'/{db}'
    return delete(f'{url}{path}')

def post_db(json, db, params):
    path = f'/{db}'
    return post(f'{url}{path}', json=json, params=params, headers={'X-Couch-Full-Commit':'true'})


def get_db_all_docs(db, **params):
    path = f'/{db}/_all_docs'
    # TODO: partial support query parameters - http://docs.couchdb.org/en/2.1.0/api/database/bulk-api.html#get--db-_all_docs
    validate_query(params, limit=number)
    return get(f'{url}{path}', params=params)

def post_db_all_docs(json, db):
    # TODO: consider JSON schema
    validate_schema(json, {
        'type': object,
        'required': ['keys'],
        'properties': {
            'keys': {
                'type': 'array',
                'items': {'type': 'string'},
                }
            }
        })
    path = f'/{db}/_all_docs'
    return post(f'{url}{path}', json=json)

