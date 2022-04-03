# -*- coding: UTF-8 -*-
import pymysql

# 由于翻译不同，需要搜索确认是否有这个卡牌

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

over2 = []
not_found = []

for name in name_list:
    sql = "select count(`id`), `name` from buy where `name` = '%s' " % name
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
