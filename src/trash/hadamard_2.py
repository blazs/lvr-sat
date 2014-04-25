import prop;
import itertools;
import sat;

def hadamard(n):
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
	
	
r = prop.cnf(hadamard(2));
print r;
s = sat.sat(r);
print s;
			