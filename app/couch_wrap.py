r"""
suite document::

  {
    "_id": "542b86ab0c674b1667d05a0f0c066761",
    "_rev": "2-0a037e8f2b39947dfe75a589b4fa6b31",
    "type": "suite",
    "data": "***test cases***\nFirst Case\n\tLog to console  A_______A\n"
  }

report document::

  {
    "_id": "542b86ab0c674b1667d05a0f0c0676d1",
    "_rev": "1-5c3d5bcf57ba7b0547304a60f61d398f",
    "type": "report",
    "log": "<html></html>",  // log, report, and output
    "execution": {  // test execution information
        "source_id": "542b86ab0c674b1667d05a0f0c066761",
        "source_rev": "2-0a037e8f2b39947dfe75a589b4fa6b31"
    }
  }


create Mango query index to solve warning::

  $ curl -X POST -H 'content-type:application/json' http://apua:qwer1234@localhost:9453/poc/_index -d '{"index":{"fields":["type"]}}'
  {"result":"created","id":"_design/3298cb694b9b0e42b2a70030ece92eca87d3552d","name":"3298cb694b9b0e42b2a70030ece92eca87d3552d"}

and the result::

    {
      "_id": "_design/3298cb694b9b0e42b2a70030ece92eca87d3552d",
      "_rev": "1-b4944d56a5bffbcba1b478673e740c59",
      "language": "query",
      "views": {
        "3298cb694b9b0e42b2a70030ece92eca87d3552d": {
          "map": {
            "fields": {
              "type": "asc"
            }
          },
          "reduce": "_count",
          "options": {
            "def": {
              "fields": [
                "type"
              ]
            }
          }
        }
      }
    }
"""


from collections import namedtuple

import requests

from .settings import url, db


class Suite(namedtuple('BaseSuite', 'id,rev,data')):
    @classmethod
    def _fromdoc(cls, doc):
        assert doc['type'] == 'suite'
        return cls(doc['_id'], doc['_rev'], doc['data'])
    def _asdoc(self):
        if self.rev:
            return {'_id': self.id, '_rev': self.rev, 'type': 'suite', 'data': self.data}
        else:
            return {'_id': self.id, 'type': 'suite', 'data': self.data}

class Result(namedtuple('BaseResult', 'id,rev,log,execution')):
    @classmethod
    def _fromdoc(cls, doc):
        assert doc['type'] == 'result'
        return cls(doc['_id'], doc['_rev'], doc['log'], doc['execution'])
    def _asdoc(self):
        if self.rev:
            return {'_id': self.id, '_rev': self.rev, 'type': 'result', 'log': self.log, 'execution': self.execution}
        else:
            return {'_id': self.id, 'type': 'result', 'log': self.log, 'execution': self.execution}

def list_suites():
    uri = f'{url}/{db}/_find'
    json={"selector":{'type': 'suite'}}
    resp = requests.post(uri, json=json)
    return tuple(map(Suite._fromdoc, resp.json()['docs']))

def list_results(suite_id, suite_rev=None):
    uri = f'{url}/{db}/_find'

    if suite_rev is None:
        json={"selector":{'type': 'result', 'execution.source_id': suite_id}}
    else:
        json={"selector":{'type': 'result',
                          'execution.source_id': suite_id,
                          'execution.source_rev': suite_rev}}

    resp = requests.post(uri, json=json)
    return tuple(map(Result._fromdoc, resp.json()['docs']))

def get_suite(id):
    uri = f'{url}/{db}/_find'
    json={"selector":{'type': 'suite', '_id': id}}
    resp = requests.post(uri, json=json)
    return Suite._fromdoc(resp.json()['docs'].pop())

def get_result(id):
    uri = f'{url}/{db}/_find'
    json={"selector":{'type': 'result', '_id': id}}
    resp = requests.post(uri, json=json)
    return Result._fromdoc(resp.json()['docs'].pop())

def get_uuid():
    uri = f'{url}/_uuids'
    return requests.get(uri).json()['uuids'].pop()

def new_suite(body):
    assert 'data' in body
    new_id = get_uuid()
    return Suite(new_id, '', body['data'])

def new_result(log_html, suite_id, suite_rev):
    new_id = get_uuid()
    return Result(new_id, '', log_html, {'source_id': suite_id, 'source_rev': suite_rev})

def put2db(obj):
    resp = requests.put(f'{url}/{db}/{obj.id}', json=obj._asdoc())
    return resp.json()

def delete_suite(id, rev):
    return requests.delete(f'{url}/{db}/{id}?rev={rev}')
