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

counter =0

def dbgect(field_id,value):
    global counter
    results = {}
    for table_name in tables_names:
        
        
        if field_id in table_fields_dict[table_name]:
            
            headrs_list=table_fields_dict[table_name][:]
            select_list=[table_name+'.*']
            from_list=[table_name]
            where_list=[table_name+'.'+field_id+'=?']
            for field in table_fields_dict[table_name]:
                if field[-3:]=='_id' and field not in [field_id,table_name+'_id'] and field[:-3] in tables_names:
                    #print('^^^^',field)
                    headrs_list.append(field[:-3]+'_value')
                    select_list.append(field[:-3]+'_value')
                    from_list.append(field[:-3])
                    where_list.append(table_name+'.'+field+'='+field[:-3]+'.'+field)
            del field
            #print('--++---',field)
            q = f'select {",".join(select_list)} from {",".join(from_list)} where {" and ".join(where_list)}'
            #print(q)   
            #print('jjjjjjjj',headrs_list)

            #print('SL',select_list)
            #print('WL',where_list)
            r=cur.execute(q,(value,))
            counter +=1
       
            results[table_name]=[tuple(headrs_list)]+r.fetchall()
            headrs_list =[0]
        #ch = type('Character',(object,),results)
        class Ch():
            def __init__(self,results):
                self.__dict__.update(results)
            def __repr__(self):
                return '|-> %s -- %s -- %s' % (
                self.literal[1][1],
                '|'.join(str(x[1]) for x in self.reading[1:] if 'ja_' in x[-1]),
                '|'.join(str(x[1]) for x in self.meaning[1:] if x[-1] in ['en','pt']),
                )
        ch=Ch(results)
    del table_name
    print(counter)
    return ch

if __name__ == '__main__':
    import random
    t=[dbgect('literal_id',random.randrange(13109)) for x in range(5)]
    
    [print(x) for x in t]
    print(counter)
