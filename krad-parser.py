#! /usr/bin/env python3
'''module for parsing kanji krad file and populating its contents into sqlite db file

1st argument krad file
2nd argument sqlite db file

alaa amz
Sun Jun 23 13:27:02 EET 2019
Truth has no special time of its own.  Its hour is now -- always.
		-- Albert Schweitzer

'''

import sys
import sqlite3

def insert_ignore_select(table_name,value):
    '''insert value or ignore if existed and select its id for a lookup single collummed table

    parametrs:-
    table_name: the name of the table
    valu: the value to insert and lookup
    note:by default the value is inserted as for {table_name}.{table_name}_value
    todo: adding fields and corresponding values tuples
    '''
    
    insert_ignore_query_string = f'INSERT OR IGNORE INTO {table_name}({table_name}_value) VALUES (?)'
    select_query = f'SELECT {table_name}_id from {table_name} where {table_name}_value = ?'
    cur.execute(insert_ignore_query_string,(value,))
    result = cur.execute(select_query,(value,))
    id = result.fetchone()[0]
    return id



kradfile = sys.argv[1]
db_file = sys.argv[2]
con = sqlite3.connect(db_file)
cur = con.cursor()
def parse(kradfile=kradfile,db_file=db_file):
    file = open(kradfile,'r')
    line = file.readline()
    while line != '':
        if line[0] == '#':
            line = file.readline()
        else:
            literal = line[0]
            parts = line[4:].strip().split()
            literal_id = insert_ignore_select('literal',literal)
            print(literal)
            
            for part in parts:
                part_id = insert_ignore_select('parts',part)
                q = 'insert into k_parts (literal_id,parts_id) values (?,?)'
                cur.execute(q,(literal_id,part_id))
                line= file.readline()
    con.commit()
    con.close()
    print('done')

if __name__ == '__main__':
    parse()
