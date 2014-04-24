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

# Sudoku pretvorjen na barvanje grafov 
def sudoku(s):
	V = 81; #stevilo kvadratkov (vozlisc)
	k = 9; #stevilo barv
	l = []; #list logicnih formul
	# sudoku je oznacen:
	#
	#	1  2  3  4  5  6  7  8  9
	#	10 11 12 13 14 15 16 17 18
	#	...
	#
	
	# pretvori sudoku s v 1d seznam
	novS = [];
	for i in range(k):
		novS = novS + s[i];
	s = novS;
	# print s;

	povVrst = [] # povezani kvadratki v vrsticah
	povStolp = [] # povezani kvadratki v stolpcih
	povKvadr = [] # povezani kvadratki v 3x3 kvadratih
	
	# Konstriramo graf, 9-barvljiv <==> Sudoku resljiv 
	# povezemo kvadratke v vrsticah
	for k in range(0,9):
		for i in range(1,10):
			for j in range(i+1, 10):
				povVrst.append((i+k*9, j+k*9));
	
	#p ovezemo kvadratke v stolpcih
	for i in range(1,10): # index stolpca v k-ti vrstici 
		for k in range(0,9): # index vrstice 
			for j in range(k+1, 9): # stoplci, ki se niso povezavi s k-tim stolpcem 
				povStolp.append((i+9*k, i+9*j));
	
	#povezemo kvadratke znotraj 3x3 kvadratov
	for i in range(0,3):
		for j in range(1,4):
			povKvadr.append(((j*3-1)+(9*(3*i+1)-10), (j*3-1)+(9*(3*i+1))+10)); # Doda povezavo, ki je manjkala 
			povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))+10));
			povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))-10));
			povKvadr.append(((j*3-1)+(9*(3*i+1)-8), (j*3-1)+(9*(3*i+1))+8)); # Doda povezav, ki jo manjkala 
			povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))+8));
			povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))-8));
			povKvadr.append(((j*3-1)+(9*(3*i+1)-1), (j*3-1)+(9*(3*i+1))-9)) # /
			povKvadr.append(((j*3-1)+(9*(3*i+1)+1), (j*3-1)+(9*(3*i+1))-9)) # \
			povKvadr.append(((j*3-1)+(9*(3*i+1)-1), (j*3-1)+(9*(3*i+1))+9)) # /
			povKvadr.append(((j*3-1)+(9*(3*i+1)+1), (j*3-1)+(9*(3*i+1))+9)) # \
	
	povezave = povVrst + povStolp + povKvadr;
	
	# vsako vozlisce ima vsaj eno barvo
	# vozlisca v imajo stevilko v zacetnem sudoku-ju pobarvamo z znano barvo
	#l.append(prop.And([prop.Or(["v%dc%d" % (i, j) for j in range(k)]) for i in range(G[0])]))
	barveVoz = [];
	for i in range(1, V+1):
		if(s[i-1] == None): #ce je None, je lahko ubistvu kjerekoli barve, ce ne upostevamo pogojev
			barveVoz.append(prop.Or(["v%dc%d" % (i, j) for j in range(1, 9+1)]));
		else:
			#print str(i)+" "+s[i-1];
			barveVoz.append("v%dc%d" % (i, int(s[i-1]))); #ce ni None, ima ze tocno doloceno barvo...
	barveVoz = prop.And(barveVoz);
	l.append(barveVoz);
	
	barveKraj = [];
	# pari krajisc so razlicnih barv 
	for (u, v) in povezave:
		if(s[u-1] != None):
			barveKraj.append(prop.Not("v"+str(v)+"c"+s[u-1]));
		elif(s[v-1] != None):
			barveKraj.append(prop.Not("v"+str(u)+"c"+s[v-1]));
		else:
			for c in range(1, 9+1):
				barveKraj.append(prop.Not(prop.And(["v"+str(u)+"c"+str(c), "v"+str(v)+"c"+str(c)])));
	l.append(prop.And(barveKraj));
	
	# vsako vozlisce je kvecjemu ene barve 
	for v in range(1, V+1):
		if(s[v-1] == None):
			for i in range(1, 9+1):
				for j in range(i+1, 9+1):
					l.append(prop.Not(prop.And(["v"+str(v)+"c"+str(i), "v"+str(v)+"c"+str(j)])))
		
	return prop.And(l);

# Prevede dan sudoku na SAT instanco; resi instanco; konstruira resitev za sudoku 
def solveSudoku(sud, sdq):
	sudoku = [0]*81;
	for i in range(1,82):
		for j in range(1,10):
			strng = 'v'+str(i)+'c'+str(j);
			if(strng in sdq[1]):
				if(str(sdq[1][strng]) == "T"):
					sudoku[i-1] = j;
	print "\nSudoku instanca na vodu:\n"
	
	for i in range(9):
		for j in range(9):
			if(sud[i][j] == None):
				print "/",
			else:
				print sud[i][j], 
		print "\n"
	
	print "\nResitev\n:"
	
	for i in range(1,82):
		if(i % 9 == 0):
			print sudoku[i-1],
			print "";
		else:
			print sudoku[i-1],
