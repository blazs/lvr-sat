#!/usr/bin/python

import math
import re
import itertools
import prop
import sat as sat
import prevedbe as p
import generate_tests as gen

# Primer uporabe DPLL SAT solverja 
def dpll_sat_test(phi):
	print "#"*3, "Resujem zadovoljivost z DPLL algoritmom", "#"*3
	print "phi = ", phi
	print sat.sat(phi)

# Primer uporabe bruteforce SAT solverja 
def bf_sat_test(phi):
	print "#"*3, "Resujem zadovoljivost z bruteforce algoritmom", "#"*3
	print "phi = ", phi
	print sat.satBruteForce(phi)

# Primer uporabe funkcije za generiranje SAT instanc 
def generate_test():
	pass

# Primer uporabe funkcij za racunanje prevedb odlocitvenih problemov na SAT 
def prevedbe_test():
	print "#"*3, "Prevajam k-barvanje grafa na SAT", "#"*3
	G = (3, [(0,1), (1,2), (0,2)])
	k = 2
	print "Stevilo barv k = ", k , ", graf G = ", G
	phi_g = p.graph_coloring(G, k)
	print "Pripadajoc SAT phi = ", phi_g
	return phi_g

# Vstopna tocka 
if __name__ == "__main__":
	# Test prevedb 
	print "*" * 80
	print "Testiram prevedbe"
	phi_g = prevedbe_test()
	# Test DPLL SAT solverja 
	print "*" * 80
	print "Testiram DPLL SAT solver"
	print dpll_sat_test(phi_g)
	# Test bruteforce SAT solverja 
	print "*" * 80
	print "Testiram bruteforce SAT solver"
	print bf_sat_test(phi_g)
	
	# print mf.sat(p.graph_coloring([3, [(0,1), (0,2), (1,2)]], 2).cnf())
