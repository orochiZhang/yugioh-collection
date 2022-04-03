# -*- coding: UTF-8 -*-
import pymysql
import logging

logging.basicConfig(filename='../log/change.log', encoding="utf8",
                    format='[%(asctime)s-%(levelname)s:%(message)s]', level=logging.DEBUG, filemode='a',
                    datefmt='%Y-%m-%d %I:%M:%S %p',)
# 批量标记已有的游戏王卡片，根据卡名

s = """
异次元的指名者x1 拼图友爱天使x1 机怪兽 达莱特龙x1 爬虫妖女·梅露辛x1 超重武者 魂-Cx1 SIMM标签貘x1 天穹之圣像骑士x1 魔神仪-蜡烛人偶x1 明星之机械骑士x1 极超流星x1 零型额外连接x1 孤毒之剑x1 预见存折x1 单一化x1 庄家选择x1 北极天熊-帝车x1 机关傀儡-基冈提斯人偶x1 创世者的化身x1 白衣忍者x1 秩序守护者x1 急兔马x1 能量吸收板x1 电脑堺凰-凰凰x1 武神-日孁x1 巨神龙 闪耀x1 光辉精灵x1 天刑王 黑天x1

"""
s = s.replace('x2', 'x1')
s = s.replace('x3', 'x1')
s = s.strip('\n')
s = s.strip(' ')
s = s.strip('x1')
name_list = s.split('x1 ')
print(name_list)

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "card")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
name_str = str(name_list).replace('[', '(').replace(']', ')')
sql = "select `id`, `name` from buy where `name` in %s;" % name_str
# sql = "select `id` from text where `name` in %s " % name_list

# 使用 execute()  方法执行 SQL 查询
cursor.execute(sql)
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()
for d in data:
    sql = "update buy set `isbuy`=1 where `id`=%s;" % d[0]
    result = cursor.execute(sql)

db.close()
logging.log(logging.INFO, "SetFlag By Name %s" % name_list)
