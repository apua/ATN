========================================================
Geographically distributed semi-Automated Test framework
========================================================

:thesis: https://paper.dropbox.com/doc/Geographically-distributed-semi-automated-test-framework-Fcd2daEnFbyUMmCOqTywq


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
