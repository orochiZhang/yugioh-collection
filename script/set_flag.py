# -*- coding: UTF-8 -*-
import pymysql

# 批量标记已有的游戏王卡片

name_list = []

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "card")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
sql = "select `id`, `name` from texts where `name` like '%No.%'"
# sql = "select `id` from text where `name` in %s " % name_list

# 使用 execute()  方法执行 SQL 查询
cursor.execute(sql)
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()
for d in data:
    
    if d[1] in ['No.3 地狱蝉王', 'No.10 黑辉士 启明者']:
        continue
    sql = "update buy set `isbuy`=1 where `id`=%s;" % d[0]
    result = cursor.execute(sql)

db.close()
