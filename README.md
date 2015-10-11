# kvapp
kvstore
# 只读 KV 存储

使用 bottle.py 实现一个只读 k-v 存储服务，对外提供 RESTFul API，将 key-value 存储在 MySQL/ SQLite 中，
使用 SQLAlchemy 作为 ORM。

编码要求：
=============
符合 PEP8 规范，要求有单元测试，有合适的注释，源码使用 git 管理，推送到 github，
如果 github 被墙，可以放到 git.oschina.net 上。

API 定义如下：
=============

获取 value 接口：
-------------

用户指定需要获取的 key，接口将返回 key 对应的 value。如果 key 不存在则返回 HTTP 404。

请求：
----------
GET /keys/{real_key}

响应：
----------
HTTP 200

{
   {key}: {object}  
}

设置 value 接口：
------------------

用户通过 body 设置一个 key value 对，要求 key 必须是字符串，value 是任何合法的 json 对象。如果设置成功则返回存储后的结果；如果请求的 body 不是合法的 json 格式，则返回 HTTP 400，如果用户设置一个已经存在的 key，则返回 HTTP 419。

请求：
---------

POST /keys/

{
   {key}:{value}
   # key 类型为字符串，如"foo"
   # value 可以是任何合法的 json 对象，比如 "foo", true, 1, {"a":"b"}
}

响应：
---------

HTTP 200

{
   {key}: {value}  #将存储完成后的结果返回给用户
}


示例：
=====

设置 key＝“test”，value 为 {“openstack”: “nova”} 。

请求：
------

POST /keys

{ "test": {"openstack": "nova"}}

响应：
------

HTTP 200

{ "test": {"openstack": "nova"}}
获取 key ＝ “test” 的 value。

请求：
------

GET /keys/test

响应：
------

HTTP 200

{ "test": {"openstack": "nova"}}

