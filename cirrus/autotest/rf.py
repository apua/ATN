"""
Methods calling RobotFramework
"""

from contextlib import contextmanager
from .apps import AutotestConfig as Config
from .rq import task


@contextmanager
def exec_via_pybot(*, workdir, suite, suts):
    """
    :workdir: the name of working directory
    :suite: the text content of a test suite file
    :suts: JSON/YAML data
    """
    def write_file(filename, content):
        with open(Config.workspace/workdir/filename, 'w') as f:
            f.write(content)

    write_file('suite.robot', suite)
    write_file('suts.yaml', yaml.dump(suts))

    cmd = 'pybot -V suts.yaml -V vars.yaml suite.robot'
    try:
        yield sp.Popen(cmd, cwd=Config.workspace/workdir, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
        #te.pid = proc.pid
        #te.save(update_fields=['pid'])

        #for line in proc.stdout:
        #    ConsoleLine.objects.create(test_execution=te, output=line.decode())
    finally:
        outs, errs = proc.communicate()
        assert outs == b''
        assert errs is None
        assert proc.returncode is not None
