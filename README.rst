======================
Automated Test Network
======================

-   ATN designs for integration of whole `test process`
    including "plan", "design", "exec", and "report".

-   ATN benefits to `share resources`, for example, `test objects` and `test data`.

-   ATN considers `Test as a Serivices` providing a platform for test planning,
    `test data` design, *remote test execution*, and reporting.

-   ATN is composed of `TaaS console`, `TaaS storage`, and a few enhanced `test harnesses`.

-   Enhanced `test harnesses` wrap `test automation framework` with job queue
    for *parallel test executions*, and provide *REST API* for collaboration with other system.

-   `Automated provisioning` is considered as part of `test data` in ATN.

-   System under test is considered a member of `system relation hierarchy` in ATN.

It is just a basic implementation for advanced feature implementation,
for example, automated test resource allocation, in the future.


Glossary
========

+--------------+------------------------+
| Abbreviation | Stands for             |
+==============+========================+
| SUT          | System Under Test      |
+--------------+------------------------+
| TD           | Test Data              |
+--------------+------------------------+
| TE           | Test Execution         |
+--------------+------------------------+
| TR           | Test Report            |
+--------------+------------------------+
| TH           | Test Harness           |
+--------------+------------------------+
| TaaS         | Test as a Service      |
+--------------+------------------------+
| ATN          | Automated Test Network |
+--------------+------------------------+

+-------------------+-------------------------------------------------------------+
| Term              | Description                                                 |
+===================+=============================================================+
| system under test | The component or system to be tested. It could be a server, |
|                   | switch, VM, container, and so on.                           |
+-------------------+-------------------------------------------------------------+
| test object       | i.e. system under test.                                     |
+-------------------+-------------------------------------------------------------+
| test data         | Compresses test cases, variables, test libraries,           |
|                   | test drivers, and auto provisioning scripts.                |
+-------------------+-------------------------------------------------------------+
| test report       | A document summarizing testing activities and results,      |
|                   | produced at regular intervals, to report progress of        |
|                   | testing activities against a baseline (such as the          |
|                   | original test plan) and to communicate risks and            |
|                   | alternatives requiring a decision to management.            |
+-------------------+-------------------------------------------------------------+
| test environment  | An environment containing hardware, instrumentation,        |
|                   | simulators, software tools, and other support elements      |
|                   | needed to conduct a test.                                   |
+-------------------+-------------------------------------------------------------+
| test harness      | A test environment comprised of stubs and drivers needed to |
|                   | execute a test.                                             |
+-------------------+-------------------------------------------------------------+
| test process      | The fundamental test process comprises test planning and    |
|                   | control, test analysis and design, test implementation and  |
|                   | execution, evaluating exit criteria and reporting, and test |
|                   | closure activities.                                         |
+-------------------+-------------------------------------------------------------+
| test as a service | An outsourcing model in which testing activities are        |
|                   | performed by a service provider rather than self.           |
+-------------------+-------------------------------------------------------------+
| TaaS console      | The web client of TaaS.                                     |
+-------------------+-------------------------------------------------------------+
| TaaS storage      | The test resource storage collecting test data and reports. |
+-------------------+-------------------------------------------------------------+

Roles and Responsibilities:

+---------------+------------------------------------------------------------+
| Role          | Resposibility                                              |
+===============+============================================================+
| tester        | A skilled professional who is involved in the testing of   |
|               | a component or system.                                     |
+---------------+------------------------------------------------------------+
| test manager  | The person responsible for project management of           |
|               | testing activities and resources, and evaluation of a SUT. |
|               | The individual who directs, controls, administers, plans   |
|               | and regulates the evaluation of a SUT.                     |
+---------------+------------------------------------------------------------+
| test director | A senior manager who manages test managers.                |
+---------------+------------------------------------------------------------+
| local tester  | A tester works at local test environment who also          |
|               | responses for SUTs maintenance.                            |
+---------------+------------------------------------------------------------+
| remote tester | A tester not works at local test environment.              |
+---------------+------------------------------------------------------------+

Reference: `ISTQB Glossary All Terms`_

.. _ISTQB Glossary All Terms:
    https://www.istqb.org/downloads/send/20-istqb-glossary/186-glossary-all-terms.html


User stories
============

Epic
----

As a `test director`,
I want an infrastructure, say automated test network (`ATN`), which integrate `test process` by
sharing `test data`, `test objects`, `test environments`, and collecting `test reports`,
so that accelerating test automation and reduce redundant test resources.

Stories
-------

As a `test manager`,

-   I want a service with user interface, to manage and share `test data`.
-   I want a service with user interface which stores `test reports`, to manage and analyze `test reports`.

As a `local tester`,

-   I need a user interface on my `test harness`, to fetch/import `test data` via `ATN` for test execution.
-   I need a user interface on my `test harness`, to execute automated test for test execution.
-   I need a user interface on the service where `test manager` work on, to upload `test report` for test reporting.
-   I want `test harness` supports parallel test executions, so that accelerating test executions.
-   I want `test harness` supports `SUTs` reservation to deny other `testers` change states of those `SUTs`,
    so that avoiding someone interrupt my test execution.
