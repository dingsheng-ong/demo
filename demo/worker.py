from celery import Celery
from demo import config
from demo.jobs import jobs

celery = Celery('demo')
celery.config_from_object(config, namespace='CELERY')

@celery.on_after_configure.connect
def _setup_periodic_tasks(sender, **kwargs):
    for job in jobs:
        name = job.name
        task = job.task
        args = job.args
        kwargs = job.kwargs
        signature = celery.task()(task).s(*args, **kwargs)
        schedule = job.schedule
        sender.add_periodic_task(schedule, signature, name=name)
