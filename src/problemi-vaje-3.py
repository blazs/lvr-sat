#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Adapted Janos' code. :-) 
#

import prop
import math
import re
import sat

# Združljivost za Python 2 in Python 3
try:
	basestring
except NameError:
	basestring = str
	
def iff(p, q):
	"""Vrne logièno ekvivalenco izrazov p in q kot konjunkcijo dveh implikacij."""
	return prop.And(prop.Implies(p, q), prop.Implies(q, p))

####
# Takes an instance of graph k-coloring problem (G,k) and outputs corresponsing Boolean formula Phi such
# that Phi is satisfiable if and only if G is k-colorable. 
####
def graph_coloring(G, k):
	# G[0] naj bo stevilo povezav 
	# G[1] naj bo seznam parov vozlics, a.k.a, seznan pobexzav
	# k > 0 je stevilo barv 
	assert k>0, "Premalo barv"
	
	l = []
	
	# vsako vozlisce ima vsaj eno barvo 
	l.append(prop.And([prop.Or(["v%dc%d" % (i, j) for j in range(k)]) for i in range(G[0])]))
	# pari krajisc so razlicnih barv 
	for (u, v) in G[1]:
		l.append(prop.And([prop.And([prop.Not(prop.And(["v"+str(u)+"c"+str(c), "v"+str(v)+"c"+str(c)])) for c in range(k)])]))
	# vsako vozlisce je kvecjemu ene barve 
	for v in range(G[0]):
		for i in range(k):
			for j in range(i+1, k):
				l.append(prop.Not(prop.And(["v"+str(v)+"c"+str(i), "v"+str(v)+"c"+str(j)])))
	phi = prop.And(l)
	print phi
	return phi

if __name__ == '__main__':
	V = 3
	E = [(0,1), (1,2)]
	G = (V, E)
	phi = graph_coloring(G, 1)
	print prop.sat3(phi)
	## 14 Mar 2014 ##
	phi = prop.cnf(phi)
	sat.brute_force(phi)
	d = {}
	
