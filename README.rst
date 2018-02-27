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


Installation and Setup
======================

There are two parts: `website`_ and `harness`_

Website
-------

(ry

Harness
-------

Dependency:

- Django
- Celery
- RabbitMQ
- Flower (optional)
- gunicorn (unused so far)


Setup and start development web server:

.. code:: sh

    $ cd harness
    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    $ ./manage.py runserver


Install RabbitMQ:

.. code:: sh

    $ pkg install rabbitmq
    $ echo 'rabbitmq_enable="YES"' >> /etc/rc.conf
    $ service rabbitmq start


Enable test execution workers:

.. code:: sh

    $ cd harness
    $ celery worker -A harness -c 2


Monitoring (optional):

1. Celery events

   .. code:: sh

       $ cd harness
       $ celery events -A harness

2. Flower

   .. code:: sh

       $ cd harness
       $ celery flower -A harness
