from source import celery


@celery.task
def something():
    import time

    time.sleep(5)
    print("foooooooooooooooooooo", flush=True)
