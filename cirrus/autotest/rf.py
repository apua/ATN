"""
Methods calling RobotFramework.
"""
import contextlib
import pathlib
import os
import subprocess as sp

import yaml
from django.conf import settings

from .rq import task


@contextlib.contextmanager
def exec_via_pybot(*, dirname:str, suite:str, suts:dict) -> 'context of subprocess':
    """
    :dirname: the name of working directory
    :suite: the text content of a test suite file
    :suts: parsed JSON/YAML data
    """
    def write_file(filepath, content):
        with filepath.open('w') as f:
            f.write(content)

    workdir = pathlib.Path(settings.AUTOTEST_WORKSPACE)/dirname
    os.makedirs(workdir, exist_ok=True)
    write_file(workdir/'suite.robot', suite)
    write_file(workdir/'suts.yaml', yaml.dump(suts))

    cmd = 'pybot -V suts.yaml suite.robot'
    proc = sp.Popen(cmd, cwd=workdir, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    try:
        yield proc
    finally:
        outs, errs = proc.communicate()


@task
def exec_test():
    import textwrap
    suite = textwrap.dedent("""\
            *** test cases ***
            T
                log to console  &{ilo}[ip]
            """)
    suts = {'ilo': {'ip':'10.30.3.1','username':'root','password':'Compaq123'}}

    with exec_via_pybot(dirname='mvp', suite=suite, suts=suts) as proc:
        print('PID:', proc.pid)
        print(*('=> ' + line.decode() for line in proc.stdout), sep='')

    return proc.returncode
