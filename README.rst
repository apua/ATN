========================================================
Automated Test Network with SUT sharing
========================================================

2018.02.22 Recall:

The first POC targets on an improved test automation framwork;
here the second POC has different target, which includes full
test automation architecture and SUT sharing.

- the site provides:

  - SUT manager

    - OOBM
    - ownership, including reservation and auth

  - image (provisioning resource, which is part of TD);
    TC, TP and Tcond (defined as TD);
    TL required by TC (library)

  - communicate with TH via REST API

  - task monitoring (may rely on `flower`)

  - store test reports

- TH (a.k.a test harness, defined in ISTQB)

  - test automation framework (RobotFramework)
  - multi-task server (HUG x Celery x Flower)
  - prepare test / upload test report

-------

TODO:

- [✓] redefine and merge API
- [_] decouple app
- [_] validate `id` and `rev` for distributed system

Known Issue:

- [✓] sometimes `{id:uuid}` is not transformed to `uuid`
  eg: PUT method via browser

Other:

- [_] merge list, add, and detail page
- [_] dismissible notice


Enable test execution workers:

.. code:: sh

    $ celery -A app.tasks worker
    $ flower -A app.tasks

Enable web server (not recommended use `hug` command because
it starts slowly and cannot auto-reload properly):

.. code:: sh

    $ gunicorn app:__hug_wsgi__ --log-level=DEBUG

Interactive with submodule during development, for example, `couch_wrap`:

.. code:: sh

    $ python -i -c 'from app.couch_wrap import *'
