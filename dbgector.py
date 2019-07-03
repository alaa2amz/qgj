#! /usr/bin/env python3

import sys
import sqlite3
dbfile = 'kd4.db'
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
            headrs_list=table_fields_dict[table_name]
            select_list=[table_name+'.*']
            from_list=[table_name]
            where_list=[table_name+'.'+field_id+'=?']
            for field in table_fields_dict[table_name]:
                if field[-3:]=='_id' and field not in [field_id,table_name+'_id'] and field[:-3] in tables_names:
                    headrs_list.append(field[:-3]+'_value')
                    select_list.append(field[:-3]+'_value')
                    from_list.append(field[:-3])
                    where_list.append(table_name+'.'+field+'='+field[:-3]+'.'+field)
            
            q = f'select {",".join(select_list)} from {",".join(from_list)} where {" and ".join(where_list)}'
            
            
            r=cur.execute(q,(value,))
            results[table_name]=[tuple(headrs_list)]+r.fetchall()
            #ch = type('Character',(object,),results)
            class Ch():
                def __init__(self,results):
                    self.__dict__.update(results)
                def __repr__(self):
                    return '|-> %s -- %s -- %s' % (
                    self.literal[1][1],
                    '|'.join(str(x[1]) for x in self.reading[1:] if 'ja_' in x[-1]),
                    '|'.join(str(x[1]) for x in self.meaning[1:] if x[-1]=='en'),
                    )
            ch=Ch(results)
    return ch

if __name__ == '__main__':
    import random
    t=[dbgect('literal_id',random.randrange(13109)) for x in range(5)]
    
    [print(x) for x in t]
