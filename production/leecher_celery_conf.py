# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from celery.schedules import crontab

CELERY_TIMEZONE = 'Europe/Moscow'

CELERYD_CONCURRENCY = 4

BROKER_URL = 'redis://127.0.0.1:6379/7'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/7'
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_REDIS_MAX_CONNECTIONS = 40

# may be list or tuple
CELERY_IMPORTS = "leecher.tasks.periodic"

CELERYBEAT_SCHEDULE = {
    'Suck out data': {
        'task': 'leecher.tasks.periodic.suck_out_iptable',
        'schedule': crontab(minute='*/2')
    },
    'Lookup for dirty blocks': {
        'task': 'leecher.tasks.periodic.lookup_for_dirty_blocks',
        'schedule': crontab(minute='*/30')
    },
}

