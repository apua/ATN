r"""
>>> from couchdb import Server
>>> server = Server() # connects to the local_server
>>> secure_remote_server = Server('https://username:password@example.com:5984/')

 |
 |  This class behaves like a dictionary of databases. For example, to get a
 |  list of database names on the server, you can simply iterate over the
 |  server object.
 |
 |  New databases can be created using the `create` method:
 |
 |  >>> db = server.create('python-tests')
 |  >>> db
 |  <Database 'python-tests'>
 |
 |  You can access existing databases using item access, specifying the database
 |  name as the key:
 |
 |  >>> db = server['python-tests']
 |  >>> db.name
 |  'python-tests'
 |
 |  Databases can be deleted using a ``del`` statement:
 |
 |  >>> del server['python-tests']
 |
 |  Methods defined here:
 """
from couchdb import Server
server = Server('http://apua:qwer1234@localhost:9453') # connects to the local_server
#server = Server('https://apua:qwer1234@localhost:6984') # connects to the local_server
for i in server: print(i)
db = server['apua_test']
print(f'db name: {db.name}')
for i in db.name: print(i)
