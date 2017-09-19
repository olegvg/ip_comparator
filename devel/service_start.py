# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from service.app import app
from wsgiref import simple_server

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 5050, app)
    httpd.serve_forever()