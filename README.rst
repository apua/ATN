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

-   [v] user roles: tester, administrator

-   [v] register SUTs where "reserved_by" is me, "maintained_by" is me

-   [ ] SUT: one cannot change "reserved_by" from me, but I can

-   [ ] SUT: one cannot change "maintained_by" from me, but I can

-   [v] SUT: always has maintainer, but may no one reserves it
    (i.e. "maintained_by" cannot be blank, but "reserved_by" can be)

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

-   [ ] I can only execute my TD with SUTs I reserved

-   [ ] test execution will fetch ISO/TL/TR automatically

-   [v] I can search TE by "start" and "tester" is me

-   [v] TE are read-only

-   [v] I can get TE console, the original TD source

-   [v] I can modify TD, even if it has been executed before

-   [v] I can get TR by TE start, including console, report.html, log.html,
    output.xml

Enhancement:

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


Acceptance Criteria of Story B
------------------------------

Criteria:

-   local user work as usal
-   remote user leverage shared SUT to execute test
-   local user can register local site
-   all TE/TR collected to remote
-   local and remote get synchronous SUT sharing status
-   remote can edit TD
-   role: tester, administrator

Spec:

-   [ ] test harness: UUID, IP
-   [ ] user identification: UUID, email
-   [ ] SUT: UUID, identification (type, credential), maintained_by, reserved_by, under
-   [ ] TD (remote): ID, ...
-   [ ] TD (local): ID, ...
-   [ ] TE (local): UUID, RQ job ID, TD, origin TD, ...
-   [ ] TE (remote): UUID, origin TD, local_done (Bool)
-   [ ] TR: UUID, ...

-   [ ] execute TD -> TD owner? -> SUT reserved? -> SUTs on the same TH?
    -> cache TD at local -> remote check TE finished manually
    -> local TE is finished -> local upload TE/TR to remote

-   [ ] register TH -> fix user identification -> add SUTs infomation by UUID
    -> upload TE/TR by UUID

-   [ ] remote user reserve SUTs -> sync to local
-   [ ] local user reserve SUTs -> sync to remote


Assumptions of Story B
----------------------

-   remote tester website have full user accounts.
-   local/remote tester only work at local/remote, i.e. not require TD at both side,
    and local/remote tester will not login to remote/local
-   remote can access local


Enhancement
===========

-   As a huge workload tester, I want an overview of my SUTs and Test executions
    so that I can .... ??
-   Handle local disconnect/re-connect to remote. Might use message queue
-   Continuous monitoring test execution


Installation and Setup
======================

There are two parts: `remote_test_website` and `local_tester_website`

`local_tester_website` depends: Django, RQ, Redis

`remote_test_website` depends: Django
