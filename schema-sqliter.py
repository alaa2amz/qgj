#! /usr/bin/env python3
'''module to convert alar's schema text files to sqlite file db tables

if to be ran as script or executable the arguments to be as follows
1st ---> schema text file
2nd ---> the name of sqlite file to be created
todo: if 2nd argument not suppliy take it as the 1st with replacing extention

alaa amz
Sun Jun 23 10:25:37 EET 2019
Pick another fortune cookie.
'''
import sqlite3
import sys

db_file = sqlite3.connect(sys.argv[2])
schema_file = open(sys.argv[1])
def main(schema_file = schema_file,db_file=db_file):
    con = sqlite3.connect(sys.argv[2])
    cur = con.cursor()    
    table_lines = schema_file.read().splitlines()
    #clearing empty lines
    table_lines = [ x for x in table_lines if x != '' ]
    tables_names = [ x[0] for x in [line.split() for line in table_lines] ]

    for table_line in table_lines:
        #foreign keys list and normal key list
        fk = []
        nk = []
        fields_words = table_line.strip().split()

        for field_word in fields_words[1:]:
            if any(i in tables_names for i in [field_word,field_word.split('__')[-1]]) :
                fk.append(field_word)            
            else:
                nk.append(field_word)
        declared_fk = [f'{x}_id INTEGER' for x in fk]
        declared_nk = [f'{x} VARCHAR' for x in nk]
        constraint_fk = [f'FOREIGN KEY ({x}_id) REFERENCES {x.split("__")[-1]} ({x.split("__")[-1]}_id)' for x in fk]
        total = declared_fk + declared_nk + constraint_fk
        total_string = ','.join(total)
        if len(total_string) > 1:
            total_string = ',' + total_string
        else:
            total_string = 'UNIQUE'
        query_string = 'CREATE TABLE {0} ({0}_id INTEGER PRIMARY KEY, {0}_value VARCHAR {1})'.format(fields_words[0], total_string)
        #print(query_string)
        cur.execute(query_string)

    #print('done')    
    con.commit()
    con.close()

if __name__ == '__main__':
    print('creating schema')
    main()
    print('done')
