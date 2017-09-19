# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import logging
from leecher import config
from leecher.db import db_init_with_sql
from celery import Celery

db_init_with_sql()

logger = logging.getLogger('leecher')

celery_instance = Celery('leecher')
celery_instance.config_from_object('leecher_celery_conf')

