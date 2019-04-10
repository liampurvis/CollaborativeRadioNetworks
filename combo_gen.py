import Player
from core import env_core
import matplotlib.pyplot as plt
import numpy as np
import re
import calendar;
import time;
import sys
import itertools



path = "pipes/"

pl_type = ["R","C","U","Ud","T"]
single_type = "0,0,0,0,0,0,0"
arr_type = ["0,0,0,0,0,0,1",
            "0,1,1,1,1,1,1",
            "0,0,0,1,1,1"]

s_not_enough_ch = 's,10,5,5,1500\n'
s_enough_ch = 's,10,7,3,1500\n'
ns = 'ns,10,5,5,5000\n'

single_benchmark = itertools.combinations(pl_type,1)

for solo in single_benchmark:
	so = solo[0]
	csv = "0,0,0,0,0,0,0".replace(",","")
	filename = "s_%s_%s_10_5_5.txt"%(str(so), csv)
	with open(path+filename, 'w') as the_file:
	    the_file.write('1,7\n')
	    the_file.write('fixed\n')
	    the_file.write('%s\n'%so)
	    the_file.write('%s\n'%single_type)
	    the_file.write(s_not_enough_ch)
	    the_file.write('30\n')
	    the_file.write('1\n')
	    the_file.close()

double_benchmark = itertools.combinations(pl_type,2)

for duo in double_benchmark:
	d1 = duo[0]
	d2 = duo[1]
	for i in range(len(arr_type)):
		csv = arr_type[i].replace(",","")
		filename = "s_%s_%s_10_5_5.txt"%(str(d1)+str(d2), csv)
		with open(path+filename, 'w') as the_file:
		    the_file.write('%d,%d\n'%(2,len(csv)))
		    the_file.write('fixed\n')
		    the_file.write('%s,%s\n'%(d1,d2))
		    the_file.write('%s\n'%arr_type[i])
		    the_file.write(s_not_enough_ch)
		    the_file.write('30\n')
		    the_file.write('1\n')
		    the_file.close()

	for i in range(len(arr_type)):
		csv = arr_type[i].replace(",","")
		filename = "s_%s_%s_10_7_3.txt"%(str(d1)+str(d2), csv)
		with open(path+filename, 'w') as the_file:
		    the_file.write('%d,%d\n'%(2,len(csv)))
		    the_file.write('fixed\n')
		    the_file.write('%s,%s\n'%(d1,d2))
		    the_file.write('%s\n'%arr_type[i])
		    the_file.write(s_enough_ch)
		    the_file.write('30\n')
		    the_file.write('1\n')
		    the_file.close()

	for i in range(len(arr_type)):
		csv = arr_type[i].replace(",","")
		filename = "ns_%s_%s_10_5_5.txt"%(str(d1)+str(d2), csv)
		with open(path+filename, 'w') as the_file:
		    the_file.write('%d,%d\n'%(2,len(csv)))
		    the_file.write('fixed\n')
		    the_file.write('%s,%s\n'%(d1,d2))
		    the_file.write('%s\n'%arr_type[i])
		    the_file.write(ns)
		    the_file.write('30\n')
		    the_file.write('1\n')
		    the_file.close()


