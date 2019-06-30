#! /usr/bin/env python3

import sys
import sqlite3
dbfile = 'kd3.db'
con = sqlite3.connect(dbfile)
cur = con.cursor()

#creating list of all tables
tables_names = cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
tables_names = [ table[1] for table in tables_names ]

#getting fields of all tables
table_fields_dict = {}
for table_name in tables_names:
    fields = cur.execute(f'PRAGMA table_info({table_name})')
    fields_list = [ x[1] for x in fields ]
    table_fields_dict[table_name] = fields_list



def dbgect(field_id,value):
    results = {}
    for table_name in tables_names:
        if field_id in table_fields_dict[table_name]:
            q = f'select * from {table_name} where {field_id} = ?'
            print(table_name,field_id,value,'7777')
            r=cur.execute(q,(value,))
            results[table_name]=[tuple(table_fields_dict[table_name])]+r.fetchall()
    return results

if __name__ == '__main__':
    t=dbgect('literal_id',16)
    import pprint
    pprint.pprint(t)
