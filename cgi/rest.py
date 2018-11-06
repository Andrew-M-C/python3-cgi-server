#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
# File Name:    rest.py
# Author:       Andrew Chang
# Repo:         https://github.com/Andrew-M-C/python3-cgi-server
# License:      LGPL v2.1
#

import sys
import json
from AMC import *


# This is a RESTful API example which can be accessed by uri
_resource_str = '''
{
    "people": {
        "students": {
            "001": {
                "name": "Harry Potter"
            },
            "002": {
                "name": "Hermione Granger"
            },
            "003": {
                "name": "Ron Weasley"
            }
        },
        "teachers": {
            "001": {
                "name": "Albus Dumbledore"
            },
            "002": {
                "name": "Severus Snape"
            },
            "003": {
                "name": "Minerva McGonagall"
            }
        }
    },
    "houses": {
        "gryffindor": {
            "founder": "Godric Gryffindor"
        },
        "hufflepuff": {
            "founder": "Helga Hufflepuff"
        },
        "ravenclaw": {
            "founder": "Rowena Ravenclaw"
        },
        "slytherin": {
            "founder": "Salazar Slytherin"
        }
    }
}
'''

_restful_resources = {}


# reply query
def restful(session_para, query_para, content_data, resp_headers):
    message = {}
    resp_headers['Content-Type'] = 'application/json; charset=utf-8'
    method = session_para['method']
    path = session_para['path']

    log.debug("HTTP verb: %s" % method)
    if method != 'GET':
        message['code'] = -1
        message['msg'] = 'this demo does not support %s' % method
        return json.dumps(message)

    while path[-1] == '/':
        path = path[:-1]

    res_parts = path.split('/')
    parts_len = len(res_parts)
    log.debug('parts: %s' % res_parts)
    search_index = 3
    query_obj = _restful_resources

    while search_index < parts_len:
        part = res_parts[search_index]
        if 0 == len(part):
            search_index += 1
            continue
        tmp_obj = query_obj.get(part, None)
        if tmp_obj is None:
            query_obj = None
            break
        else:
            query_obj = tmp_obj
            search_index += 1

    # check return
    if query_obj is None:
        message['code'] = -1
        message['msg'] = 'resource not found'
        message['data'] = {}
    else:
        message['code'] = 0
        message['msg'] = 'success'
        if isinstance(query_obj, dict) is False:
            message['data'] = query_obj
        elif isinstance(list(query_obj.values())[0], dict):
            message['data'] = list(query_obj.keys())
        else:
            message['data'] = query_obj

    return json.dumps(message)


# uri access
def test(session_para, query_para, content_data, resp_headers):
    message = {}
    message['session'] = session_para
    message['query'] = query_para
    resp_headers['Content-Type'] = 'application/json; charset=utf-8'
    return json.dumps(message)


def _init():
    global _restful_resources
    _restful_resources = json.loads(_resource_str)
    # log.debug('resources: \n%s' % _restful_resources)
    return


if __name__ == '__main__':
    sys.exit(-1)
else:
    _init()
