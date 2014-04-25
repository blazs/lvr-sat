import prop
import math
import re
import itertools
import sat
#import freser_sat


def hadamard(n):
	#hadamardove matrike obstajajo le za sode n
	assert n % 2 == 0;
	if(n % 2 != 0):
		return prop.Fls();
		
	l = [];
	
	#predpostavka - prva vrstica so vsi True
	l.append(prop.And(["v0s%d" % i for i in range(n)]));
	
	#generiramo mozne kombinacije, tako da je n/2 clenov True in n/2 False
	a = list(itertools.combinations(range(n), n/2)); #print a;
	#print a;
	#gneriraj vse mozne vrstice | v moz[i] so spravljenje vse mogoce kombinacije spremenljivk za vrstico i
	moz = [[]];
	for i in range(1,n):
		moz.append([]);
		for j in range(len(a)):
			moz[i].append(prop.And([prop.Not("v"+str(i)+"s%d" % k) if (k not in a[j]) else "v"+str(i)+"s%d" % k for k in range(n)]));
	#print moz;
	#generiraj vse mozne matrike, katerih vrstice bi ustrezale Hadamardovi matriki
	#b = list(itertools.combinations(range(1,n*len(a)), n-1)); #iz vseh moznih vrstic moramo izbrati n-1, ker prvo ze imamo
	#print b;
	moz2 = [];
	
	b = list(itertools.combinations(range(len(moz[1])), n-1));
	for j in range(1):#range(len(b)):
		moz2.append(prop.And([l[0], prop.And([moz[i][b[j][i-1]] for i in range(1,n)])]));
	print moz2;
	return prop.Or(moz2);
	"""
	for i in range(n-1):
	#for i in range(1):
		#moz2.append([moz[j] for j in b[i]]);
		#print moz2[i];
		moz2.append(prop.And([l[0], prop.And([moz[i][j] for j in range(len(moz[i]))])]));
	#print moz;
	#print moz2;
	#naredimo OR teh matrik
	return prop.Or(moz2);
	#print c;
	#return c;
	"""
	
	#return moz;
	
def solveHadamard(hdm, n):
	print "Hadamardova matrika za n="+str(n)+":";
	for i in range(n):
		for j in range(n):
			strng = "v"+str(i)+"s"+str(j);
			if(str(hdm[1][strng]) == "T"):
				print "+1",
			else:
				print "-1",
		print ""
	
	
h = prop.cnf(hadamard(4));
solv = sat.sat(h);
print solv;
solveHadamard(solv, 4);
#phi = prop.cnf(h);
#print phi;
#print prop.sat3(h);