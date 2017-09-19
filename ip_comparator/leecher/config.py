# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import yaml
import logging


redis_config = {}
postgresql_config = {}
cleanup_backward_delay = '10 minutes'

with open('comparator_config.yml') as config_file:
    config = yaml.load(config_file)

    _leecher_logger = logging.getLogger('leecher')

    try:
        leecher_log_level = config['leecher']['logger']['level']
        _leecher_logger.setLevel(leecher_log_level)
    except (KeyError, TypeError):
        _leecher_logger.error("'config:leecher.logger.level' not found or incorrect, beware and check your config!")

    leecher_log_handler = logging.StreamHandler()
    try:
        leecher_log_format = config['leecher']['logger']['format']
        leecher_formatter = logging.Formatter(leecher_log_format)
        leecher_log_handler.setFormatter(leecher_formatter)
    except (KeyError, TypeError):
        _leecher_logger.error("'config:leecher.logger.format' not found or incorrect, beware and check your config!")

    _leecher_logger.addHandler(leecher_log_handler)

    try:
        redis_config['host'] = config['leecher']['redis']['host']
        redis_config['port'] = config['leecher']['redis']['port']
        redis_config['db'] = int(config['leecher']['redis']['db'])
    except (KeyError, TypeError):
        _leecher_logger.error("'config:leecher.redis' not found or incorrect, beware and check your config!")

    try:
        postgresql_config['dsn'] = config['leecher']['pgsql']['dsn']
    except (KeyError, TypeError):
        _leecher_logger.error("'config:leecher.pgsql' not found or incorrect, beware and check your config!")

    try:
        cleanup_backward_delay = config['leecher']['cleanup']['backward_delay']
    except (KeyError, TypeError):
        _leecher_logger.warn("'config:leecher.cleanup.backward_delay' not found. Default '{}' used."
                             .format(cleanup_backward_delay))