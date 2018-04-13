======================
Automated Test Network
======================

-   ATN designs for integration of whole `test process`_
    including "plan", "design", "exec", and "report".

-   ATN benefits to `share resources`_, for example, `test objects`_ and `test data`_.

-   ATN considers `Test as a Service`_ providing a platform for test planning,
    `test data`_ design, *remote* `test execution`_, and reporting.

-   ATN is composed of `TaaS console`_, `TaaS storage`_, and a few enhanced `test harnesses`_.

-   Enhanced `test harnesses`_ wrap `test automation framework`_ with job queue
    for *parallel* `test executions`_, and provide *REST API* for collaboration with other system.

-   `Automated provisioning`_ is considered as part of `test data`_ in ATN.

-   System under test is considered a member of `system relation hierarchy`_ in ATN.

.. _share resources:
.. _test automation framework:
.. _automated provisioning:
.. _system relation hierarchy:
.. _test executions: `test execution`_


.. contents:: :depth: 1


User stories
============

Epic
----

As a `test director`_,
I want an infrastructure, say automated test network (`ATN`_), which integrate `test process`_ by
sharing `test data`_, `test objects`_, `test environments`_, and collecting `test reports`_,
so that accelerating test automation and reduce redundant test resources.

Split
-----

As a `test manager`_,

-   I want a service with user interface, to manage and share `test data`_.
-   I want a service with user interface which stores `test reports`_, to manage and analyze `test reports`_.

As a `local tester`_,

-   I need a user interface on my `test harness`_, to fetch/import `test data`_ via `ATN`_ for test execution.
-   I need a user interface on my `test harness`_, to execute automated test for test execution.
-   I need a user interface on the service where `test manager`_ work on, to upload `test report`_ for test reporting.
-   I want `test harness`_ supports parallel test executions, so that accelerating test executions.
-   I want `test harness`_ supports `SUTs`_ reservation to deny other `testers`_ change states of those `SUTs`_,
    so that avoiding someone interrupt my test execution.
-   I want `test harness`_ determines a system is either under test (`SUT`_) or a part of `test environment`_
    and restrict their usage automatically, so that I won't break `test environments`_.
-   I need a solution for sharing `SUTs`_ and `test environments`_.

As a `remote tester`_,

-   I need a service with user interface to fetch `test data`_, leverage `SUTs`_ and `test environments`_ to execute test,
    and upload `test report`_ for `test process`_.
-   I want the service (as above) supports `SUTs`_ reservation to deny other `testers`_ change states of those `SUTs`_,
    so that avoiding someone interrupt my test execution.


Solution
========

Assumptions
-----------

-   `Test directors`_ and `test managers`_ work at the same network in the corporation, say "corp-net".
-   Every `local tester`_ works in a private network of a laboratory, say "lab-net".
-   `Remote testers`_ work in either corp-net or their own lab-net.
-   Every system, either under test or not, has owner (or say, maintainer).
-   There is AD server in corp-net contains all user account based on Email.
-   Every `test harness`_ is connected to a lab-net, but might not be connected to corp-net yet, according to its maintainers (i.e. `local testers`_).
-   While an automated test is submitted, it shall be executed immediately.
-   Every reservation has no dead line, in other word, there is no "until" field to declare when will the `SUTs`_ and `test environments`_ be released.

Perspective
-----------

-   Provide `TaaS storage`_ which stores `test data`_ and `test reports`_ in corp-net.
-   Provide `TaaS console`_ which provides user interface for `test process`_ cooperating with `TaaS storage`_ in corp-net.
-   Enhance `test harnesses`_ to provide user interface to fulfill requirements comes from `local testers`_.
-   `TaaS storage`_, `TaaS console`_, and enhanced `test harnesses`_ communicate with REST style API via HTTP(S); each of them is working software based on microservices architecture.

File structure::

    .
    ├── harness
    │   └── autotest
    └── taas
        └── autotest
        └── taas

API
---

(TODO: provide later)

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

Dependency
----------

See `requirements <requirements.txt>`_


Use cases
=========

(TODO: add user scenario in RF format)


Enhancement
===========

Logging:

-   As a `test manager`_, I want to log automated test steps to analyze, so that I can measure and predict automated test duration.
-   As a `test manager`_, I want to log reservation to analyze, so that I can measure and predict reservation duration and manage resource accurately.

Test execution:

-   As a `tester`_, I want a service caching large files of `test data`_, e.g. ISO images, such service has user interface, so that I can accelerate my test execution.

`SUTs`_ management:

-   As a `local tester`_, I want auto-discovery tools based on different OOBM of systems, such auto-discovery tools will add systems onto `test harness`_ automatically, so that I don't register systems onto `test harness`_ manually and reduce human errors.
-   As a `local tester`_, I want an integrated `SUTs`_ management dashboard (i.e. system management), so that I can monitor laboratory resources in one sight.

Network:

