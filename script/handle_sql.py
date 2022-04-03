# -*- coding: UTF-8 -*-
# 脚本逻辑，处理DataEditorX导出的sql文件，提取需要的数据，写入mysql
import re
import pymysql

data_dict = {}

race_dict = {
    0x1: "战士族",
    0x2: "魔法师族",
    0x4: "天使族",
    0x8: "恶魔族",
    0x10: "不死族",
    0x20: "机械族",
    0x40: "水族",
    0x80: "炎族",
    0x100: "岩石族",
    0x200: "鸟兽族",
    0x400: "植物族",
    0x800: "昆虫族",
    0x1000: "雷族",
    0x2000: "龙族",
    0x4000: "兽族",
    0x8000: "兽战士族",
    0x10000: "恐龙族",
    0x20000: "鱼族",
    0x40000: "海龙族",
    0x80000: "爬虫类族",
    0x100000: "念动力族",
    0x200000: "幻神兽族",
    0x400000: "创造神族",
    0x800000: "幻龙族",
    0x1000000: "电子界族",
}

# 卡片类型
type_dict1 = {
    0x1: "怪兽",
    0x2: "魔法",
    0x4: "陷阱",
}

# 怪兽分类
type_dict2 = {
    0x8: "N/A",
    0x10: "通常",
    0x20: "效果",
    0x40: "融合",
    0x80: "仪式",
    0x100: "N/A",
    0x200: "灵魂",
    0x400: "同盟",
    0x800: "二重",
    0x1000: "调整",
    0x2000: "同调",
    0x4000: "衍生物",
    0x8000: "N/A",
    0x200000: "反转",
    0x400000: "卡通",
    0x800000: "超量",
    0x1000000: "灵摆",
    0x2000000: "特殊召唤",
    0x4000000: "连接",
}

# 魔法陷阱
type_dict3 = {
    0x10000: "速攻",
    0x20000: "永续",
    0x40000: "装备",
    0x80000: "场地",
    0x100000: "反击",
}

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "card")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

def handle_data(s):
    global data_dict
    data_re = re.compile(r'\((.*?)\)', re.DOTALL)
    result = data_re.findall(s)
    if result:
        result = str(result[0])
        result_list = result.split(',')
        # 编号，x, x, x, 类型, atk, def, level, race, x, x
        # (10000,3,0,0x0,0x2000021,-2,-2,0xa,0x2000,0x20,0x42000);
        card_id, _, _, _, card_type, atk, den, level, race, _, _ = result_list
        race = int(race, base=16)
        race = race_dict.get(race, "-")
        level = int(level, base=16)
        level = int(level & 0xFF)
        card_type = int(card_type, base=16)
        card_type_list = []
        for k, v in type_dict1.items():
            if card_type & k == k:
                card_type_list.append(v)
                if k == 0x1:
                    for k, v in type_dict2.items():
                        if card_type & k == k:
                            card_type_list.append(v)
                else:
                    for k, v in type_dict3.items():
                        if card_type & k == k:
                            card_type_list.append(v)
        
        if card_id not in data_dict:
            data_dict[card_id] = {}
        data_dict[card_id]['card_type'] = "·".join(card_type_list)
        data_dict[card_id]['atk'] = atk
        data_dict[card_id]['den'] = den
        data_dict[card_id]['level'] = level
        data_dict[card_id]['race'] = race
        

def handle_text(s):
    global data_dict
    data_re = re.compile(r'\((.*?)\)', re.DOTALL)
    result = data_re.findall(s)
    if result:
        result = str(result[0])
        result_list = result.split(",'")
        card_id = result_list[0]
        card_name = result_list[1].strip("'")
        card_content = result_list[2].strip("'")
        if card_id not in data_dict:
            data_dict[card_id] = {}
        data_dict[card_id]['card_name'] = card_name
        data_dict[card_id]['card_content'] = card_content

key = ['card_name', 'card_content', 'card_type', 'atk', 'den', 'level', 'race']

update_all = True

def write_db():
    global data_dict
    
    for card_id, data in data_dict.items():
        illegal = False
        for k in key:
            if k not in data:
                illegal = True
                break
        if illegal:
            print('数据不合法>>>>', data)
            continue
        card_name = data['card_name']
        card_content = data['card_content']
        card_type = data['card_type']
        atk = data['atk']
        den = data['den']
        level = data['level']
        race = data['race']
        
        sql = "select `id` from buy where id = %s"
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute(sql, (card_id,))
        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchone()
        if data:
            if not update_all:
                return
            # 更新数据
            sql = "UPDATE `buy` SET `name`=%s,`content`=%s,`attr`=%s,`race`=%s,`atk`=%s,`def`=%s, `level`=%s WHERE `id`=%s"
            args = (card_name, card_content, card_type, race, atk, den, level, card_id)
            cursor.execute(sql, args)
        else:
            # 新增数据，插入
            sql = "INSERT INTO `buy`(`id`, `name`, `content`, `attr`, `race`, `atk`, `def`, `level`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (card_id, card_name, card_content, card_type, race, atk, den, level)
            cursor.execute(sql, args)
    data_dict = {}
        
print('数据处理中……')
with open("card.sql", "r", encoding='utf-8-sig') as f:
    s = f.readline()
    i = 0
    index = 0
    temp = None
    n = 0
    while s:
        if temp:
            temp += s
        if ";" not in s:
            # 先缓存
            if temp:
                temp += s
            else:
                temp = s
        else:
            if temp:
                s = temp + s
                temp = None
            if "datas" in s:
                handle_data(s)
            elif "texts" in s:
                handle_text(s)
                write_db()
                n += 1
        if n % 100 == 0:
            print('数据处理进度:', n)
        s = f.readline()
print('数据处理完成……')