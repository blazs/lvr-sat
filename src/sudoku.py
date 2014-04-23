import prop
import math
import re
import itertools
import sat
#import freser_sat

#sudoku pretvorjen na barvanje grafov...
def sudoku(s):
	V = 81; #stevilo kvadratkov (vozlisc)
	k = 9; #stevilo barv
	l = []; #list logicnih formul
	#sudoku je oznacen:
	"""
		1  2  3  4  5  6  7  8  9
		10 11 12 13 14 15 16 17 18
		...
	"""
	
	#pretvori sudoku s v 1d seznam
	novS = [];
	for i in range(k):
		novS = novS + s[i];
	s = novS;
	#print s;

	povVrst = [] #povezani kvadratki v vrsticah
	povStolp = [] #povezani kvadratki v stolpcih
	povKvadr = [] #povezani kvadratki v 3x3 kvadratih
	"""
	for i in range(1, 82):
		if (i % 9 != 0 and i != 81):
			povVrst.append((i,i+1)); #delamo povezave vrstic
		if (i < 73):
			povStolp.append((i,9+i)); #delamo povezave stolpcev
	"""
	# Konstriramo graf, 9-barvljiv <==> Sudoku resljiv 
	#povezemo kvadratke v vrsticah
	for k in range(0,9):
		for i in range(1,10):
			for j in range(i+1, 10):
				povVrst.append((i+k*9, j+k*9));
	
	#povezemo kvadratke v stolpcih
	for i in range(1,10): # index stolpca v k-ti vrstici 
		for k in range(0,9): # index vrstice 
			for j in range(k+1, 9): # stoplci, ki se niso povezavi s k-tim stolpcem 
				povStolp.append((i+9*k, i+9*j));
	
	
			
	#print povVrst;
	#print povStolp;
	
	#povezemo kvadratke znotraj 3x3 kvadratov
	for i in range(0,3):
		for j in range(1,4):
			#povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))+1));
			#povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))-1));
			#povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))+9));
			#povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))-9));
			povKvadr.append(((j*3-1)+(9*(3*i+1)-10), (j*3-1)+(9*(3*i+1))+10)); # Doda povezavo, ki je manjkala 
			povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))+10));
			povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))-10));
			povKvadr.append(((j*3-1)+(9*(3*i+1)-8), (j*3-1)+(9*(3*i+1))+8)); # Doda povezav, ki jo manjkala 
			povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))+8));
			povKvadr.append(((j*3-1)+(9*(3*i+1)), (j*3-1)+(9*(3*i+1))-8));
	#print povKvadr;
	
	povezave = povVrst + povStolp + povKvadr;
	#povezave = povVrst + povKvadr;
	#povezave = list(set(povezave)); #odstranimo duplikate povezav 
	#print povezave
	
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
	#print barveVoz;
	
	barveKraj = [];
	# pari krajisc so razlicnih barv 
	for (u, v) in povezave:
		if(s[u-1] != None):
			#barveKraj.append(prop.Not(prop.And(["v"+str(u)+"c"+s[u-1], "v"+str(v)+"c"+s[u-1]])));
			barveKraj.append(prop.Not("v"+str(v)+"c"+s[u-1]));
		elif(s[v-1] != None):
			#barveKraj.append(prop.Not(prop.And(["v"+str(u)+"c"+s[v-1], "v"+str(v)+"c"+s[v-1]])));
			barveKraj.append(prop.Not("v"+str(u)+"c"+s[v-1]));
		else:
			for c in range(1, 9+1):
				barveKraj.append(prop.Not(prop.And(["v"+str(u)+"c"+str(c), "v"+str(v)+"c"+str(c)])));
		#l.append(prop.And([prop.And([prop.Not(prop.And(["v"+str(u)+"c"+str(c), "v"+str(v)+"c"+str(c)])) for c in range(k)])]))
	#print barveKraj;
	l.append(prop.And(barveKraj));
	#print l;
	# print "BARVEEEEE", k
	# vsako vozlisce je kvecjemu ene barve 
	for v in range(1, V+1):
		if(s[v-1] == None):
			for i in range(1, 9+1):
				for j in range(i+1, 9+1):
					l.append(prop.Not(prop.And(["v"+str(v)+"c"+str(i), "v"+str(v)+"c"+str(j)])))
		
	l = prop.And(l);

	#print l;
	
	return l;
	
