#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
# File Name:    server_main.py
# Author:       Andrew Chang
# Repo:         https://github.com/Andrew-M-C/python3-cgi-server
# License:      LGPL v2.1
#

import sys
# import threading
# import socket
import socketserver
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from socketserver import ThreadingMixIn
import urllib.parse

import cgi
from AMC import *


_SERVER_PORT = 23232


_handlers = {
    '/p3-cgi/test': cgi.rest.test,
    '/p3-cgi/restful': cgi.rest.restful,
}


_404_page = '''
<html>
<head><title>404 Not Found</title></head>
<body bgcolor="white">
<center><h1>404 Not Found</h1></center>
<hr><center>AMC Python Server</center>
</body>
</html>
'''

_403_page = '''
<html>
<head><title>403 Forbidden</title></head>
<body bgcolor="white">
<center><h1>403 Forbidden</h1></center>
<hr><center>AMC Python Server</center>
</body>
</html>
'''


_501_page = '''
<html>
<head><title>501 Not Implemented</title></head>
<body bgcolor="white">
<center><h1>501 Not Implemented</h1></center>
<hr><center>AMC Python Server</center>
</body>
</html>
'''


_400_page = '''
<html>
<head><title>400 Bad Request</title></head>
<body bgcolor="white">
<center><h1>400 Bad Request</h1></center>
<hr><center>AMC Python Server</center>
</body>
</html>
'''


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    'Handle requests in a separate thread.'
    pass


class CgiHandler(BaseHTTPRequestHandler):
    'Subclass of BaseHTTPRequestHandler'

    def _parse(self):
        parsed_path = urllib.parse.urlparse(self.path)

        session_para = {}
        query_para = urllib.parse.parse_qs(parsed_path.query)

        session_para['client_address'] = str(self.client_address[0])
        session_para['client_port'] = int(self.client_address[1])
        session_para['method'] = str(self.command)
        session_para['path'] = str(parsed_path.path)
        session_para['request_version'] = str(self.request_version)

        for name, value in sorted(self.headers.items()):
            session_para[name] = value.strip()

        return (session_para, query_para)

    def _write_resp(self, resp, conf={}):
        content_type = 'text/html'
        if resp is None:
            log.debug('response nothing')
            self.send_response(403)
            content_type = conf.get('Content-Type', 'text/html')
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(_403_page.encode('utf-8'))
        elif isinstance(resp, str):
            log.debug('response:\n%s' % resp)
            self.send_response(200)
            content_type = conf.get('Content-Type', 'application/text; charset=utf-8')     # 'text/plain; charset=utf-8')
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(resp.encode('utf-8'))
        elif isinstance(resp, bytes):
            log.debug('response:\n%s' % resp.decode('utf-8'))
            self.send_response(200)
            content_type = conf.get('Content-Type', 'application/plain; charset=utf-8')     # 'text/plain; charset=utf-8')
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(resp)
        else:
            self.send_response(200)
            self.end_headers()
        log.debug('Content-Type: %s' % content_type)
        return

    def do_HTTP(self):
        resp_headers = {}
        session_para, query_para = self._parse()
        path = session_para['path'].lower()
        handler_func = None

        # remove last '/'
        while path[-1] == '/':
            path = path[:-1]

        # now search for handler
        # log.debug('Search path: "%s"' % path)
        handler_func = _handlers.get(path, None)

        while handler_func is None:
            slash_index = path.rfind('/')
            if slash_index == -1:
                log.warn('Unrecognized path: "%s"' % session_para['path'])
                break
            else:
                path = path[:slash_index]
            handler_func = _handlers.get(path, None)

        if handler_func:
            content_len = int(session_para.get('Content-Length', 0))
            content_data = self.rfile.read(content_len)
            resp_data = handler_func(session_para, query_para, content_data, resp_headers)
            self._write_resp(resp_data, resp_headers)
        else:
            self.send_response(501)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(_501_page.encode('utf-8'))
        return

    def do_GET(self):
        self.do_HTTP()
        return

    def do_POST(self):
        self.do_HTTP()
        return

    def do_PUT(self):
        self.do_HTTP()
        return

    def do_DELETE(self):
        self.do_HTTP()
        return


class GuestServer(socketserver.StreamRequestHandler):   # 尚未完成

    def _parse(self, req_data):
        session_para = {}
        query_para = {}
        content_data = b''

        # 首先将 header 和正文分隔开来，查找 b'\r\n\r\n' 的位置
        split_bytes = '\r\n\r\n'.encode('utf-8')
        split_bytes_len = len(split_bytes)
        split_bytes_offset = req_data.find(split_bytes)
        log.debug('Header length %d, data length %d' %
                  (int(split_bytes_offset), int(len(req_data) - split_bytes_offset - split_bytes_len)))

        header_bytes = req_data[0:split_bytes_offset]
        content_data = req_data[split_bytes_offset + split_bytes_len:]
        header = header_bytes.decode('utf-8')
        log.debug('header:\n%s' % header)
        log.debug('content data:\n%s' % str(content_data))

        return (session_para, query_para, content_data)

    def handle(self):
        log.debug('Got connection')
        log.debug('Got connection from %s' % str(self.client_address))

        req_data = self.request.recv(10240)
        # log.debug('Got data:\n<BEGIN>\n%s\n<ENG>' % str(req_data))

        session_para, query_para, content_data = self._parse(req_data)
        return


def main():
    # log.set_log_file_path('new_log.log')
    socketserver.TCPServer.allow_reuse_address = True
    if 1:
        server = ThreadedHTTPServer(('localhost', _SERVER_PORT), CgiHandler)
    else:
        server = socketserver.ThreadingTCPServer(('127.0.0.1', _SERVER_PORT), GuestServer)
    address = server.server_address
    log.info('%s starts, address: %s:%d' % (sys.argv[0], address[0], address[1]))
    server.serve_forever()
    return


if __name__ == '__main__':
    # sys.settrace(trace)
    # log.set_log_level(log.LOG_DEBUG)
    # log.set_identifier(sys.argv[0])

    log.console_level = log.LOG_DEBUG
    log.file_level = log.LOG_INFO
    log.set_log_identifier(sys.argv[0])

    lang.set_stdout_encoding('utf-8')
    log.debug('stdout encoding: %s' % lang.get_stdout_encoding())
    ret = main()

    if ret is None:
        ret = 0
    sys.exit(ret)
