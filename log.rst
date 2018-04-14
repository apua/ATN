2018.04.13:

After review ISTQB Term. I induce the definitions below::

    spec = { {user story}, design, ... }
    user story = { reason, acceptance criteria, ... }
    acceptance criteria = { requirement | accepted by stakeholders }
    use case = scenario ∈ feature ⊂ acceptance criteria

In addition:

-   `Acceptance testing` enable `stakeholders` to determine `acceptance criteria`;
    `user acceptance testing` simulate `users` to satisfy `requirements`.

-   Without `microservices`, it might be difficult to split SRS documents.

-   In my SRS example, it doesn't contain implementation detail, instead,
    it focus on `functional requirements` and `quality requirements`.

-   Most of `requirements` in `user stories` are `functional requirements`;
    most of `quality requirements` are not in `user stories`.

-   `Requirement engineering`_ (also available for user stories) are not iterative in Waterfall,
    and have methods:

    -   `I* modeling language <https://en.wikipedia.org/wiki/I*>`_
    -   other `modeling languages <https://en.wikipedia.org/wiki/Modeling_language>`_ (?!)

    In Agile, refer to `rational unified process`_ for `requirement engineering`_ during iterations.

    .. _rational unified process: https://en.wikipedia.org/wiki/Unified_Process
    .. _requirement engineering: https://en.wikipedia.org/wiki/Requirements_engineering

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2018.04.05:

The 2nd POC is going to be closed.

In addition to review the current stage, there is also the next goal below.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2018.03.27:

Have to set time to closure. Re-define functional specs:

- at test harness, auto-discover systems, and show whether available to test or not

- create/edit test data, indicate SUTs, execute test, and report

- reflect SUT information during test execution

- at test harness, support multiple test executions at the same time

- at TaaS console, register/revoke test harness and synchronize SUTs information

- at TaaS console, be able to change reservation only

- monitor test execution

- unit test to garantee multi-task with Django model

- system test to garantee functionality

- validator for API, Form, Models, test suites

- refactor for later maintenance


Need to review/update README next.


2018.03.14:

Move some text to `misc.rst` and keep only user story, acceptance criteria,
and so on, which are necessary for development.

Merge `local` branch that have partial implement, and review criteria.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Development flow
================

-   Objects: Epic story -> Stories -> Criteria -> Specification
-   TDD and doctest
-   multiple branches with Git

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
