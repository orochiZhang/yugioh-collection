# -*- coding: UTF-8 -*-
import pymysql
import logging


class CardController(object):
    def __init__(self):
        self.logger = logging.getLogger("CardController")
        fh = logging.FileHandler('./log/change.log', mode='a', encoding="utf-8")  # 定义一个写文件的handler
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter(fmt='[%(asctime)s-%(levelname)s:%(message)s]', datefmt='%Y-%m-%d %I:%M:%S %p'))
        self.logger.addHandler(fh)  # 将handler加入logger
    
    def sql_execute(self, sql, arg):
        # 打开数据库连接
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
        cursor.execute(sql, arg)
        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchall()
        # 关闭数据库连接
        db.close()
        return data
    
    # 查询所有/已有/没有
    def show_card(self, page=1, isbuy=10):
        page = 1 if page <= 0 else page
        num = (page - 1) * 100
        isbuy = (1, 0) if isbuy == 10 else (isbuy, isbuy)
        
        sql = "select count(*) from buy where `isbuy` in %s ;"
        count = self.sql_execute(sql, (isbuy,))[0][0]
        
        sql = "select `id`, `name`, `isbuy` from buy where `isbuy` in %s limit %s, %s;"
        result = self.sql_execute(sql, (isbuy, num, num + 100))
        data = {}
        for t in result:
            card_id, name, buy_flag = t[0], t[1], t[2]
            if buy_flag in isbuy:
                data[card_id] = {}
                data[card_id]['isbuy'] = buy_flag
                data[card_id]['name'] = name
        return {
            'count': count,
            'page_all': count // 10,
            'page': page,
            'data': data
        }
    
    # 标记为已有
    def buy_card(self, id):
        sql = "update buy set `isbuy`=1 where `id`=%s;"
        result = self.sql_execute(sql, (id,))
        self.logger.log(logging.INFO, "Set Buy Flag By id %s" % id)
        return result
    
    # 标记为没有
    def no_card(self, id):
        sql = "update buy set `isbuy`=0 where `id`=%s;"
        result = self.sql_execute(sql, (id,))
        self.logger.log(logging.INFO, "Set NoBuy Flag By id %s" % id)
        return result
    
    # 卡密，卡名，效果的模糊搜索
    def search_card(self, context, isbuy=10):
        if not context:
            return {}
        isbuy = (1, 0) if isbuy > 1 else (isbuy, isbuy)
        # if True:
        #     data = self.search_card_by_es(context, isbuy)
        #     return data
        
        context = '%' + context + '%'
        sql = "SELECT `id`, `name`, `isbuy`, `atk` FROM buy WHERE " \
              "(`name` LIKE %s or `content` LIKE %s or `id` LIKE %s" \
              "or `race` LIKE %s);"
        result = self.sql_execute(sql, (context, context, context, context))
        data = {}
        for t in result:
            card_id, name, buy_flag, atk = t[0], t[1], t[2], t[3]
            if buy_flag in isbuy:
                data[card_id] = {}
                data[card_id]['isbuy'] = buy_flag
                data[card_id]['name'] = name
                data[card_id]['atk'] = atk
        return {'data': data}
    
    def search_card_by_es(self, context, isbuy):
        from elasticsearch import Elasticsearch
        query = {
            "bool": {
                "should": [
                    {"wildcard": {
                        "card_id": {
                            "value": "*"+context+"*"
                        }, }},
                    {"match_phrase": {"content": context}, },
                    {"match_phrase": {"name": context}, },
                ]
            }
            
        }
        es = Elasticsearch(['http://127.0.0.1:9200'], basic_auth=('elastic', '123456'))
        data = es.search(index="card", query=query, source=["name", ], size=10000)
        return_data = {}
        for d in data['hits']['hits']:
            card_id = d['_id']
            name = d['_source']['name']
            return_data[card_id] = {}
            return_data[card_id]['name'] = name

        id_list = [int(x) for x in return_data.keys()]
        sql = "SELECT `id`, `isbuy`, `atk` FROM buy WHERE `id` in %s;"
        result = self.sql_execute(sql, (id_list,))
        
        for t in result:
            card_id, buy_flag, atk = str(t[0]), t[1], t[2],
            if buy_flag in isbuy:
                return_data[card_id]['isbuy'] = buy_flag
                return_data[card_id]['atk'] = atk
        return {'data': return_data}

    # 卡名模糊搜索
    def search_card_by_name(self, context, isbuy=10):
        if not context:
            return {}
        isbuy = (1, 0) if isbuy > 1 else (isbuy, isbuy)
        context = '%' + context + '%'
        sql = "SELECT `id`, `name`, `isbuy` FROM buy WHERE (`name` LIKE %s);"
        result = self.sql_execute(sql, (context,))
        data = {}
        for t in result:
            card_id, name, buy_flag = t[0], t[1], t[2]
            if buy_flag in isbuy:
                data[card_id] = {}
                data[card_id]['isbuy'] = buy_flag
                data[card_id]['name'] = name
        return {'data': data}
    
    # 卡包编号模糊搜索
    def search_card_by_pack_number(self, context, isbuy=10):
        if not context:
            return {}
        index = -1
        isbuy = (1, 0) if isbuy > 1 else (isbuy, isbuy)
        context = '%' + context + '%'
        sql = "SELECT `card_id`, `card_no`, `rare` FROM packinfo WHERE (`card_no` LIKE %s);"
        result = self.sql_execute(sql, (context,))
        data = {}
        id_list = []
        for t in result:
            card_id, card_no, rare = t[0], t[1], t[2]
            if card_id:
                id_list.append(card_id)
            else:
                card_id = index
                index -= 1
            data[card_id] = {'name': card_no + " " + rare}
        if not id_list:
            return {'data': data}
        
        sql = "SELECT `id`, `name`, `isbuy` FROM buy WHERE `id` in %s"
        result = self.sql_execute(sql, (id_list,))
        
        for t in result:
            card_id, name, buy_flag = t[0], t[1], t[2]
            if buy_flag not in isbuy:
                del data[card_id]
            else:
                data[card_id]['name'] += (" " + name)
                data[card_id]['isbuy'] = buy_flag
        return {'data': data}
    
    def count(self):
        sql = "select count(*) from buy where `isbuy` = 1 ;"
        buy = self.sql_execute(sql, None)[0][0]
        sql = "select count(*) from buy ;"
        all = self.sql_execute(sql, None)[0][0]
        sql = "SELECT count(*) FROM `buy` WHERE `name` LIKE '%衍生物%'"
        not_count = self.sql_execute(sql, None)[0][0]
        all -= not_count
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
        index = -1
        sql = "select `card_id`, `card_no`, `rare` from packinfo where `series` = %s and pack = %s;"
        data = self.sql_execute(sql, (series, pack))
        for d in data:
            card_id, card_no, rare = d[0], d[1], d[2]
            if card_id:
                id_list.append(card_id)
            else:
                card_id = index
                index -= 1
            result[card_id] = {
                "card_no": card_no,
                "rare": rare,
                'name': card_no + " " + rare + " "
            }
        
        if id_list:
            sql = "select `id`, `name`, `isbuy` FROM buy WHERE `id` in %s;"
            data = self.sql_execute(sql, (id_list,))
            for d in data:
                card_id, name, isbuy = d[0], d[1], d[2]
                result[card_id]["name"] += name
                result[card_id]["isbuy"] = isbuy
        return result
