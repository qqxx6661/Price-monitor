#!/usr/bin/env python
# coding:utf-8
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import urlparse, parse_qs
from DB import DatabaseObject
from config import DB_CONFIG, API_CONFIG
from logger import logger
import datetime
import json


class ProxyServer:
    def __init__(self, port):
        self.port = int(port)
        self.run()

    class ProxyPoolHandler(BaseHTTPRequestHandler):
        def __init__(self, request, client_address, server):
            try:
                self.sqlite = DatabaseObject(DB_CONFIG['SQLITE'])
                self.table_name = 'proxy'
            except Exception, e:
                self.sqlite = ''
                logger.error('SQLite error: %s', e)
            BaseHTTPRequestHandler.__init__(self, request, client_address, server)

        def do_GET(self):
            # num=1&port=80&type=3&protocol=http&area=北京
            if '/favicon.ico' in self.path:
                return
            params = parse_qs(urlparse(self.path).query)
            data = self.get_proxy(params)
            self.protocal_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(data)

        def get_proxy(self, params):
            where_dict = {'port': 'port', 'type': 'type', 'protocol': 'protocol', 'area': 'area'}
            conds = {
                'field': ['ip', 'port'],
                'order': ['updatetime desc', 'lastusedtime', 'score desc', 'speed'],
                'limit': 1,
                'where': [],
            }
            if params:
                for (k, v) in params.items():
                    try:
                        k = k.lower()
                        if k == 'num':
                            conds['limit'] = v[0]
                        elif k == 'area':
                            conds['where'].append((where_dict[k], 'like', '%%%s%%' % v[0]))
                        elif k == 'minscore':
                            conds['where'].append(('score', '>=', v[0]))
                        else:
                            conds['where'].append((where_dict[k], '=', v[0]))
                    except:
                        continue
            data = self.sqlite.select(self.table_name, conds)
            tmp = [{'ip': n[0], 'port': n[1], 'lastusedtime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} for
                   n in data]
            self.sqlite.update(self.table_name, tmp)
            data = ['%s:%s' % n for n in data]
            return json.dumps(data)

    def run(self):
        http_server = HTTPServer(('localhost', self.port), self.ProxyPoolHandler)
        logger.info('listened on localhost:%s' % API_CONFIG['PORT'])
        http_server.serve_forever()


if __name__ == '__main__':
    ProxyServer(API_CONFIG['PORT'])
