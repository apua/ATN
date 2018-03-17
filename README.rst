========================================================
Automated Test Network with SUT sharing
========================================================

2018.03.14:

Move some text to `misc.rst` and keep only user story, acceptance criteria,
and so on, which are necessary for development.

Merge `local` branch that have partial implement, and review criteria.


Glossary
========

+------+-------------------------------------------------------------+
| Term | Description                                                 |
+======+=============================================================+
| SUT  | system under test, e.g. HPE DL380Gen10, VMware ESXi         |
+------+-------------------------------------------------------------+
| TD   | test data, including test cases, variables, test libraries, |
|      | test drivers, and auto provisioning scripts                 |
+------+-------------------------------------------------------------+
| TE   | test execution                                              |
+------+-------------------------------------------------------------+
| TR   | test result, including test report and log,                 |
|      | providing full information about the result of TE           |
+------+-------------------------------------------------------------+
| TAF  | test automation framework                                   |
+------+-------------------------------------------------------------+
| ATN  | automated test network, the network present in this demo    |
+------+-------------------------------------------------------------+

+------------------+------------------------------------------------------------+
| Role             | Desciption                                                 |
+==================+============================================================+
| local tester     | a tester who work at private test network                  |
+------------------+------------------------------------------------------------+
| remote tester    | a tester who work at public network                        |
+------------------+------------------------------------------------------------+
| SUT maintainer   | a tester who maintain a SUT, is who add the SUT in general |
+------------------+------------------------------------------------------------+
| local site admin | a tester who manage a local site, is one of local tester   |
+------------------+------------------------------------------------------------+

Reference: `ISTQB Glossary All Terms`_

.. _ISTQB Glossary All Terms:
    https://www.istqb.org/downloads/send/20-istqb-glossary/186-glossary-all-terms.html


User stories
============

Epic story
----------

Provide a network based on test automation architecture, i.e. ATN,
which chain and share SUT/test harness/test automation framework/test result,
so that reduce redundant test resource and collect test result automatically.

Stories
-------

A.  As a local tester, I want to manage TD/submit TE/generate TR at LAN,
    so that I can run automated test to get the job done as usual.

B.  As a local tester, I can register my local tester website, a test automation
    framework, onto remote tester website, with access control, so that
    I can share resource with other tester and not interrupt my scheduled job.

C.  As a remote tester, I want to leverage shared resource to execute automated
    test while managing TD and collecting TR at remote,
    so that get the job done.

Acceptance Criteria
-------------------

A.  -   [v] user roles: tester, administrator

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

B.  Criteria:

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

Assumptions
-----------

-   assume RQ worker is enough to run test execution immediately (in fact,
    developer can take # of RQ workers as many as # of SUTs)

-   there may be more than one local tester

-   test harness has public IP, or the gateway has been set port forwarding (
    i.e. remote can access local site)

-   test harness can take additional port for REST API

-   every SUTs has maintainer, but may no one reserve it

-   reservation cannot set "until" so far, and no one can reserve future
    released SUT, either

-   remote tester website have full user accounts.
-   local/remote tester only work at local/remote, i.e. not require TD at both side,
    and local/remote tester will not login to remote/local
-   remote can access local


Enhancement
===========

-   Automatically collecting TR; note that disconnected TAF cannot upload TR,
    and not every TE/TR valuable to be collected
-   As a huge workload tester, I want an overview of my SUTs and Test executions
    so that I can .... ??
-   Handle local disconnect/re-connect to remote. Might use message queue
-   Continuous monitoring test execution


Installation and Setup
======================

There are two parts: `remote_test_website` and `local_tester_website`

`local_tester_website` depends: Django, RQ, Redis

`remote_test_website` depends: Django
