# -*- coding: UTF-8 -*-
import pymysql

# 根据text数据库数据去更新buy数据的数据。默认isbuy = 0

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "card")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
sql = "select `id` from texts"
# 使用 execute()  方法执行 SQL 查询
cursor.execute(sql)
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()

for t in data:
    id = t[0]
    sql2 = "select `id` from buy where `id` = %s" % id
    cursor.execute(sql2)
    data = cursor.fetchall()

    if not data:
        sql3 = "insert into buy (`id`, `isbuy`) values (%s, %s)" % (id, 0)
        cursor.execute(sql3)

# 关闭数据库连接
db.close()
