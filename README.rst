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
-   I need a solution for sharing `SUTs` and `test environments`.

As a `remote tester`,

-   I need a service with user interface to fetch `test data`, leverage `SUTs` and `test environments` to execute test,
    and upload `test report` for `test process`.
-   I want the service (as above) supports `SUTs` reservation to deny other `testers` change states of those `SUTs`,
    so that avoiding someone interrupt my test execution.

Assumptions
-----------

-   `Test directors` and `test managers` work at the same network in the corporation, say "corp-net".
-   Every `local tester` works in a private network of a laboratory, say "lab-net".
-   `Remote testers` work in either corp-net or their own lab-net.
-   Every system, either under test or not, has owner (or say, maintainer).
-   There is AD server in corp-net contains all user account based on Email.
-   Every `test harness` is connected to a lab-net, but might not be connected to corp-net yet, according to its maintainers (i.e. `local testers`).
-   While an automated test is submitted, it shall be executed immediately.
-   Every reservation has no dead line, in other word, there is no "until" field to declare when will the `SUTs` and `test environments` be released.

Solution
--------

-   Provide `TaaS storage` which stores `test data` and `test reports` in corp-net.
-   Provide `TaaS console` which provides user interface for `test process` cooperating with `TaaS storage` in corp-net.
-   Enhance `test harnesses` to provide user interface to fulfill requirements comes from `local testers`.
-   `TaaS storage`, `TaaS console`, and enhanced `test harnesses` communicate with REST style API via HTTP(S); each of them is working software based on microservices architecture.

Enhancement
-----------

Logging:

-   As a `test manager`, I want to log automated test steps to analyze, so that I can measure and predict automated test duration.
-   As a `test manager`, I want to log reservation to analyze, so that I can measure and predict reservation duration and manage resource accurately.

Test execution:

-   As a `tester`, I want a service caching large files of `test data`, e.g. ISO images, such service has user interface, so that I can accelerate my test execution.

`SUTs` management:

-   As a `local tester`, I want auto-discovery tools based on different OOBM of systems, such auto-discovery tools will add systems onto `test harness` automatically, so that I don't register systems onto `test harness` manually and reduce human errors.
-   As a `local tester`, I want an integrated `SUTs` management dashboard (i.e. system management), so that I can monitor laboratory resources in one sight.

Network:

-   As a `local tester`, sometimes it is impossible to connect `test harness` to corp-net (there is gateway at least), it requires a solution to make `test harness` become a part of ATN, so that sharing `SUTs` and `test environments`.
-   As a `remote tester`, it requires solution like disconnect/re-connect handler, so that it covers unstable or high-latency network connection between `test harness` and ATN.
-   As a `test manager`, while working in geographically different network, e.g. Houston/Bangalore/Taipei, I want a "local" `TaaS console`, so that I can operate `TaaS console` smoothly.

Test design:

-   As a `test manager`, I want enhanced test automation framework which is typed, so that creating more reliable test cases of `test data`.
-   As a `test manager`, I want enhanced dry-run feature on `TaaS console`, so that creating more reliable variables of `test data`.


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