def solveSudoku(sud, sdq):
	sudoku = [0]*81;
	for i in range(1,82):
		for j in range(1,10):
			strng = 'v'+str(i)+'c'+str(j);
			if(strng in sdq[1]):
				if(str(sdq[1][strng]) == "T"):
					sudoku[i-1] = j;
	print ""
	print "PODAN SUDOKU..."
	print ""
	
	for i in range(9):
		for j in range(9):
			if(sud[i][j] == None):
				print "/",
			else:
				print sud[i][j], 
		print ""
	
	print ""
	print "RESITEV...."
	print ""
			
	for i in range(1,82):
		if(i % 9 == 0):
			print sudoku[i-1],
			print "";
		else:
			print sudoku[i-1],
			

"""
sud = \
[[None, '8', None, '1', '6', None, None, None, '7'],
 ['1', None, '7', '4', None, '3', '6', None, None],
 ['3', None, None, '5', None, None, '4', '2', None],
 [None, '9', None, None, '3', '2', '7', None, '4'],
 [None, None, None, None, None, None, None, None, None],
 ['2', None, '4', '8', '1', None, None, '6', None],
 [None, '4', '1', None, None, '8', None, None, '6'],
 [None, None, '6', '7', None, '1', '9', None, '3'],
 ['7', None, None, None, '9', '6', None, '4', None]]
 """
 
""" 
sud = \
[[None, '2', '7', '8', '9', '3', None, None, '6'],
[None, '6', '9', None, None, None, '3', None, None],
[None, None, '1', None, None, None, None, None, '8'],
[None, '1', '8', None, None, None, None, None, '4'],
[None, None, None, '1', None, '7', None, None, None],
['9', None, None, None, None, None, '5', None, None],
[None, None, '2', None, None, None, '4', '1', None],
['1', None, None, '9', '5', '6', '8', '3', None]]
"""

## Tezak sudoku (http://lipas.uwasa.fi/~timan/sudoku/) ## 
sud = \
[['1', None, None, None, None, '7', None, '9', None],
[None, '3', None, None, '2', None, None, None, '8'],
[None, None, '9', '6', None, None, '5', None, None],
[None, None, '5', '3', None, None, '9', None, None],
[None, '1', None, None, '8', None, None, None, '2'],
['6', None, None, None, None, '4', None, None, None],
['3', None, None, None, None, None, None, '1', None],
[None, '4', None, None, None, None, None, None, '7'],
[None, None, '7', None, None, None, '3', None, None]]

"""
sud = \
[[None, '4', '8', None, '9', '5', None, None, '6'],
['5', None, '1', '6', '2', '8', '3', None, '9'],
['9', '3', '6', '7', None, '1', None, '8', '2'],
['6', None, '2', '5', '3', '9', '1', '7', '4'],
['3', '5', '9', '1', '7', '4', None, None, None],
[None, '1', '4', None, '6', '2', '9', '5', '3'],
['8', '6', '3', '4', '1', None, '2', None, None],
['1', '9', None, None, '8', '6', '4', '3', '7'],
[None, '2', '7', '9', '5', '3', None, '6', None]];
"""
 
phi = sudoku(sud);
phiCNF = prop.cnf(phi);
#print phi;
#print phiCNF;
#print prop.sat3(phiCNF);
sdq = sat.sat(phiCNF);
print sdq;
#print sdq[1]['v2c0'];
solveSudoku(sud, sdq);
#print sdq[1];
#print sdq[1]['v'+str(11)+'c5'];


	