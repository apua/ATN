========================================================
Automated Test Network with SUT sharing
========================================================

2018.03.14:

Move some text to `misc.rst` and keep only user story, acceptance criteria,
and so on, which are necessary for development.

Merge `local` branch that have partial implement, and review criteria.


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

-   [v] I can create TD where

    -   author (me)

    -   last modified

    -   optional "refer_to" to indicate the test plan written by SME

    -   suites:

        -   TC
        -   variables (including ISO images)
        -   keywords
        -   TL
        -   TR (including variables, keywords, TL)

-   [v] anyone can copy from my TD

-   [ ] I can only execute my TD with my SUTs

-   [ ] test execution will fetch ISO/TL/TR automatically

-   [v] I can search TE by "start" and "tester" is me

-   [v] TE are read-only

-   [v] I can get TE console, the original TD source

-   [v] I can modify TD, even if it has been executed before

-   [v] I can get TR by TE start, including console, report.html, log.html,
    output.xml
    
Enhance:

-   [ ] I can list my SUTs only

-   [ ] I can list my TD only

-   [ ] I can search TD

    - "refer_to"
    - suites name

-   [ ] I can get TE status (running/finished), TD which executed with, TR

-   [ ] I can get TR where html/xml is in iframe


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

There are two parts: `remote_test_website` and `local_tester_website`

`local_tester_website` depends: Django, RQ, Redis

`remote_test_website` depends: Django
