#!/usr/bin/python

import random as rnd
import prop
import freser_sat as mf

# 
# Generira testne primere. (Oprostita, ker pisem Python kodo v Cjevskem stilu.)
# 

def shuffle(L):
	for i in range(len(L)):
		r = rnd.randint(i, len(L)-1)
		L[i], L[r] = L[r], L[i]
	return L

# Vrne ``nakljucno'' (to je tukaj slabo-definiran pojem :-) instanco SAT problema 
# Vrnjena instanca ima dolzino kvecjemu length in kvecjemu vars razlicnih spremenljivk 
def random_phi(length = 10, vars = 10):
	V = ["phi"+str(i) for i in range(vars)]
	phi = []
	i = 0
	while i < length:
		tmp = []
		if i >= length-3: break
		k = rnd.randint(3, length-i-1)
		for j in range(k):
			tmp_var = V[rnd.randint(0, vars-1)]
			# P(negacija formula) = 1/2? 
			if rnd.randint(0, 5) <= 3: tmp.append(prop.Not(tmp_var) if rnd.randint(0,1) == 0 else tmp_var) # E[dolzina] = k * 3/5
			else: break
			i = i+1
		if len(prop.Or(tmp).l) > 0: phi.append(prop.Or(tmp)) # Protislovja spustimo (zato vrnemo formulo dolzine kvecjemu length :-)
		i = i+1
	return prop.And(phi)

# Vzame seznam literalov; ga nakljucno permutira; razbije na k delov; vrne konjunkcijo. (Hvala prof. Bauerju za kul predlog. :-)
def rnd_cnf(literals, k = 3):
	literals = shuffle(literals)
	n = len(literals)
	return prop.And([prop.Or(literals[i*n/k:(i+1)*n/k]) for i in range(n/k)])

# Vrne ``tezko'' instanco SAT problema 
# Ideja: Generiraj DNF na enak nacin pri rnd_cnf; vrni CNF.
def hard_phi(literals, k = 3):
	literals = shuffle(literals)
	n = len(literals)
	L = [prop.And(literals[i*n/k:(i+1)*n/k]) for i in range(n/k)]
	L.append(literals[0])
	print L
	return prop.Or(L).cnf()

# Vstopna tocka; nekaj testov; samo za okus 
if __name__ == "__main__":
    j=10
    literals = [prop.Not("v"+str(i)) for i in range(j)]
    literals = literals + ["v"+str(i) for i in range(j)]
    phi = hard_phi(literals, 3)
    print phi
    print mf.sat(phi)
