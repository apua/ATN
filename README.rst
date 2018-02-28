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


User stories
============

A.  As a local tester, a test harness with webUI allows me to do things below,
    so that I can run automated test:

    1.  manage test data, including ISO image for auto-provisioing
    #.  manage test libraries
    #.  indicate test data and then execute test
    #.  auto-fetch things like ISO image and test libraries required by
        started test execution
    #.  monitoring specified test execution status
        by the combination of timestamp and test data
        (with arguments like SUTs info)
    #.  store test reports

B.  As a remote tester, a website on public allows me to do things below,
    so that I can invoke shared SUTs to run automated test:

    1.  multiple test harnesses register on the website
    #.  reserve SUTs for later use
    #.  manage test data
    #.  give information below and execute test:

        -   test data
        -   required stuff including ISO image for auto-provisioing and
            test libraries
        -   SUTs info under the same harness

    #.  monitoring specified test execution status
        by the combination of test harness, timestamp, and test data
        (with arguments like SUTs info)
    #.  store test reports

.. note:: not "semi-automated" test

.. note:: setup/teardown test environment is part of test execution

.. note:: not consider one test execution with multiple test harnesses


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
