import pymysql

class CardController(object):
    
    def sql_execute(self, sql):
        # 打开数据库连接
        db = pymysql.connect("localhost", "root", "123456", "card")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute(sql)
        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        return data
    
    def show_card(self, page=1, isbuy=10):
        if page <= 0:
            page = 1
        num = (page-1)*100
        if isbuy == 10:
            isbuy = (1, 0)
        elif isbuy in [1, 0]:
            isbuy = (isbuy, isbuy)
        sql = "select count(*) from texts where `isbuy` in %s ;" % str(isbuy)
        result = self.sql_execute(sql)
        count = result[0][0]
        sql = "select `isbuy`, `id`, `name` from texts where `isbuy` " \
              "in %s limit %s,%s;" % (isbuy, num, num+100)
        result = self.sql_execute(sql)
        data = {}
        for t in result:
            id = t[1]
            temp = {
                'is_buy': t[0],
                'name': t[2],
            }
            data[id] = temp
        json = {
            'count': count,
            'page_all': count//10,
            'page': page,
            'data': data
        }
        return json
    
    def buy_card(self, id):
        sql = "update texts set `isbuy`=1 where `id`=%s;" % (id)
        data = self.sql_execute(sql)
        return data
    
    def no_card(self, id):
        sql = "update texts set `isbuy`=0 where `id`=%s;" % (id)
        data = self.sql_execute(sql)
        return data
    
    def search_card(self, context, isbuy=0):
        if isbuy > 1:
            isbuy = 1
        if not context:
            return {}
        context = '%' + context + '%'
        print(context, isbuy)
        sql = "SELECT `isbuy`, `id`, `name` FROM texts " \
              "WHERE isbuy <= %d and " \
              "(`name` LIKE '%s' or `content` LIKE '%s');" \
              % (isbuy, context, context)
        result = self.sql_execute(sql)
        data = {}
        for t in result:
            id = t[1]
            temp = {
                'is_buy': t[0],
                'name': t[2],
            }
            data[id] = temp
        json = {
            'data': data
        }
        return json
    
    def count(self):
        sql = "select count(*) from texts where `isbuy` = 1 ;"
        data = self.sql_execute(sql)
        buy = data[0][0]
        sql = "select count(*) from texts ;"
        data = self.sql_execute(sql)
        all = data[0][0]
        result = {
            'buy': buy,
            'all': all,
            'rate': round(buy / all, 3)*100
        }
        return result
    
