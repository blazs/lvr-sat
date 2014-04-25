#!/usr/bin/python

import math
import re
import itertools
import prop
import sat as sat
import prevedbe as p
import sudoku
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

# Primer uporabe DPLL SAT solverja z hevristiko
def dpll_sat_heuristics_test(phi):
	print "#"*3, "Resujem zadovoljivost z bruteforce algoritmom", "#"*3
	print "phi = ", phi
	print sat.sat2(phi)

# Primer uporabe funkcije za generiranje SAT instanc 
def generate_test():
	pass

# Primer uporabe funkcij za racunanje prevedb odlocitvenih problemov na SAT 
def obarljivostGrafa_test1():
	print "#"*3, "Prevajam k-barvanje grafa na SAT", "#"*3
	G = (3, [(0,1), (1,2), (0,2)])
	k = 2
	print "Stevilo barv k = ", k , ", graf G = ", G
	phi_g = p.graph_coloring(G, k)
	print "Pripadajoc SAT phi = ", phi_g
	return phi_g.cnf()

def testirajNaVsehSolverjih(phi):
    # Test DPLL SAT solverja
    print "*" * 80
    print "Testiram DPLL SAT solver"
    print dpll_sat_test(phi)
    # Test bruteforce SAT solverja
    print "*" * 80
    print "Testiram bruteforce SAT solver"
    print bf_sat_test(phi)
    #Test DPLL SAT solverja s preprosto hevristiko
    print "*" * 80
    print "Testira DPLL SAT z hevristiko"
    print dpll_sat_heuristics_test(phi)

# Vstopna tocka
if __name__ == "__main__":
	# Test prevedb

    # 1. Obarljivost grafa
    print "*" * 80
    print "Testiram prevedbo na obarljivost grafa"
    phi_g = obarljivostGrafa_test1()
    testirajNaVsehSolverjih(phi_g)
    print "#" * 80
    #2. Sudokuprint "*" * 80
    print "Testiram prevedbe"
    phi_g = obarljivostGrafa_test1()
    testirajNaVsehSolverjih(phi_g)
    print "#" * 80



