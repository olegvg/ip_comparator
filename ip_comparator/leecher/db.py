# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import os
from leecher.config import redis_config, postgresql_config
from celery.signals import worker_process_init, worker_process_shutdown
import redis
import psycopg2


class Conn(object):
    __slots__ = ('redis', 'pgsql')
conn = Conn()

@worker_process_init.connect
def db_conn_init(**kwargs):
    conn.redis = redis.StrictRedis(host=redis_config['host'], port=redis_config['port'], db=redis_config['db'])
    conn.pgsql = psycopg2.connect(postgresql_config['dsn'])


@worker_process_shutdown.connect
def db_release(**kwargs):
    conn.pgsql.close()


def db_init_with_sql():
    pgsql = psycopg2.connect(postgresql_config['dsn'])

    with pgsql.cursor() as cur:
        cur.execute("SELECT relname from pg_class where relkind = 'r' and relname = 'iptable';")
        if cur.fetchone() is None:
            sql_file = os.path.join(os.path.dirname(__file__), 'init_db.sql')
            cur.execute(open(sql_file, 'r').read())
            pgsql.commit()

    pgsql.close()
