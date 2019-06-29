#! /usr/bin/env python3

import sys
import sqlite3
db_name = 'kd3.db'
con = sqlite3.connect(db_name)
cur = con.cursor()

def get_literal_meaning(literal,sep='|'):
    q = 'select meaning_value from meaning,literal where literal.literal_id = meaning.literal_id and meaning.m_lang_id is null and literal_value = ?'
    result = cur.execute(q,(literal[0],))
    result_list = [literal[0]]+[x[0] for x in result]
    result_string = sep.join(result_list)
    return result_string

def get_parts_catalog():
    q1 = 'select parts.parts_value from parts'
    result = cur.execute(q1)
    parts_list = [x[0] for x in result]
    catalog_list = [get_literal_meaning(x) for x in parts_list]
    return catalog_list

if __name__ == '__main__':
    for x in get_parts_catalog():
        print(x)
