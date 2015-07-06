#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'Rodan'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column
from sqlalchemy.types import CHAR,Integer,String
from sqlalchemy.ext.declarative import declarative_base

from bottle import Bottle, run
from bottle import get, post, request  # or route
from bottle import template
from bottle import error
from bottle import response, abort, HTTPResponse

import json

import pdb

# init mysql database
import MySQLdb


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


BaseModel = declarative_base()

#connect the database,suppose there's no kvtest database
conn = MySQLdb.connect(host = 'localhost', port = 3306, user = 'root', passwd = 'a')
curs = conn.cursor()

#create a database named kvtest
#Ensure the program can run multiple times ,use try...exception
try:
    curs.execute('create database kvtest')
except:
    print 'Database kvtest exists!Use the existed one'

DB_CONNECT_STRING = 'mysql+mysqldb://root:a@localhost/kvtest?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo = False)

session = None
DB_Session = None


class KVpair(BaseModel):
    __tablename__ = 'kvDictionary'
    key = Column(String(500), primary_key=True)
    value = Column(String(500))


#create table kvDictionary
init_db()

class SessionCtx(object):
    '''
    just try to use with keyword =_=
    '''
    def __enter__(self):
        #use 'global' to tell python the variable engine is defined out of this func     
        global engine
        global session
        global DB_Session
        DB_Session = sessionmaker(bind = engine)
        session = DB_Session()
        self.should_cleanup = True
        return session

    def __exit__(self,exctype,excvalue,traceback):
        global session
        if self.should_cleanup:
            session.close()


def get_session():
    return SessionCtx()



kvapp = Bottle()

headers = dict()
headers['Content-Type'] = 'application/json'


@kvapp.get('/keys/<real_key>')  # or @route('/keys/<real_key>')
def getvalue(real_key):
    ''' find the value'''
    with get_session() as session:
        query = session.query(KVpair)
        result = query.filter(KVpair.key == real_key).first()

        if result is not None:
            print "request: %s" % result.key
            print "answer: %s" % result.value
            print '\n'
            bodyvaluedict = {result.key: result.value}
            body = json.dumps(bodyvaluedict)
            return HTTPResponse(body, status = 200, **headers)
        else:
            return HTTPResponse(' ', status = 404, **headers)
            #abort(404,"Sorry,not find the value of %s" % real_key)


@kvapp.post('/keys')  # or @route('/login',method = 'POST')
def do_post():
    with get_session() as session:
        headers = dict()
        headers['Content-Type'] = 'application/json'
        try:
            userKeyValuePairBody = request.json
        except Exception, e:
            # 请求的body部分不是json格式,返回400
            print "illegal request body"
            return HTTPResponse('illegal request body,not json',
                status = 400, **headers)
        else:
            #choose the first kvpair in body,只对提交的第一个kv对进行操作
            for k, v in userKeyValuePairBody.items():
                if isinstance(k, basestring):
                    kvpair = KVpair(key = k, value = str(v))
                    # 查询该key值是否在表中已经存在
                    query = session.query(KVpair)
                    testresult = query.filter(KVpair.key == k).first()
                    # 表中原来没有该key值，则将该kv键值对加入,返回200
                    if testresult is None:
                        session.add(kvpair)
                        session.commit()                      
                        storeResult = query.filter(KVpair.key == k).first()
                        return HTTPResponse('{%s : %s}' % (storeResult.key,
                            storeResult.value), status = 200, **headers)
                    # 表中原来有该key值，不作操作，返回419
                    else:
                        return HTTPResponse('already existed key',
                            status = 419, **headers)
                else:
                    # 用户提交的key部分不是字符串,返回400
                    return HTTPResponse('illegal request body,key is not string',
                        status = 400, **headers)
                break
        finally:
            pass




'''
session.execute('show databases').fetchall()
session.execute('use kvtest')
'''

'''
session.execute('drop table if exists kvDictionary')
session.execute('create table user (id int primary key, name text,
    email text, passwd text, last_modified real')
'''


'''add some initial key and values'''
'''kvpair = KVpair(key = 'luodan',value = '{"lunch":"rice"}')
session.add(kvpair)

kvpair = KVpair(key = 'gtt', value = '{"breakfase":"noodle"}')
session.add(kvpair)

session.commit()

query = session.query(KVpair)
print query
print query.statement

testresult = query.filter(KVpair.key == 'gtt').one()
print testresult
print 'result of gtt',testresult.value'''

if __name__=='__main__': 
    run(kvapp, host='localhost', port = 8080)


