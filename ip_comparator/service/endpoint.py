# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import logging
import falcon
from falcon.util import uri
import ujson
from app import app
from db import redis_client


logger = logging.getLogger('service')


class ServiceEndpoint(object):
    def on_get(self, req, resp):
        """
        GET handler of match service

        :param req:
            Get string like ?first_id=X&second_id=Y
            where first_id and second_id are vars filled with id-s to be checked. X and Y in this case are ints!
        :param resp:
            JSON + HTTP/resp code depends of algorithm branch, see the code
        :return:
        """
        query = uri.parse_query_string(req.query_string)
        # if [x for x in query if x not in ['first_id', 'second_id']]:
        #     raise
        try:
            query['first_id'] = int(query['first_id'])
            query['second_id'] = int(query['second_id'])
        except(KeyError, TypeError):
            logger.warn("'runtime:endpoint.ServiceEndpoint.on_get' parsing query parameters error")
            resp.status = falcon.HTTP_500
            resp.body = ujson.dumps({
                'status': 'error',
                'note': 'query error'
            })
            return

        sets_dict = {x: set(redis_client.smembers(query[x])) for x in ['first_id', 'second_id']}

        empty_ids = [x[0] for x in sets_dict.items() if x[1] == set([])]
        if len(empty_ids) > 0:
            resp.status = falcon.HTTP_404
            resp.body = ujson.dumps({
                'status': 'not_found',
                'ids': empty_ids,
                'note': "some id's are not found in db"
            })
        else:
            intersect_set = reduce(lambda l, k: l & k, sets_dict.values())
            if len(intersect_set) > 0:
                resp.status = falcon.HTTP_200
                resp.body = ujson.dumps({
                    'status': 'not_connected',
                    'id': [query['first_id'], query['second_id']]
                })
            else:
                resp.status = falcon.HTTP_200
                resp.body = ujson.dumps({
                    'status': 'connected',
                    'id': [query['first_id'], query['second_id']]
                })


match = ServiceEndpoint()
app.add_route('/match', match)
