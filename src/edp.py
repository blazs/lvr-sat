# 
# Klicemo rahlo spremenjen zunanji C++ program, ki sta ga objavila B. Konev in A. Lisista. Program
# vrne SAT instanco v CNF, ki ustreza Erdosevemu problemu diskrepance za dane parametre. Formulo
# pretvorimo v primerno obliko in jo nahranimo nasemu solverju. 
# 

import prop
import math
import re
import itertools
import sat
import os

def clean(v):
	if v[0] == '-':
		return prop.Not("v"+v[1:])
	else:
		return "v"+v

def edp2sat(fname):
	L = open(fname).read().split('\n')
	fmt = L[0]
	return prop.And([prop.Or([clean(c) for c in clause.split()[:-1]]) for clause in L[1:-1]])
	#for clause in L[1:]:
	#	t = ["v"+str(c.replace("-", "m")) for c in clause.split()]
	#	phi.append(prop.Or(t))
	

if __name__ == '__main__':
	length = 2
	discrepancy = 1
	bits = 5
	cmd = 'sat14.exe %d %d %d > out.cnf' % (length, discrepancy, bits)
	print cmd
	os.system(cmd)
	os.system('grep -v "^c" out.cnf | grep -v "^$" > new.cnf')
	phi = edp2sat('new.cnf')
	print phi
	print sat.sat(phi)
