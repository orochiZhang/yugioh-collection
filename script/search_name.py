# -*- coding: UTF-8 -*-
import pymysql

# 由于翻译不同，需要搜索确认是否有这个卡牌

name_list = []


# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "card")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

over2 = []
not_found = []

for name in name_list:
    sql = "select count(`id`), `name` from texts where `name` = '%s' " % name
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)
    result = cursor.fetchall()
    for d in result:
        if not d:
            not_found.append(name)
        if d and d[0] > 1:
            over2.append(name)
        if d and d[0] == 0:
            not_found.append(name)
print('无法匹配，请确认', not_found)
print('匹配大于2，请确认', over2)
db.close()