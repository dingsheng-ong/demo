from celery.schedules import crontab
from collections import namedtuple
from demo.jobs.hello import hello

_t = namedtuple('job', ('name', 'task', 'schedule', 'args', 'kwargs'),
                defaults=(None, None, None, (), {}))

jobs = (_t(name='hello', task=hello, schedule=1.0), )
