#! /usr/bin/env python3

import sys
import sqlite3
db_name = 'kd4.db'
con = sqlite3.connect(db_name)
cur = con.cursor()

def _regexp(pattern,input_string):
    import re
    pa = result = re.compile(pattern)
    return pa.search(input_string) is not None
    
con.create_function('REGEXP',2,_regexp)
def wamk(args=sys.argv):
    '''where are my kanjies'''
    # q = 'select literal.literal_value from kmlp,literal,k_parts where kmlp.pis = k_parts.parts_id and k_parts.literal_id = literal.literal_id and kmlp.meaning REGEXP ?'
    q2 = '''select literal.* 
    from literal,k_parts
    where literal.literal_id = k_parts.literal_id 
    and k_parts.parts_id in
    (select parts.parts_id as pid 
    from literal, meaning,parts 
    where literal.literal_value = parts.parts_value 
    and meaning.literal_id = literal.literal_id 
    and meaning.m_lang_id = 1
    and meaning.meaning_value REGEXP ?)
    '''
    q='''
    select literal_id,literal_value from kanji_by_part_meaning where meaning_value REGEXP ?

    '''
    print(q)
    kanji_set = set()
    kanji_list = []
    for arg in args:
        
        arg=r'\b'+arg+r'\b'
        ro=cur.execute(q,(arg,))
        ro=set(ro)
                
        if len(ro) == 0 or len(kanji_set) == 0:
            kanji_set = kanji_set.union(ro)
        else:
            kanji_set = kanji_set.intersection(ro)
    kanji_list = [x for x in kanji_set]
        #print('uuu',kanji_list)
    return kanji_list

if __name__ == '__main__':
    import dbgector
    d=wamk()
    #e=[dbgector.dbgect('literal_id',x[0]) for x in d]
    #f=sorted(e,key= lambda x:int(x.stroke_count[1][1]))
    #[print(s) for s in f]
    #from datetime import datetime as dt
    #log_file = open('qgj-log.txt','a')
    #log_file.write(dt.utcnow().isoformat()+' ')
    #log_file.write(' '.join(sys.argv)+'\n')
    #[print(s,file=log_file) for s in f]
    #log_file.flush()
    print(d)
