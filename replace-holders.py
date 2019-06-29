#! /usr/bin/env python3

place_holders ='''\
化 ⺅
刈 刂
込 辶
汁 氵
初 衤
尚 ⺌
買 罒
犯 犭
忙 忄
礼 礻
个 𠆢
老 ⺹
扎 扌
杰 灬
疔 疒
禹 禸
艾 ⺾
邦 ⻏
阡 ⻖
'''

import sys
import sqlite3
db_file = sys.argv[1]
con = sqlite3.connect(db_file)
cur = con.cursor()

def insert_ignore_select(table_name,value):
    insert_ignore_query_string = f'INSERT OR IGNORE INTO {table_name}({table_name}_value) VALUES (?)'
    select_query = f'SELECT {table_name}_id from {table_name} where {table_name}_value = ?'
    cur.execute(insert_ignore_query_string,(value,))
    result = cur.execute(select_query,(value,))
    id = result.fetchone()[0]
    return id

def replace_holders(place_holders=place_holders, db_file=db_file):
    place_holders = place_holders.splitlines()
    for line in place_holders:
        list = line.split()
        id = insert_ignore_select('parts',list[0])
        q = 'update  parts set parts_value = ? where parts_id= ?'
        cur.execute(q,(list[1],id))
        print(id,list,sep='-->')
    con.commit()
    con.close()
    #print('done')

if __name__ == '__main__':
    replace_holders()
