#!/usr/bin/python

# 
# Pomozne funkcije 
# 

import os
import sys
import time
import prop

# Sestavi CNF formulo iz DIMACS formata 
clean = lambda v: prop.Not("v"+v[1:]) if v[0] == '-' else "v"+v

def parse_output(fname = 'new.cnf'):
	L = open(fname).read().split('\n')
	fmt = L[0]
	return prop.And([prop.Or([clean(c) for c in clause.split()[:-1]]) for clause in L[1:-1]])

# Vzame sudoku, kjer so vnosi v vrstici loceni s presledki; vrstice locene z '\n' (novo vrstico); prazna mesta oznacena z 0
# Vrne sudoku primeren za nas (Borjev :-) sudoku solver 
replace = lambda L: [None if x == '0' else x for x in L]
def get_sudoku(fname):
	L = open(fname).read().split('\n')
	S = [replace(l.split()) for l in L]
	return S
