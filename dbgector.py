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
            from_list=[table_name]
            where_dict[field_id]=value#####
            for field in table_fields_dict[table_name]:
                if field[-3:]=='_id' and field != field_id\
                and field[:-3] in tables_names:
                    from_list.append(field[:-3])
                    where_dict[table_name+'.'+field]=field[:-3]+'.'+field###
            where_list = [
            q = f'select * from {"."join(from_list)} where {} = ?'
            print(table_name,field_id,value,'7777')
            r=cur.execute(q,(value,))
            results[table_name]=[tuple(table_fields_dict[table_name])]+r.fetchall()
    return results

if __name__ == '__main__':
    t=dbgect('literal_id',16)
    import pprint
    pprint.pprint(t)
