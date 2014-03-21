#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Adapted Janos' code. :-) 
#

import prop
import math
import re
import itertools

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
	
#TODO: popravi!
def hadamard(n):
	#hadamardove matrike obstajajo le za sodi n
	assert n%2 == 0
	if n%2 == 1:
		return prop.Fls()
	l = []
	xorList = []
	# gremo po vrsticah
	for i in range(n):
		for j in range(i+1, n):
			#pogledamo vrstico i,j in njun xor
			#vrstica1 = prop.And(["v%ds%d" % (i,k) for k in range(n)])
			#vrstica2 = prop.And(["v%ds%d" % (j,k) for k in range(n)])
			#xor = prop.Not(Equiv(vrstica1, vrstica2))
			#xorList[i] = prop.Not(Equiv(["v%ds%d" % (i,
			for elem in range(n-1):
				xorList.append(prop.Not(prop.Or([prop.And(["v%ds%d" % (i, elem), "v%ds%d" % (j, elem)]), prop.And([prop.Not("v%ds%d" % (i,elem)), prop.Not("v%ds%d" % (j, elem))])])))
			l.append(prop.And(xorList))
			#njun xor mora imeti n/2 enic in n/2 minus enic
			#generiramo vse mozne kombinacije elementov znotraj vrstice
			a = list(itertools.combinations(range(n), n/2))
			#preverimo, da xor ima n/2 enic => vrstica1 in vrstica2 se bosta razlikovali za n/2 elementov
			ORi = []
			#TODO: popravi spremenljivke od xor....
			
			stavek = []
			stavek2 = []
			for o in range(len(a)):
				#print xorList[a[o][0]]
				stavek.append(prop.And([xorList[a[o][p]] for p in range(len(a[o])-1)]))
				for u in range(n-1):
					if u not in a[o]:
						stavek2.append(prop.And(prop.Not(xorList[u])))
				#stavek2.append(prop.And([prop.Not(xorList[u]) for u in range(n-1) not in a[o]]))
				#ORi.append(prop.Or([stavek, stavek2]))
				#ORi.append(prop.Or([stavek2, stavek]))
				ORi.append(prop.Or([stavek[0], stavek2[0]]))
				#print stavek2
				#print stavek
				#print ORi
				stavek2 = []
				stavek = []
			
			
					#ORi.append(prop.Or([prop.And(xorList[a[o]]), prop.And(prop.Not(a[u])) for u in range(o, len(a))]))
			
				#ORi.append(prop.Or([prop.And([Eq(a[o]), prop.And([prop.Not(Eq(a[u])) for u in range(o, len(a))])])]))
			l.append(prop.And(ORi))
	return prop.And(l);
			
#def Equiv(x1, x2):
#	return prop.Or([prop.And([x1,x2]), prop.And([prop.Not(x1), prop.Not(x2)])])
	
#def Eq(list):
#	return prop.Or([prop.And(["c%d" % a[i] for i in range(len(list))]), prop.And([prop.Not("c%d" % a[i]) for i in range(len(list))]))

if __name__ == '__main__':
	phi = hadamard(4)
	print phi
	#print phi
	#print prop.sat3(phi.cnf())
	#print prop.sat3(phi)
	#V = 3
	#E = [(0,1), (1,2)]
	#G = (V, E)
	#phi = graph_coloring(G, 1)
	#print prop.sat3(phi)
	