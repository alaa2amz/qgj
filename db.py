#
#! /usr/bin/env python3
import sqlite3
import logging

class ExEntry():
    def __init__(self,results,field_id):
                    self.__dict__.update(results)
                    self.__field_id = field_id

    def __repr__(self):
        return repr(self.__dict__[self.__field_id[:-3]][1])
        
    def __str__(self):
        return self.__repr__()
    
    def headers(self):
        self.__headers={}
        self.__fields=[]
        for x,y in self.__dict__.items():
             if x[0] !='_': self.__headers[x]=y[0]
        return self.__headers
    
    def get_predicated_column(self,table,column,
                    predicate_column='',
                    predicate_values='',
                    inverse=False):

        #initializing predicated column array
        self.__column_list = []
        
        #getting column indexes
        import logging
        logging.critical(self.__dict__[table][0])
        self.__header_raw = self.__dict__[table][0]
        
        self.__column_index = self.__header_raw.index(column)
        if predicate_column != '':
            self.__predicate_column_index = self.__header_raw.index(
            predicate_column)

        #get table and strip it's header
        self.__table = self.__dict__[table][1:]
        
        for row in self.__table:
            if predicate_column !='' and\
            row[self.__predicate_column_index] in predicate_values:
                self.__valid_value = row[self.__column_index]
                self.__column_list.append(self.__valid_value)
            elif predicate_column == '':
                self.__column_list.append(row[self.__column_index])
        
        return self.__column_list

    def present(self,template):
        self.__entries=[]
        self.__outlists=[]
        for x in template.splitlines():
            self.__args=[]
            for i,y in enumerate(x.split()):
                self.__args.append(y.split(',') if i==3 else y)
            logging.critical(self.__args)
            self.__entries.append(self.__args)
        for entry in self.__entries:
            self.__outlists.append(self.get_predicated_column(*entry))
        return self.__outlists
        

        

    
        

#----------------------------------------------------------------------#
    
class Db():

    def __regexp(pattern,input_string):
        import re
        pattern = re.compile(pattern)
        return pattern.search(input_string) is not None


    def __init__(self,dbfile):
        self.dbfile = dbfile
        self.con = sqlite3.connect(dbfile)
        self.con.create_function('REGEXP',2,self.__regexp)
        self.cur = self.con.cursor()

    def db(self,dbfile):
        self.dbfile = dbfile
        self.con = sqlite3.connect(dbfile)
        self.cur = self.con.cursor()

    def concur(self):
        return (self.con,self.cur)

    def tables(self):
        #creating list of all tables
        self.__tables_names = self.cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
        self.__tables_names = [ table[1] for table in self.__tables_names ]
        return self.__tables_names

    def fields(self):
        #getting fields of all tables
        self.__table_fields_dict = {}
        for table_name in self.tables():
            self.__fields = self.cur.execute(f'PRAGMA table_info({table_name})')
            self.__fields_list = [ x[1] for x in self.__fields ]
            self.__table_fields_dict[table_name] = self.__fields_list
        del self.__fields,self.__fields_list
        return self.__table_fields_dict

    def dbject(self,field_id,value):

        self.__results = {}
        self.__table_fields_dict = self.fields()
        self.__tables = self.tables()
        for _table_name in self.__tables:

            if field_id in self.__table_fields_dict[_table_name]:
                self.__headrs_list =  self.__table_fields_dict[_table_name][:]
                self.__select_list =  [_table_name+'.*']
                self.__from_list   =  [_table_name]
                self.__where_list  =  [_table_name+'.'+field_id+'=?']

                for _field in self.__table_fields_dict[_table_name]:

                    if _field[-3:]=='_id' and _field not in [field_id,_table_name+'_id'] and _field[:-3] in self.__tables:
                        self.__headrs_list.append(_field[:-3] + '_value')
                        self.__select_list.append(_field[:-3] + '_value')
                        self.__from_list.append(_field[:-3])
                        self.__where_list.append(_table_name + '.' + _field + '=' + _field[:-3] + '.' + _field)

                self.__query = f'select {",".join(self.__select_list)} from {",".join(self.__from_list)} where {" and ".join(self.__where_list)}'



                self.__query_set = self.cur.execute(self.__query,(value,))
                self.__results[_table_name] = [tuple(self.__headrs_list)]+self.__query_set.fetchall()
                #ch = type('Character',(object,),results)
                self.__exentry=ExEntry(self.__results,field_id)
        return self.__exentry

    
    
if __name__ == '__main__':
    import sys
    from pprint import pprint
    db_file = sys.argv[1]
    field_id = sys.argv[2]
    value = sys.argv[3]
    db1 = Db(db_file)
    my_dbject = db1.dbject(field_id,value)
    pprint(my_dbject.headers())
    print(my_dbject)
    t='''\
literal literal_value
meaning meaning_value m_lang_value en
reading reading_value r_type_value ja_on,ja_kun
stroke_count stroke_count_value
rad_value rad_value_value
grade grade_value
'''
    print('----->>>>>',my_dbject.present(t))
