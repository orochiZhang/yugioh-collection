# -*- coding: UTF-8 -*-

import pymysql

class CardController(object):
    
    def sql_execute(self, sql, arg):
        # 打开数据库连接
        db = pymysql.connect("localhost", "root", "123456", "card")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute(sql, arg)
        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        return data
    
    # 查询所有/已有/没有
    def show_card(self, page=1, isbuy=10):
        page = 1 if page <= 0 else page
        num = (page-1) * 100
        isbuy = (1, 0) if isbuy == 10 else (isbuy, isbuy)
        
        sql = "select count(*) from buy where `isbuy` in %s ;"
        count = self.sql_execute(sql, (isbuy,))[0][0]
        
        sql = "select `id`, `isbuy` from buy where `isbuy` in %s limit %s, %s;"
        result = self.sql_execute(sql, (isbuy, num, num+100))
        data = {}
        for t in map(lambda t: {t[0]: {'isbuy': t[1]}}, [t for t in result]):
            data.update(t)
        
        if data:
            sql = "select `id`, `name` from texts where `id` in %s"
            for t in self.sql_execute(sql, (list(data.keys()),)):
                data[t[0]]["name"] = t[1]
        return {
            'count': count,
            'page_all': count//10,
            'page': page,
            'data': data
        }

    # 标记为已有
    def buy_card(self, id):
        sql = "update buy set `isbuy`=1 where `id`=%s;"
        result = self.sql_execute(sql, (id,))
        return result
    
    # 标记为没有
    def no_card(self, id):
        sql = "update buy set `isbuy`=0 where `id`=%s;"
        result = self.sql_execute(sql, (id,))
        return result
    
    # 卡密，卡名，效果的模糊搜索
    def search_card(self, context, isbuy=10):
        if not context:
            return {}
        isbuy = (1, 0) if isbuy > 1 else (isbuy, isbuy)
        context = '%' + context + '%'
        sql = "SELECT `id`, `name` FROM texts WHERE (`name` LIKE %s or `content` LIKE %s or `id` LIKE %s);"
        result = self.sql_execute(sql, (context, context, context))
        data = {}
        id_list = []
        for t in result:
            id_list.append(t[0])
            data[t[0]] = {'name': t[1]}
        if not id_list:
            return {'data': data}
        
        sql = "SELECT `id`, `isbuy` FROM buy WHERE `id` in %s"
        result = self.sql_execute(sql, (id_list,))
        for t in result:
            if t[1] not in isbuy:
                del data[t[0]]
            else:
                data[t[0]]['isbuy'] = t[1]
        return {'data': data}

    # 卡名模糊搜索
    def search_card_by_name(self, context, isbuy=10):
        if not context:
            return {}
        isbuy = (1, 0) if isbuy > 1 else (isbuy, isbuy)
        context = '%' + context + '%'
        sql = "SELECT `id`, `name` FROM texts WHERE (`name` LIKE %s);"
        result = self.sql_execute(sql, (context,))
        data = {}
        id_list = []
        for t in result:
            id_list.append(t[0])
            data[t[0]] = {'name': t[1]}
        if not id_list:
            return {'data': data}
    
        sql = "SELECT `id`, `isbuy` FROM buy WHERE `id` in %s"
        result = self.sql_execute(sql, (id_list,))
        for t in result:
            if t[1] not in isbuy:
                del data[t[0]]
            else:
                data[t[0]]['isbuy'] = t[1]
        return {'data': data}

    # 卡包编号模糊搜索
    def search_card_by_pack_number(self, context, isbuy=10):
        if not context:
            return {}
        isbuy = (1, 0) if isbuy > 1 else (isbuy, isbuy)
        context = '%' + context + '%'
        sql = "SELECT `card_id`, `card_no`, `rare` FROM packinfo WHERE (`card_no` LIKE %s);"
        result = self.sql_execute(sql, (context,))
        data = {}
        id_list = []
        for t in result:
            card_id, card_no, rare = t[0], t[1], t[2]
            id_list.append(card_id)
            data[t[0]] = {'name': card_no +" "+ rare}
        if not id_list:
            return {'data': data}

        sql = "SELECT `id`, `name` FROM texts WHERE `id` in %s;"
        result = self.sql_execute(sql, (id_list,))
        for t in result:
            card_id, name = t[0], t[1]
            data[card_id]['name'] += (" " + name)
    
        sql = "SELECT `id`, `isbuy` FROM buy WHERE `id` in %s"
        result = self.sql_execute(sql, (id_list,))
        for t in result:
            if t[1] not in isbuy:
                del data[t[0]]
            else:
                data[t[0]]['isbuy'] = t[1]
        return {'data': data}
    
    def count(self):
        sql = "select count(*) from buy where `isbuy` = 1 ;"
        buy = self.sql_execute(sql, None)[0][0]
        sql = "select count(*) from buy ;"
        all = self.sql_execute(sql, None)[0][0]
        return {
            'buy': buy,
            'all': all,
            'rate': round(buy / all * 100, 3)
        }
    
    def get_pack_list(self):
        sql = "select `series`, `pack` from pack"
        data = self.sql_execute(sql, None)
        result = {}
        for d in data:
            series = d[0]
            pack = d[1]
            if series not in result:
                result[series] = [pack]
            else:
                result[series].append(pack)
        return result

    def get_pack_info(self, series, pack):
        result = {}
        id_list = []
        
        sql = "select `card_id`, `card_no`, `rare` from packinfo where `series` = %s and pack = %s;"
        data = self.sql_execute(sql, (series, pack))
        for d in data:
            result[d[0]] = {"card_no": d[1], "rare": d[2]}
            id_list.append(d[0])

        if id_list:
            sql = "select `id`, `name` FROM texts WHERE `id` in %s;"
            data = self.sql_execute(sql, (id_list,))
            for d in data:
                result[d[0]]["name"] = d[1]
        
            sql = "select `id`, `isbuy` from buy WHERE `id` in %s;"
            data = self.sql_execute(sql, (id_list,))
            for d in data:
                result[d[0]]["isbuy"] = d[1]
        return result
