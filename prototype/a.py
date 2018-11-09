def task(func):
    from redis import Redis
    from rq.decorators import job
    queue_name = 'default'
    connection = Redis()
    return job(queue_name, connection=connection)(func)


@task
def exec():
    print(123)
    print(123)
    print(123)
    print(123)
    print(123)
    print(123)
    print(123)
    print(123)
    print(123)
    print(123)