-   I want `test harness` determines a system is either under test (`SUT`) or a part of `test environment`
    and restrict their usage automatically, so that I won't break `test environments`.
-   I need a user interface on the service where `remote tester` work on, to provide/remove my `test harness` information,
    so that other `testers` can leverage the shared `SUTs` and `test environments`.

As a `remote tester`,

-   I need a service with user interface to fetch `test data`, leverage `SUTs` and `test environments` to execute test,
    and upload `test report` for `test process`.
-   I want the service (as above) supports `SUTs` reservation to deny other `testers` change states of those `SUTs`,
    so that avoiding someone interrupt my test execution.

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

-   remote tester website have all user accounts from AD

-   local/remote tester only work at local/remote, i.e. not require TD at both side,
    and local/remote tester will not login to remote/local

Acceptance Criteria
-------------------

A.  -   [v] user roles: tester, administrator

    -   [v] register SUTs where "reserved_by" is me, "maintained_by" is me

    -   [v] SUT: one cannot change "reserved_by" from me, but I can

    -   [v] SUT: one cannot change "maintained_by" from me, but I can

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

    -   [v] I can only execute my TD with SUTs I reserved

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

    -   [v] test harness: UUID, IP
    -   [v] user identification: UUID, email
    -   [v] SUT: UUID, identification (type, credential), maintained_by, reserved_by, under
    -   [v] TD (remote): ID, ...
    -   [v] TD (local): ID, ...
    -   [v] TE (local): UUID, RQ job ID, TD, origin TD, ...
    -   [v] TE (remote): UUID, origin TD, local_done (Bool)
    -   [v] TR

    -   [v] execute TD -> TD owner? -> SUT reserved? -> SUTs on the same TH?
        -> cache TD at local -> remote check TE finished manually
        -> local TE is finished -> local upload TE/TR to remote

    -   [v] register TH -> fix user identification -> add SUTs infomation by UUID
        -> upload TE/TR by UUID

    -   [v] remote user reserve SUTs -> sync to local
    -   [v] local user reserve SUTs -> sync to remote

D.  Analysis:

    -   OOBM is bound w/ SUT, and OOBM require "SUT management" to auto-discover and control;
        w/o OOBM, SUT cannot be managed and out of scope

    -   for integrity, SUT must be verified via SUT management while saving (add/edit)

    -   "SUT management" has owner. Its rule is the same as "maitained by"

    -   require "auto-provisioning" based on RF and leverage existing test data to
        "change" SUT state

    -   SUT information is stored at site database

    -   UUID is the iLO UUID/VM UUID/...; generating UUID if it does not provide (e.g. switch)

    -   still have other information to identify the same SUT for manually added

    -   (enhancement) use typing system in programming to verify SUT information

    -   (enhancement) support handling unknown type of SUT

    -   while register test harness, all SUTs are added to Remote;
        adding/editing SUTs will sync to Remote if test harness is registered;
        editing SUTs at Remote will sync to test harness

-   [v] Continuous monitoring test execution


Enhancement
===========

-   Handle local disconnect/re-connect to remote

-   As a remote tester, I want to validate TL and resource pool like ISO images
    before test execution, so that I can ask maintainer for test environment preparation

-   Test data dry-run to validate itself and test harness

-   Remote users can access local (test harness) to install TL (into system) or download file
    (related to disk space). It depends on discussion between tester, and is out of scope
    of the architecture

-   "SUT management" auto-discovery feature

-   SUT status monitoring


Implementation
==============

Arch::

    .
    ├── harness
    │   └── autotest
    └── taas
        └── autotest
        └── taas

Requirements: check out `requirements.txt`

Diagram
-------

A.  Local tester execute automated test::

        Test Data -> Test Data: create and edit TD
        Test Data -> Test Execution: execute TD
        Test Execution -> Test Execution: wait and monitor TE
        Test Execution -> Test Reporting: report

B.  Register and revoke local site ::

        TaaS Console -> TaaS Console: register with TH credential
        TaaS Console -> Test Harness: mark TH registered by TaaS
        Test Harness -> TaaS Console: fetch TH owned SUTs and add to TaaS

        TaaS Console <-> Test Harness: Sync to each other while reservation changed

        TaaS Console -> TaaS Console: revoke TH
        TaaS Console -> TaaS Console: remove SUTs owned by TH
        TaaS Console -> Test Harness: mark TH not registered by TaaS
        Test Harness -> Test Harness: release SUTs reserved by remote users

C.  Leverage shared SUTs and execute automated test::

        TaaS Console -> TaaS Console: create and edit TD
        TaaS Console -> TaaS Console: execute TD
        TaaS Console -> Test Harness: submit TE

        TaaS Console <-> Test Harness: wait and monitor TE

        Test Harness -> Test Harness: report
        Test Harness -> TaaS Console: upload report to TaaS


D.  Setup SUT:

    i.  SUT has OOBM
    #.  connecting OOBM onto test network
    #.  TH automatic discover OOBM
    #.  TH register the OOBM as SUT with default "maintained by" and "reserved by"
    #.  maintainer release SUT and then remote user reserve SUT
    #.  create automated provisioning script from test data
    #.  execute automated provisioning script and update SUTs information