-   As a `local tester`_, sometimes it is impossible to connect `test harness`_ to corp-net (there is gateway at least), it requires a solution to make `test harness`_ become a part of ATN, so that sharing `SUTs`_ and `test environments`_.
-   As a `remote tester`_, it requires solution like disconnect/re-connect handler, so that it covers unstable or high-latency network connection between `test harness`_ and ATN.
-   As a `test manager`_, while working in geographically different network, e.g. Houston/Bangalore/Taipei, I want a "local" `TaaS console`_, so that I can operate `TaaS console`_ smoothly.

Test design:

-   As a `test manager`_, I want enhanced test automation framework which is typed, so that creating more reliable test cases of `test data`_.
-   As a `test manager`_, I want enhanced dry-run feature on `TaaS console`_, so that creating more reliable variables of `test data`_.


Appendix
========

Abbreviation
------------

+--------------+---------------------------+
| Abbreviation | Stands for                |
+==============+===========================+
| _`SUT`       | `System Under Test`_      |
+--------------+---------------------------+
| _`TD`        | `Test Data`_              |
+--------------+---------------------------+
| _`TE`        | `Test Execution`_         |
+--------------+---------------------------+
| _`TR`        | `Test Report`_            |
+--------------+---------------------------+
| _`TH`        | `Test Harness`_           |
+--------------+---------------------------+
| _`TaaS`      | `Test as a Service`_      |
+--------------+---------------------------+
| _`ATN`       | `Automated Test Network`_ |
+--------------+---------------------------+

.. _SUTs: SUT_


Terminology
-----------

+----------------------+----------------------------------------------------------------+
| Term                 | Description                                                    |
+======================+================================================================+
| _`system under test` | The component or system to be tested. It could be a server,    |
|                      | switch, VM, container, and so on.                              |
+----------------------+----------------------------------------------------------------+
| _`test object`       | i.e. `system under test`_.                                     |
+----------------------+----------------------------------------------------------------+
| _`test data`         | Compresses test cases, variables, test libraries,              |
|                      | test drivers, and auto provisioning scripts.                   |
+----------------------+----------------------------------------------------------------+
| _`test report`       | A document summarizing testing activities and results,         |
|                      | produced at regular intervals, to report progress of           |
|                      | testing activities against a baseline (such as the             |
|                      | original test plan) and to communicate risks and               |
|                      | alternatives requiring a decision to management.               |
+----------------------+----------------------------------------------------------------+
| _`test environment`  | An environment containing hardware, instrumentation,           |
|                      | simulators, software tools, and other support elements         |
|                      | needed to conduct a test.                                      |
+----------------------+----------------------------------------------------------------+
| _`test harness`      | A `test environment`_ comprised of stubs and drivers needed to |
|                      | execute a test.                                                |
+----------------------+----------------------------------------------------------------+
| _`test process`      | The fundamental `test process`_ comprises test planning and    |
|                      | control, test analysis and design, test implementation and     |
|                      | execution, evaluating exit criteria and reporting, and test    |
|                      | closure activities.                                            |
+----------------------+----------------------------------------------------------------+
| _`test execution`    | The process of running a test on the component or              |
|                      | `system under test`_, producing actual result(s)               |
+----------------------+----------------------------------------------------------------+
| _`test as a service` | An outsourcing model in which testing activities are           |
|                      | performed by a service provider rather than self.              |
+----------------------+----------------------------------------------------------------+
| _`TaaS console`      | The web client of TaaS.                                        |
+----------------------+----------------------------------------------------------------+
| _`TaaS storage`      | The storage collecting `test data`_ and `test reports`_.       |
+----------------------+----------------------------------------------------------------+

.. _test objects: `test object`_
.. _test reports: `test report`_
.. _test environments: `test environment`_
.. _test harnesses: `test harness`_

Roles and Responsibilities
--------------------------

+------------------+------------------------------------------------------------+
| Role             | Resposibility                                              |
+==================+============================================================+
| _`tester`        | A skilled professional who is involved in the testing of   |
|                  | a component or system.                                     |
+------------------+------------------------------------------------------------+
| _`test manager`  | The person responsible for project management of           |
|                  | testing activities and resources, and evaluation of a SUT. |
|                  | The individual who directs, controls, administers, plans   |
|                  | and regulates the evaluation of a SUT.                     |
+------------------+------------------------------------------------------------+
| _`test director` | A senior manager who manages test managers.                |
+------------------+------------------------------------------------------------+
| _`local tester`  | A `tester`_ works at local test environment who also       |
|                  | responses for SUTs maintenance.                            |
+------------------+------------------------------------------------------------+
| _`remote tester` | A `tester`_ not works at local test environment.           |
+------------------+------------------------------------------------------------+

.. _testers: tester_
.. _test directors: `test director`_
.. _test managers: `test manager`_
.. _local testers: `local tester`_
.. _remote testers: `remote tester`_

References
----------

-   `ISTQB Glossary All Terms`_

.. _ISTQB Glossary All Terms:
    https://www.istqb.org/downloads/send/20-istqb-glossary/186-glossary-all-terms.html
