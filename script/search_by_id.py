# -*- coding: UTF-8 -*-
import pymysql

# 根据卡密搜索卡片，卡密数据可能存在错误

name_list = data = [


]

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "card")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
id_list = []
for data in name_list:
    for t in data:
        id_list.append(t[1])
        sql = "select `id`, `name` from texts where `id` = %s;" % t[1]
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute(sql)
        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchall()
        if not data:
            print("找不到 %s" % t[1])

id_str = str(id_list).replace('[', '(').replace(']', ')')
sql = "select `id`, `name` from texts where `id` in %s;" % id_str
# 使用 execute()  方法执行 SQL 查询
cursor.execute(sql)
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()
for d in data:
    print(d)