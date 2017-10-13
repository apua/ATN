if __name__=='__main__':
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import couchdb
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField

from app.utils import _v, _t


couch = couchdb.Server('http://apua:qwer1234@localhost:9453')
db = couch['poc'] if 'poc' in couch else couch.create('poc')


class DocumentManager:
    def __init__(self, db):
        self.db = db

    def __get__(self, instance, owner):
        self.owner = owner
        return self

    def delete(self, id):
        db.delete(self.get(id))

    def get(self, id):
        return self.owner.load(self.db, id)

    def all(self):
        """
        return documents, ref:

        - https://pythonhosted.org/CouchDB/client.html#database
        - https://docs.djangoproject.com/en/1.11/topics/db/queries/#retrieving-all-objects
        """
        # TODO: It is about Python CouchDB API, `db.values()` is not implemented.
        return [self.get(id) for id in self.db]


class TestData(Document):
    data = TextField()
    objects = DocumentManager(db)
    example = '***test cases***\n1st Case\n    log_to_console  suite 1\n'

    def save(self):
        _v('db')
        self.store(db)

    def delete(self):
        del db[self.id]

    @classmethod
    def post_schema(cls, packed):
        return cls(**packed)

    def keys(self):  # with `keys` and `__getitem__`, the class itself is dict-like
        return iter(self)

    def to_json(self):
        return {'id': self.id, **self}

    def update(self, d):
        _v('d')
        return self._data.update(d)

    # def run(self): "run job by another model


class Id(str):
    def __new__(cls, uuid: __import__('uuid').UUID):
        return super().__new__(cls, uuid.hex)
