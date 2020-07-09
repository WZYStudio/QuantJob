import pymysql
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from demo.mysql_job.tick import Tick
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.dialects.mysql import (INTEGER, CHAR)
from sqlalchemy import Column, Table, MetaData

Base = declarative_base()


def pymysql_demo1():
    conn = pymysql.connect('192.168.50.100', 'wzy', '123', port=3306)

    # Step1 查看是否有db， 注意其实也是模糊查询；正确操作应该是 create dbName if not exist dbName
    cursor = conn.cursor()
    cursor.execute("show databases like '%myTestD%'")
    results = cursor.fetchall()
    print('show db result is:' + str(len(results)) + str(results[0]))

    # Step2 锁定了使用这个db
    cursor.execute('use myTestDB')

    # Step3 查询是否有某个表,也是模糊查询； 正确操作应该是 create table if not exists
    cursor.execute("SELECT  * from myTestTable")
    cursor.execute("show tables like '%myTestTabl%'")
    results = cursor.fetchall()
    print('show table result is:' + str(len(results)) + str(results[0]))

    # Step4 查询数据
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        name = row[1]
        msg = row[2]
        # print('name is:%s,msg is %s' % (name, msg))
        print('id is:' + str(id) + ' name is' + name + '  msg is:' + msg)

    conn.close()
    return


def sqlalchemy_demo1():
    my_stock_db = 'mystock_db'
    engine = create_engine("mysql+pymysql://wzy:123@192.168.50.100/" + my_stock_db + "?charset=utf8", echo=True)

    # 如果没有数据库，就建库, 借助了sqlalchemy_utils包
    if not database_exists(engine.url):
        create_database(engine.url)

    # 建表成功, 自己去扫描Tick类，对我无感, 我觉得这个建表方法我不会用..
    # my_tick = Tick()
    Base.metadata.create_all(engine)

    # 另一种建表方法， 不需要类，这种比较符合过程思维
    meta = MetaData()
    stock_2_table = Table('stock_2_table', meta, Column('id', INTEGER, primary_key=True), Column('name', CHAR(127)),
                          Column('password', CHAR(127)))
    stock_2_table.create(bind=engine)

    # 插入数据
    # return


if __name__ == '__main__':
    # pymysql_demo1()
    sqlalchemy_demo1()
