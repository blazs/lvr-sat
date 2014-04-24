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

clean = lambda v: prop.Not("v"+v[1:]) if v[0] == '-' else "v"+v

def edp2sat(fname):
	L = open(fname).read().split('\n')
	fmt = L[0]
	return prop.And([prop.Or([clean(c) for c in clause.split()[:-1]]) for clause in L[1:-1]])

if __name__ == '__main__':
	length = 4
	discrepancy = 1
	bits = 5
	cmd = 'sat14 %d %d %d > out.cnf' % (length, discrepancy, bits)
	print "Compiling sat14.cc..."
	os.system('g++ sat14.cc -o sat14')
	print "Running sat14.cc..."
	os.system(cmd)
	print "Cleaning up the output..."
	os.system('grep -v "^c" out.cnf | grep -v "^$" > new.cnf')
	phi = edp2sat('new.cnf')
	print "Running the SAT solver..."
	# print phi
	print sat.sat(phi)
