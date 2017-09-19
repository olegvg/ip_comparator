# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import redis
from config import redis_config


redis_client = redis.StrictRedis(host=redis_config['host'], port=redis_config['port'], db=redis_config['db'])