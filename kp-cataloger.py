#! /usr/bin/env python3

import sys
import sqlite3
import dbgector
dbfile = 'kd4.db'
con = sqlite3.connect(dbfile)
cur = con.cursor()


q1 = 'select literal.literal_id,literal.literal_value from literal,parts where parts.parts_value = literal.literal_value'

def get_kanji_parts_list():
    result = cur.execute(q1)
    kanji_parts_list = list(result)
    #print(kanji_parts_list)
    return kanji_parts_list

def get_cataloge():
    literal_list = get_kanji_parts_list()
    objects_list = [dbgector.dbgect('literal_id',x[0]) for x in literal_list]
    return  objects_list

if __name__ == '__main__':
    s= get_cataloge()
    [print(x) for x in s]
