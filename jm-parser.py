#! /usr/bin/env python3
'''parse JMdict japanese dictionary xml file to sqlite db file

if ran fom shell as script or executable
first argument --> input JMdict xml file path
second argument --> sqlite db file for populating the data

alaa amz 2019-06-22
'''

import xml.sax
import sys
import sqlite3
import groups

#input and output files
xmlfile = sys.argv[1]
dbfile = sys.argv[2]

#creating db connection
con = sqlite3.connect(dbfile)
cur = con.cursor()

#getting table names and fields for each
tables_names = cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
tables_names = [ table[1] for table in tables_names ]
table_fields_dict = {}
for table_name in tables_names:
    fields = cur.execute(f'PRAGMA table_info({table_name})')
    fields_list = [ x[1] for x in fields ]
    table_fields_dict[table_name] = fields_list

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

class JmdictHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.tag_stack = []
        self.tag_register_dict = {}
        self.tag_attr_dict = {}
        self.tag_content_dict = {}
        self.counter = 0

    def startDocument(self):
        print('start')

    def startElement(self,name,attrs):
        
        self.tag_stack.append(name)

        if name == 'sense':
            self.q = f'insert into {name}  (ent_seq_id)  values({self.tag_register_dict["ent_seq"]})'
            cur.execute(self.q)
            self.tag_register_dict[name] = cur.lastrowid

        self.tag_content_dict[name] = ''
        self.tag_attr_dict[name] = attrs

    def endElement(self,name):
        if name in tables_names and name != 'sense':
            self.fields = []
            self.values = []
            print('name: ',name,' attrs: ',dict(self.tag_attr_dict[name]),' content: ',self.tag_content_dict[name])
            #input('---')
            
            for field in table_fields_dict[name][1:]:
                if field.find('_id') != -1 and field[:-3] in self.tag_register_dict:
                    self.fields.append(field)
                    self.values.append(str(self.tag_register_dict[field[:-3]]))
                ###
                print('fffff---->',self.tag_register_dict)
                print('rrrrr----',field,dict(self.tag_attr_dict[name]))
                #input('ll')
                if field[:-3] in self.tag_attr_dict[name] or 'xml:'+field[:-3] in self.tag_attr_dict[name]:
                    if field.find('lang') != -1  :
                        self.key = 'xml:'+field[:-3]
                    else:
                        self.key = field[:-3]
                    print('rrrrr----',field[:-3],self.tag_attr_dict[name][self.key])
                    self.id = insert_ignore_select(field[:-3],self.tag_attr_dict[name][self.key])
                    print(self.id)
                    #input()
                    self.fields.append(field)
                    self.values.append(self.id)
                if field.find('_value') != -1 and( name not in groups.value_as_lookup):
                    #input('vvvv')
                    self.fields.append(field)
                    self.values.append(str(self.tag_content_dict[name]))
                if field.find('inf_id') != -1 and( name in groups.value_as_lookup):
                    self.infid = insert_ignore_select('inf',str(self.tag_content_dict[name]))
                    self.fields.append(field)
                    self.values.append(self.infid)
                if field.find('pri_id') != -1 and( name in groups.value_as_lookup):
                    self.infid = insert_ignore_select('pri',str(self.tag_content_dict[name]))
                    self.fields.append(field)
                    self.values.append(self.infid)
                
                    
                

            self.qm_list = ['?' for x in range(len(self.values))]
            self.qm_string = ','.join(self.qm_list)
            self.fields_string = ','.join(self.fields)
            #self.values_string = ','.join(self.values)
            
            self.q = f'insert into {name}({self.fields_string}) values ({self.qm_string})'
            ###
            print('qqq',self.q,self.tag_content_dict,self.values)
            #input()
            cur.execute(self.q,tuple(self.values))
            if name in ['sense','ent_seq','keb','reb']:
                self.tag_register_dict[name] = cur.lastrowid
            self.popped_tag = self.tag_stack.pop()
            if self.popped_tag == 'ent_seq':
                self.counter += 1
                print (self.counter,'--->',self.tag_content_dict[self.popped_tag])
            if self.counter > 1000:
                con.commit()
                con.close()
                exit()

    def characters(self,content):
        if content  not in [' ','\n']:
            self.tag = self.tag_stack[-1]
            self.tag_content_dict[self.tag] += content

    def endDocument(self):
        con.commit()
        con.close()
def parse(xmlfile=xmlfile,dbfile=dbfile):
    xml.sax.parse(xmlfile,JmdictHandler())
    


if __name__ == '__main__':
    parse()
