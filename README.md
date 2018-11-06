**English** | [简体中文](https://github.com/Andrew-M-C/python3-cgi-server/blob/master/README_zh_CN.md)

# Python3 CGI Server

This repo is a HTTP server based on Python 3.5+, which programmers can quickly build a HTTP demo with.

# Before Use

First of all, you should clone this repo to local. As this repo depends on a small [Python3 tool](https://github.com/Andrew-M-C/python3_tools), it should be downloaded before use. Detailed operations are as below:

```
$ cd ext-libs
$ git clone https://github.com/Andrew-M-C/python3_tools
$ cd -
```

# Start Server

I have hidden this server after nginx reversed-proxy. I also suggest you do so. Then, execute `python3 server_main.py` command at work path to start this server.

# Way to Use

You can quickly develop your own HTTP service as follow:

## Register a New Path

Update the dictionary-typed variable named `_handlers` in `server_main.py` file. Add handler pairs you designed. The key of which is HTTP path name, and the value the handler function. Keys should NOT ended with one or more slashes.

In this demo, I designed two handlers, with path "`/p3-cgi/test`" and "`/p3-cgi/restful`".

## Path Matching Principle

The matching principle for a complete HTTP request path are:

1. Fully match the path. If any handler hits, invokes it. the trailing slashes will be ignored.
2. If full matching does not hit, parts separated by slashed will be removed one by one from the trailing, until any of the remains hits
3. If no handlers hit till root path, returns 501 error.

## Write your Own Handlers

Please refer to `test()` function in File `cgi/rest.py`. Here are the description of parameters and return value:

- `session_para`：session parameter, dict type. This dict stores some main parameters in HTTP request. The function `CgiHandler._parse()` shows what they are. The most important ones are `method` and `path`.
- `query_para`：query parameters，dict type.
- `content_data`：HTTP content body data, byte type. 
- `resp_headers`：This parameter is a dictionary, used for returning. If you want to specify HTTP response header, please modify this dict. However, only "Content-Type" is supported currently.
- return value: Supports following types: `bytes`, `string`, `None`.

# RESTful API Example

In this demo, the path "`/p3-cgi/restful`" is an example for RESTful API GET method. It will return resources requested by HTTP client.

Specially, this API returns sub-resource names for resource nodes, while whole resource infomation for resource leaves.