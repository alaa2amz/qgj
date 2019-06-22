#! /usr/bin/env python3

import xml.sax
import sys
import sqlite3
import groups
xmlfile = sys.argv[1]
dbfile = sys.argv[2]
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

def insert_ignore_select(table_name,value):
    insert_ignore_query_string = f'INSERT OR IGNORE INTO {table_name}({table_name}_value) VALUES (?)'
    select_query = f'SELECT {table_name}_id from {table_name} where {table_name}_value = ?'
    cur.execute(insert_ignore_query_string,(value,))
    result = cur.execute(select_query,(value,))
    id = result.fetchone()[0]
    return id

class KanjiDicHandler(xml.sax.ContentHandler):
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
        if name == 'rmgroup':
            self.q = f'insert into {name}  (literal_id)  values({self.tag_register_dict["literal"]})'
            cur.execute(self.q)
            self.tag_register_dict[name] = cur.lastrowid

        self.tag_content_dict[name] = ''
        self.tag_attr_dict[name] = attrs

    def endElement(self,name):




        if name in tables_names and name != 'rmgroup':
            self.fields = []
            self.values = []



            
            for field in table_fields_dict[name][1:]:
                if field.find('_id') != -1 and field[:-3] in self.tag_register_dict:
                    self.fields.append(field)
                    self.values.append(str(self.tag_register_dict[field[:-3]]))
                
                if field[:-3] in self.tag_attr_dict[name] and field[-3:] == '_id':
                    self.key = field[:-3]
                    self.id = insert_ignore_select(field[:-3],self.tag_attr_dict[name][self.key])
                    self.fields.append(field)
                    self.values.append(self.id)
                if field.find('_value') != -1:
                    self.fields.append(field)
                    self.values.append(str(self.tag_content_dict[name]))
               
                
                    
                
            # qm --> question mark
            self.qm_list = ['?' for x in range(len(self.values))]
            self.qm_string = ','.join(self.qm_list)
            self.fields_string = ','.join(self.fields)
            self.q = f'insert into {name}({self.fields_string}) values ({self.qm_string})'
            cur.execute(self.q,tuple(self.values))

            if name in ['rmgroup','literal','dic_ref','q_code']:
                self.tag_register_dict[name] = cur.lastrowid

            
            if len(self.tag_attr_dict[name]) > 1:
                for attribute in dict(self.tag_attr_dict[name]):
                    if attribute in ['m_page','m_vol']:
                        self.qq = f'insert into {attribute}({attribute}_value,{name}_id,literal_id) values (?,?,?)'
                        cur.execute(self.qq,(self.tag_attr_dict[name][attribute],self.tag_register_dict[name],self.tag_register_dict['literal']))
                    if attribute == 'skip_misclass':
                        self.id = insert_ignore_select('skip_misclass_type',self.tag_attr_dict[name][attribute])
                        self.qq = f'insert into {attribute}({attribute}_type_id,{name}_id,literal_id) values (?,?,?)'
                        cur.execute(self.qq,(self.id,self.tag_register_dict[name],self.tag_register_dict['literal']))
            self.popped_tag = self.tag_stack.pop()
            if self.popped_tag == 'literal':
                self.counter += 1
                print(self.counter,'-->',self.tag_content_dict[name])
            '''if self.counter > 1000:
                con.commit()
                con.close()
                exit()'''

    def characters(self,content):
        if content  not in [' ','\n']:
            self.tag = self.tag_stack[-1]
            self.tag_content_dict[self.tag] += content

    def endDocument(self):
        con.commit()
        con.close()
def parse(xmlfile=xmlfile,dbfile=dbfile):
    xml.sax.parse(xmlfile,KanjiDicHandler())
    


if __name__ == '__main__':
    parse()
