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
