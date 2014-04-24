#!/usr/bin/python

import math
import re
import itertools
import prop

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
	#print phi
	return phi

# NOTE: Za n=2 dobis out-of-bounds; dvojne negacije; podvojene formule
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