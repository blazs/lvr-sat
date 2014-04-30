#!/usr/bin/python

import math
import re
import itertools
import prop
import os # Klicemo g++ 
import helpers as h

# Takes an instance of graph k-coloring problem (G,k) and outputs corresponsing Boolean formula Phi such
# that Phi is satisfiable if and only if G is k-colorable. 
def graph_coloring2sat(G, k):
	# G[0] naj bo stevilo povezav 
	# G[1] naj bo seznam parov vozlics, a.k.a, seznan pobexzav
	# k > 0 je stevilo barv 
	assert k > 0, "Premalo barv"
	
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

def hadamard2sat(n):
	assert n % 2 == 0;
	l = [];
	
	#naredi matrikco za lazje mislit
	ma3ka = {};
	for i in range(n):
		for j in range(n):
			ma3ka[(i,j)]  = "v"+str(j)+"s"+str(i); #vjsi = vrstica j, stolpec i
	print ma3ka;
	
	xOri = []
	#nardimo xOre vrstic za vsak stolpec.
	for i in range(n-1):
		for j in range(n):
			xOri.append(prop.Or([prop.And([ma3ka[(i,j)], prop.Not(ma3ka[(i+1,j)])]), prop.And([prop.Not(ma3ka[(i,j)]), ma3ka[(i+1,j)]])]));
		#vse mozne true - false kombinacije
		a = list(itertools.combinations(xOri, len(xOri)/2));
		
		#generiramo mozne stolpce
		stolpec = []
		for j in range(len(a)):
			stolpec.append(prop.And([x if x in a[j] else prop.Not(x) for x in xOri]));
			
		#nardimo or moznih stolpcev
		l.append(prop.Or(stolpec));
		xOri = [];
		
	#vrnemo koncno formulo
	return prop.And(l);

# Sudoku preveden na barvanje grafov 
def sudoku2sat(s):
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
# sdq ... SAT instanca, ki pripada sudokujevi instanci 
# sud ... sudoku instanca 
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

# Erdosev problem diskrepance
# Klicemo rahlo spremenjen zunanji C++ program [Konev and Lisista, 2014]. Program
# vrne SAT instanco v CNF, ki ustreza Erdosevemu problemu diskrepance za dane parametre. Formulo
# pretvorimo v primerno obliko in jo nahranimo nasemu solverju. 
def edp2sat(C, L):
	bits = int(math.ceil(math.log(2*(C+1), 2)))
	discrepancy = C
	length = L
	cmd = 'sat14 %d %d %d > out.cnf' % (length, discrepancy, bits)
	print "Compiling sat14.cc..."
	os.system('g++ sat14.cc -o sat14')
	print "Running sat14.cc..."
	os.system(cmd)
	print "Cleaning up the output..."
	os.system('grep -v "^c" out.cnf | grep -v "^$" > new.cnf')
	phi = h.parse_output('new.cnf')
	#print "Running the SAT solver..."
	return phi
