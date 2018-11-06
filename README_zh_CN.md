[English](https://github.com/Andrew-M-C/python3-cgi-server) | **简体中文**

# Python3 CGI Server

本仓库是一个基于 Python 3.5 以上版本的 HTTP 服务器，程序员们可以使用这个来构建一个简单的 HTTP demo。

# 使用前准备

首先，你需要将本仓库 clone 到本地。然后，本项目还依赖于我自己的一个 [Python3 工具库](https://github.com/Andrew-M-C/python3_tools)。因此，在执行之前也需要下载这个库。具体方法是：

```
$ cd ext-libs
$ git clone https://github.com/Andrew-M-C/python3_tools
$ cd -
```

# 启动服务器

在本 demo 中，本人将服务藏在了 nginx 反向代理后面。然后，在工作目录下执行 `python3 server_main.py`即可启动服务。

# 使用方法

## 注册一个新路径

在 `server_main.py` 文件中，修改 `_handlers` 字典变量。其中字典的 key 是路径名（以 "`/`" 开始，但不能以 "`/`" 结束）；而字典的 value 则是处理函数名。示例代码中给出了两个，分别是处理 "`/p3-cgi/test`" 和 "`/p3-cgi/restful`" 的 API。

## 路径匹配原则

对于一个完整的路径，其匹配顺序为：

1. 首先进行全路径匹配，路径末尾的所有连续的斜杠符 "`/`" 均会被忽略
2. 如果全路径匹配未命中，则逐步减少斜杠部分，直至匹配命中
3. 如果到达根路径均未能匹配，则返回 501 错误

## 撰写处理函数

这里可以参见代码中的 `cgi/rest.py` 文件的 `test()` 函数。我们主要说明函数的几个参数以及返回值：

- `session_para`：表示会话参数，实际上是 HTTP 请求的一些主要参数。参见 `server_main.py` 的 `CgiHandler._parse()` 函数。其中最有用的是 `method` 和 `path` 成员。
- `query_para`：这表示 "query parameters"，也就是通常在发出请求时，跟在 URL 路径后面、以问号 "`?`" 分割的那一串键值对。这是一个字典类型参数。
- `content_data`： 这是请求带上的 HTTP body content。其实除了 POST，DELETE、PUT 等也会带上参数。
- `resp_headers`：该变量作为返回值用。如果需要自定义 HTTP 返回的 header 中的内容，可以修改该字典的对应值。不过目前只支持 "`Content-Type`" 的修改。
- 返回值：可以支持直接返回这些类型：`bytes`, `string`, `None`。

# RESTful API 示例

在 demo 中，路径 "`/p3-cgi/restful`" 是一个 RESTful API 的 GET 方法示例。代码中定义了一个简单的资源树，然后解析请求的 URI，并且将 URI 对应的资源返回给前端。

这里比较特别的是，对于资源节点，API 只返回下一级节点的名称列表，只有对叶子结点才会返回完整的资源信息。

你可以访问以下路径感受一下:

- https://andrewmc.cn/p3-cgi/restful/
- https://andrewmc.cn/p3-cgi/restful/people
- https://andrewmc.cn/p3-cgi/restful/people/teachers/001