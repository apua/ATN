QUEUE_NAME = 'poc'


def task(func):
    from redis import Redis
    from rq.decorators import job

    connection = Redis()
    return job(QUEUE_NAME, connection=connection)(func)


@task
def run_pybot(workdir, suite, suts):
    def write_file(filename, content):
        from pathlib import Path

        with open(Path(workdir)/filename, 'w') as f:
            # assume `isinstance(suite, str)`
            f.write(content)

    write_file('suite.robot', suite)
    write_file('suts.yaml', suts)

    cmd = 'pybot -V suts.yaml suite.robot'
    proc = sp.Popen(cmd, cwd=workdir, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    prin('pid:', proc.pid)

    for line in proc.stdout:
        print(line)
        #ConsoleLine.objects.create(test_execution=te, output=line.decode())

    outs, errs = proc.communicate()
    assert outs == b''
    assert errs is None
    assert proc.returncode is not None

    return proc.returncode  # return code is defined by `pybot`
