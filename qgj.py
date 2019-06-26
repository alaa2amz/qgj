#! /usr/bin/env python3

import sys
import sqlite3
db_name = 'kd3.db'
con = sqlite3.connect(db_name)
cur = con.cursor()
def wamk(args=sys.argv):
    '''where are my kanjies'''
    q = 'select literal.literal_value from kmlp,literal,k_parts where kmlp.pis = k_parts.parts_id and k_parts.literal_id = literal.literal_id and kmlp.meaning = ?'
    kanji_set = set()
    for arg in args:
        ro=cur.execute(q,(arg,))
        ro=set(ro)
        if len(ro) == 0 or len(kanji_set) == 0:
            kanji_set = kanji_set.union(ro)
        else:
            kanji_set = kanji_set.intersection(ro)
    print(kanji_set)

if __name__ == '__main__':
    wamk()
    
