#! /usr/bin/env python3


#split by pipe
#split by space
#get qgj results
#query keb
#debjector
import qgj
#import dbgect
import debjector
import sys
import sqlite3
import re

con = sqlite3.connect('jm4.db')
cur = con.cursor

def _regexp(pattern,input_string):
    import re
    pa = result = re.compile(pattern)
    return pa.search(input_string) is not None
con.create_function('REGEXP',2,_regexp)

def dqgj(argv=sys.argv):
    all_srgs_string = ' '.join(argv[1:])
    pipe_separated_list = all_srgs_string.split('-')
    words_list = [ x.split() for x in pipe_separated_list]
    print(words_list)
    k_list = []
    [ k_list.append(qgj.wamk(args=x)) for x in words_list]
    print(k_list)
    p_list = []
    print(p_list)
    #p_list= ['|'.join(x[1]) for tupley  in p_list for x in tupley ]
    for li in k_list:
        g=[]
        for tu in li:
            g.append(tu[1])
        p_list.append('['+"".join(g)+']')
        ps=''.join(p_list)
    print(ps)
    q = 'select * from keb where keb_value REGEXP ?'
    r_set = con.execute(q,('^'+ps+'$',))
    return list(r_set)

if __name__ == '__main__':
    r = dqgj()
    print(r)
    [print(debjector.dbgect('ent_seq_id',x[2])) for x in r]
