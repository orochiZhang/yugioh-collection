from elasticsearch import Elasticsearch
import pymysql

db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='card',
)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
sql = "select id, name, content, race from buy;"
cursor.execute(sql)
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()
es = Elasticsearch(['http://127.0.0.1:9200'], basic_auth=('elastic', '123456'))
for d in data:
    card_id, name, content, race = d[0], d[1], d[2], d[3]
    print('write', card_id, name)
    action = {
        "name": name,
        "content": content,
        "card_id": "Card" + str(card_id),
        "race": race,
    }
    es.index(index="card", document=action, id=card_id)

# 关闭数据库连接
db.close()