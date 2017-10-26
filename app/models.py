import couchdb
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField


couch = couchdb.Server('http://apua:qwer1234@localhost:9453')


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


class ImprovedDocument(Document):
    def save(self):
        self.store(self._db)

    def delete(self):
        del self._db[self.id]

    @classmethod
    def post_schema(cls, packed):
        return cls(**packed)

    def keys(self):  # with `keys` and `__getitem__`, the class itself is dict-like
        return iter(self)

    def to_json(self):
        return {'id': self.id, **self}

    def update(self, d):
        return self._data.update(d)


class TestData(ImprovedDocument):
    _dbname = 'testdata'
    _db = couch[_dbname] if _dbname in couch else couch.create(_dbname)
    objects = DocumentManager(_db)
    data = TextField()


class TestResult(ImprovedDocument):
    _dbname = 'testresult'
    _db = couch[_dbname] if _dbname in couch else couch.create(_dbname)
    objects = DocumentManager(_db)
    result = TextField()


class Id(str):
    def __new__(cls, uuid: __import__('uuid').UUID):
        return super().__new__(cls, uuid.hex)



