#! /usr/bin/env python3

import sys
import sqlite3
db_file = sys.argv[1]
con = sqlite3.connect(db_file)
cur = con.cursor()

parts = '''\
ノ KATAKANA LETTER NO
ヨ KATAKANA LETTER YO
｜ FULLWIDTH VERTICAL LINE
ハ KATAKANA LETTER HA
⺅ CJK RADICAL PERSON
⻖ CJK RADICAL MOUND TWO
⺾ CJK RADICAL GRASS ONE
⺌ CJK RADICAL SMALL ONE
⺹ CJK RADICAL OLD
⻏ CJK RADICAL CITY
マ KATAKANA LETTER MA
ユ KATAKANA LETTER YU
𠆢 umbrella hat
辶 walk walking cart change 
'''

def insert_ignore_select(table_name,value):
    insert_ignore_query_string = f'INSERT OR IGNORE INTO {table_name}({table_name}_value) VALUES (?)'
    select_query = f'SELECT {table_name}_id from {table_name} where {table_name}_value = ?'
    cur.execute(insert_ignore_query_string,(value,))
    result = cur.execute(select_query,(value,))
    id = result.fetchone()[0]
    return id

def insert_12_parts_literals(parts=parts,db_file=db_file):
    

    parts=parts.lower()
    parts_lines=parts.splitlines()

    for line in parts_lines:
        part_list = line.split(maxsplit=1)
        id = insert_ignore_select('literal',part_list[0])
        q = 'insert into meaning (literal_id,meaning_value,rmgroup_id,m_lang_id) values (?,?,?,?)'
        cur.execute(q,(id,part_list[-1],1,1))
        print(id,part_list)
    con.commit()
    con.close()
    print('done')


if __name__ == '__main__':
    insert_12_parts_literals()
