# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import re
import logging
import psycopg2
from leecher.db import conn
from leecher import celery_instance
from ..config import cleanup_backward_delay

logger = logging.getLogger('leecher')


@celery_instance.task
def suck_out_iptable():
    """
    Main worker which gets data from PostgreSQL and sends it it to Redis storage

    :return: -
    """
    with conn.pgsql.cursor() as cur:
        # interval_id bigint, user_id integer, ip_address inet, t_date timestamp with time zone
        cur.execute('SELECT interval_id, user_id, ip_address, t_date from seek_window();')

        # this commit() makes sure that worker doesn't hold iptable more time that needed
        conn.pgsql.commit()

        row = cur.fetchone()
        if row is None:
            return

        block_id = row[0]
        while True:
            user_id = row[1]
            ip = row[2]
            ip = re.search(r'(\d+?\.\d+?\.\d+?)\.\d+', ip).group(1)
            conn.redis.sadd(user_id, ip)
            row = cur.fetchone()
            if row is None:
                break

    with conn.pgsql.cursor() as cur:
        cur.execute("UPDATE date_marker SET state='clean' WHERE id=%s", (block_id,))
        conn.pgsql.commit()


@celery_instance.task
def lookup_for_dirty_blocks():

    """
    There is cleanup worker. Its SQL query looks a bit complicated but it works seldom so it's not a problem

    :return: -
    """
    with conn.pgsql.cursor() as cur:
        cur.execute(
            "select y.id as interval_id, z.user_id, z.ip_address, z.t_date from iptable as z, "
            "(select id, start_marker, end_marker "
            "from (select state, id, lag(end_marker, 1, to_timestamp(0)) "
            "over (order by end_marker asc) as start_marker, end_marker "
            "from date_marker  where end_marker < (now() - interval %s)) as x "
            "where state = 'dirty') as y where y.start_marker < t_date and t_date <= y.end_marker",
            (cleanup_backward_delay,))

        try:
            for row in cur:
                block_id = row[0]
                user_id = row[1]
                ip = row[2]
                ip = re.search(r'(\d+?\.\d+?\.\d+?)\.\d+', ip).group(1)
                conn.redis.sadd(user_id, ip)
                cur.execute("UPDATE date_marker SET state='clean' WHERE id=%s", (block_id,))

                logger.warn("Cleanup record: {}, {}, {:%d.%m.%Y %H:%M:%S %z}".format(*row[1:4]))
        except psycopg2.ProgrammingError:
            pass

        conn.pgsql.commit()
