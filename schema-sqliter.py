#! /usr/bin/env python3

import sqlite3
import sys



con = sqlite3.connect(sys.argv[2])
cur = con.cursor()

schema_file = open(sys.argv[1])
table_lines = schema_file.read().splitlines()
table_lines = [ x for x in table_lines if x != '' ]
print(table_lines)
input()
tables_names = []
#tables_names = [ x[0] for x in [line.split() for line in table_lines] ]

for line in table_lines:
    fields = line.split()
    tables_names.append(fields[0])
    
print('llll',tables_names)

for table_line in table_lines:
    fk = []
    nk = []
    fields_words = table_line.strip().split()
    for field_word in fields_words[1:]:
        if field_word in tables_names:
            fk.append(field_word)            
        else:
            nk.append(field_word)
    declared_fk = [f'{x}_id INTEGER' for x in fk]
    declared_nk = [f'{x} VARCHAR' for x in nk]  ####
    constraint_fk = [f'FOREIGN KEY ({x}_id) REFERENCES {x} ({x}_id)' for x in fk]
    total = declared_fk + declared_nk + constraint_fk
    total_string = ','.join(total)
    if len(total_string) > 1:
        total_string = ',' + total_string
    else:
        total_string = 'UNIQUE'
    query_string = 'CREATE TABLE {0} ({0}_id INTEGER PRIMARY KEY, {0}_value VARCHAR {1})'.format(fields_words[0], total_string)
    print(query_string)
    cur.execute(query_string)

con.commit()
con.close()
