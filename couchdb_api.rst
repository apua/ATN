Ref: `CouchDB 2.1.0`__

__ http://docs.couchdb.org/en/2.1.0/api/


API and Support List
====================

- 10.2. Server

  - 10.2.1. /

    * [v] GET /

  - 10.2.2. /_active_tasks
  - 10.2.3. /_all_dbs

    * [v] GET /_all_dbs

  - 10.2.4. /_cluster_setup
  - 10.2.5. /_db_updates
  - 10.2.6. /_membership
  - 10.2.7. /_replicate
  - 10.2.8. /_scheduler/jobs
  - 10.2.9. /_scheduler/docs
  - 10.2.10. /_restart
  - 10.2.11. /_stats
  - 10.2.12. /_utils
  - 10.2.13. /_uuids

    * [v] GET /_uuids

  - 10.2.14. /favicon.ico

- 10.3. Databases

  - 10.3.1. /db

    * [v] HEAD /{db}
    * [v] GET /{db}
    * [v] PUT /{db}
    * [v] DELETE /{db}

  - 10.3.2. /db/_all_docs

    * [o] GET /{db}/_all_docs
    * [v] POST /{db}/_all_docs

  - 10.3.3. /db/_bulk_docs
  - 10.3.4. /db/_find
  - 10.3.5. /db/_index
  - 10.3.6. /db/_explain
  - 10.3.7. /db/_changes
  - 10.3.8. /db/_compact
  - 10.3.9. /db/_compact/design-doc
  - 10.3.10. /db/_ensure_full_commit
  - 10.3.11. /db/_view_cleanup
  - 10.3.12. /db/_security
  - 10.3.13. /db/_purge
  - 10.3.14. /db/_missing_revs
  - 10.3.15. /db/_revs_diff
  - 10.3.16. /db/_revs_limit

- 10.4. Documents

  - 10.4.1. /db/doc
  - 10.4.2. /db/doc/attachment

- 10.5. Design Documents

  - 10.5.1. /db/_design/design-doc
  - 10.5.2. /db/_design/design-doc/attachment
  - 10.5.3. /db/_design/design-doc/_info
  - 10.5.4. /db/_design/design-doc/_view/view-name
  - 10.5.5. /db/_design/design-doc/_show/show-name
  - 10.5.6. /db/_design/design-doc/_show/show-name/doc-id
  - 10.5.7. /db/_design/design-doc/_list/list-name/view-name
  - 10.5.8. /db/_design/design-doc/_list/list-name/other-ddoc/view-name
  - 10.5.9. /db/_design/design-doc/_update/update-name
  - 10.5.10. /db/_design/design-doc/_update/update-name/doc-id
  - 10.5.11. /db/_design/design-doc/_rewrite/path

- 10.6. Local (non-replicating) Documents

  - 10.6.1. /db/_local/id


Design
======

Consider :model:`TestData` and :model:`TestResult`.
On CouchDB, those models are mapped to views or indexes,
and each data are stored as documents.


docs:

.. code:: yaml
    :name: TestData

    _id: !!uuid
    _rev: !!num-uuid
    model: !!str testdata
    properties: !!map
        data: !!str |
            *** test case ***
            case
                log to console  LOL

.. code:: yaml
    :name: TestResult

    _id: !!uuid
    _rev: !!num-uuid
    model: !!str testresult
    properties: !!map
        testdata: {"id": !!uuid, "rev": !!num-uuid}
        result: !!str


Get all objects (ie docs):

>>> for td in TestData.objects.all():
...     print(td.id, td.data)


Get specified doc; for query parameters, refer to `Query Parameters`__:

__ http://docs.couchdb.org/en/2.1.0/api/document/common.html#get--db-docid

>>> td = TestData.objects.get(id)
>>> td.id ; td.data
>>> TestData.objects.get(id, **{'rev': '{num}-{uuid}'})  # with query parameters |**

Since models are document-oriented, it is :class:`MutableMapping`, of course:

>>> td = TestData.objects.get(id)
>>> td['id'] ; td.items() ; td.update({'data': ''}) ; td.update([('data', '')])
>>> dict(td) ; {**td}  #**


However, some operations are not allowed for convention with MVCC__:

__ http://www.wikiwand.com/en/Multiversion_concurrency_control

>>> # statements below raise exception
>>> td['id'] = new_id ; td['rev'] = new_rev ; del td['data']
>>> td.update({'id': new_id}) ; td.update({'non_existing_key': ''})


Property `id`, `rev`, and `objects` are preserved by default,
it cannot modify default currently.


.. `objects.get` MUST return just one item, raise exception otherwise;
.. `objects.all`, `objects.filter`, and else return a "query set".
.. Refer to Django__:
..
.. __ https://docs.djangoproject.com/en/1.11/topics/db/queries/#retrieving-a-single-object-with-get
..
.. >>> TestResult.objects.all()  # not query yet
.. >>> [*TestResult.objects.all()]  # send query
..
..
.. Deleting objects requires


Consider:
    delete, update, Mango query....they are not the same as Django,
    should they be designed to lazy or eager?


get uuid : http://docs.couchdb.org/en/2.1.0/api/server/common.html?highlight=_uuids#uuids

POST /{db} : http://docs.couchdb.org/en/2.1.0/api/database/common.html#post--db

PUT /{db}/{docid} : http://docs.couchdb.org/en/2.1.0/api/document/common.html#put--db-docid

DELETE /{db}/{docid} : http://docs.couchdb.org/en/2.1.0/api/document/common.html#delete--db-docid

Retrieving Deleted Documents :
http://docs.couchdb.org/en/2.1.0/api/document/common.html#retrieving-deleted-documents

COPY /{db}/{docid} -- copy document

delete multiple : http://docs.couchdb.org/en/2.1.0/api/database/bulk-api.html?highlight=_bulk_docs

    POST http://localhost:9453/poc/_bulk_docs

    {
        "docs": [
            {
                "_id": "542b86ab0c674b1667d05a0f0c01f14d",
                "_rev": "5-fba05dabf4955ecf1a7d5b9d1721d7d0",
                "_deleted": true
            },
            {
                "_id": "542b86ab0c674b1667d05a0f0c01a93b",
                "_rev": "7-68ad56e1a743a3d824dbc9593d8eda36",
                "_deleted": true
            },
            {
                "_id": "542b86ab0c674b1667d05a0f0c01dba3",
                "_rev": "2-241ed26b932a014d36832f39da6b6eb9",
                "_deleted": true
            },
            {
                "_id": "542b86ab0c674b1667d05a0f0c01e24e",
                "_rev": "2-6e8945ccbd605c7d2361d5347ef29f1b",
                "_deleted": true
            }
        ]
    }
