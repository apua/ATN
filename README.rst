========================================================
Automated Test Network with SUT sharing
========================================================

2018.02.22 Recall:

The 1st POC targets on an improved test automation framwork;
here the 2nd POC has different target, which includes full
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

In the 2nd POC, below topics are ignored and discussed in 3rd POC:

- security
- REST API data structure verification
- detail ORM model, eg: `on_delete` behavior


User stories
============

Epic story: As xxx, I want a test automation network, which shares SUTs, but
guarantee not disturb automated test mission.

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


Acceptance Criteria of Story A
------------------------------

-   [ ] user roles: tester, administrator

-   [ ] I can register SUTs where "reserved_by" is me, "maintained_by" is me

-   [ ] no one can reserve the SUTs I reserved

-   [ ] only I can change my SUTs "reserved_by"

-   [ ] I can reserve a SUT from no one reserved

-   [ ] only I can change my SUTs "maintained_by"

-   [ ] I cannot change my SUTs "maintained_by" to null

-   [ ] I can list my SUTs only

-   [ ] I can create TD where

    -   author (me)

    -   last modified

    -   optional "refer_to" to indicate the test plan written by SME

    -   suites:

        -   TC
        -   variables (including ISO images)
        -   keywords
        -   TL
        -   TR (including variables, keywords, TL)

-   [ ] anyone can copy my TD that all data the same in addition to
    they are author

-   [ ] I can list my TD only

-   [ ] I can search TD

    - "refer_to"
    - suites name

-   [ ] I can only execute my TD with my SUTs

-   [ ] test execution will fetch ISO/TL/TR automatically

-   [ ] I can search TE by "start" and "tester" is me

-   [ ] TE are read-only

-   [ ] I can get TE console, status (running/finished), TD which executed with,
    the original TD source, TR

-   [ ] I can modify TD, even if it has been executed before

-   [ ] I can get TR by TE start, including console, report.html, log.html,
    output.xml, where html/xml is in iframe


Assumptions of Story A
----------------------

-   assume RQ worker is enough to run test execution immediately (in fact,
    developer can take # of RQ workers as many as # of SUTs)

-   there may be more than one local tester

-   test harness has public IP, or the gateway has been set port forwarding (
    i.e. remote can access local site)

-   test harness can take additional port for REST API

-   every SUTs has maintainer, but may no one reserve it

-   reservation cannot set "until" so far, and no one can reserve future
    released SUT, either


Enhancement
===========

As a huge workload tester, I want an overview of my SUTs and Test executions
so that I can .... ??


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


Development Guide
=================

At 2018.03.01, I have a lesson:

-   Set my signature correctly -- "Apua <Apua.A.Aa@gmail.com>".

-   Avoid `git rebase` as much as possible because it is not only
    conflict with upstream (e.g. Github) but also have too much power
    to make information complicated.

-   Avoid `git reset HEAD@{x}` (`reflog`) as much as possible because
    it add steps into `reflog` as many as `reset` and less possible to save
    incorrect last operations.

-   There is relationship between user story, Django project and app, and
    version control branch. Thinking hierarchy carefully is helpful for naming.

-   (Conti.) A version control branch maps to a main user story (i.e. feature).

-   (Conti.) A Django app maps to a main user story (i.e. feature).

-   Require commit log convention for classification; here I have:

    *   chore -- misc.
    *   doc -- document updating
    *   poc -- mess during POC

-   Development process may be changed, not afraid and repond to change.
