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

def dqgj(argv=sys.argv):
    all_srgs_string = ' '.join(argv[1:])
    pipe_separated_list = all_srgs_string.split('-')
    words_list = [ x.split() for x in pipe_separated_list]
    print(words_list)
    k_list = []
    [ k_list.append(qgj.wamk(args=x)) for x in words_list]
    print(k_list)
    p_list = []
    p_list= [list(x) for x in k_list]
    print(p_list)
    p_list= ['|'.join(x[1]) for x  in [y for y in p_list]]
    print(p_list)


if __name__ == '__main__':
    dqgj()
