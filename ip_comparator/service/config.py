# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import yaml
import logging


redis_config = {}

with open('comparator_config.yml') as config_file:
    config = yaml.load(config_file)

    _service_logger = logging.getLogger('service')

    try:
        service_log_level = config['service']['logger']['level']
        _service_logger.setLevel(service_log_level)
    except (KeyError, TypeError):
        _service_logger.error("'config:service.logger.level' not found or incorrect, beware and check your config!")

    service_log_handler = logging.StreamHandler()
    try:
        service_log_format = config['service']['logger']['format']
        service_formatter = logging.Formatter(service_log_format)
        service_log_handler.setFormatter(service_formatter)
    except (KeyError, TypeError):
        _service_logger.error("'config:service.logger.format' not found or incorrect, beware and check your config!")

    _service_logger.addHandler(service_log_handler)

    try:
        redis_config['host'] = config['service']['redis']['host']
        redis_config['port'] = config['service']['redis']['port']
        redis_config['db'] = int(config['service']['redis']['db'])
    except (KeyError, TypeError):
        _service_logger.error("'config:service.redis' not found or incorrect, beware and check your config!")