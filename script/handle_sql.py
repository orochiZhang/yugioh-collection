# -*- coding: UTF-8 -*-

# 脚本逻辑，处理DataEditorX导出的sql文件，转变成多个小文件，并且改为mysql能使用的语法

data_new = "replace INTO `datas` (`id`, `key1`, `key2`, `key3`, `key4`, `key5`, "\
            "`key6`, `key7`, `key8`, `key9`, `key10`)"

text_new = "replace INTO `texts` (`id`, `name`, `content`, `key1`, `key2`, `key3`, " \
           "`key4`, `key5`, `key6`, `key7`, `key8`, `key9`, `key10`, `key11`, `key12`, " \
           "`key13`, `key14`, `key15`, `key16`)"

file_list = ["data1.sql", "data2.sql", "data3.sql", "data4.sql"]

with open("data.sql", "r", encoding='utf-8-sig') as f:
    s = f.readline()
    i = 0
    index = 0
    while s:
        s = s.replace("INSERT or replace into datas ", data_new)
        s = s.replace("INSERT or replace into texts ", text_new)
        with open(file_list[index], "a", encoding="utf8") as p:
            p.write(s)
        i += 1
        if i >= 10000 and ";" in s:
            index += 1
            i = 0
        s = f.readline()