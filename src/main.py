#!/usr/bin/python

# 
# Nekaj primerov uporabe ter testiranje in merjenje casa.
# 

import math
import re
import itertools
import prop
import sat as sat
import prevedbe as p
import generate_tests as gen
import helpers as h
import time
import numpy as np

### Primer uporabe SAT solverjev ###
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

### Primer uporabe implementacij prevedb ###
# Primer uporabe funkcij za racunanje prevedb odlocitvenih problemov na SAT 
def graph_coloring_2sat(G):
	print "#"*3, "Prevajam k-barvanje grafa na SAT", "#"*3
	G = (3, [(0,1), (1,2), (0,2)])
	k = 2
	print "Stevilo barv k = ", k , ", graf G = ", G
	phi_g = p.graph_coloring(G, k)
	print "Pripadajoc SAT phi = ", phi_g
	return phi_g.cnf()

def hadamard(n):
	return p.hadamard2sat(n)

def sudoku(fname = 'sudoku.in'):
	# pretvori sudoku iz formata [4] v nas format 
	sudoku = h.parseSudoku(fname)
	# vrne pripadajoco SAT instanco 
	return p.sudoku2sat(sudoku)
	
# Erdosev problem diskrepance 
# C ... diskrepanca 
# L ... dolzina zaporedja 
def edp(C = 1, L = 5):
	return p.edp2sat(C, L)

###  ###
# Primer uporabe funkcije za generiranje SAT instanc 
def generate_test():
	pass
def test1():
    ## Sestavljanje in manipuliranje formul ##
    # Sestavimo zelo enostavno formulo u \/ v
    phi = prop.Or(["v", "u"])

    ## Uporaba SAT solverjev ##
    # Test DPLL SAT solverja
    print "*" * 80
    print "Testiram DPLL SAT solver"
    dpll_sat_test(phi)
    # Test bruteforce SAT solverja
    print "*" * 80
    print "Testiram bruteforce SAT solver"
    bf_sat_test(phi)

    ## Prevedbe ##
    print "*" * 80
    print "*" * 80
    print "Testiram prevedbe"
    # k-barvanje grafov
    print "*" * 80
    print "Barvanje grafov"
    k = 2 # dvodelnost
    G = (3, [(0,1), (1,2), (0,2)])
    phi = p.graph_coloring2sat(G, k)
    print phi
    # Sudoku
    print "*" * 80
    print "Sudoku"
    S = h.get_sudoku('sudoku01a.in')
    phi = p.sudoku2sat(S)
    print phi
    # Hadamard
    print "*" * 80
    print "Hadamard"
    phi = hadamard(4)
    print phi
    # Erdosev problem diskrepance
    print "*" * 80
    print "Erdosev problem diskrepance"
    phi = edp(1, 5)
    print phi
def test2():
    #preprost casovni test razlicnih sat solverjev
    S = h.get_sudoku('sudoku01a.in')
    phi = p.sudoku2sat(S)
    print phi
    print "testiram sudoku z DPLL sat"
    start = time.time()
    print sat.sat(phi.cnf())
    print "potreboval sem %.3f s" %(time.time()-start)
    print "testiram sudoku z DPLL sat z hevristiko"
    start = time.time()
    print sat.sat2(phi.cnf())
    print "potreboval sem %.3f s" %(time.time()-start)
def test3():
    # experimentiramo na sudoku, kateri sat solver je hitrejsi, z n ponovitvami in na koncu izpisemo rezultate
    start2=time.time()
    n = 50 # stevilo ponovitev 
    sudokuFile="s10a.txt" # tezek sudoku
    S = h.get_sudoku(sudokuFile)
    phi = p.sudoku2sat(S)
    dpll = []
    dpllHeu1 = []
    dpllHeu2 = []
    for i in range(n):
        print i
        start = time.time()
        sat.sat(phi.cnf())
        dpll.append(time.time() - start)
    for i in range(n):
        print i
        start = time.time()
        sat.sat2(phi.cnf())
        dpllHeu1.append(time.time() - start)
    for i in range(n):
        print i
        start = time.time()
        sat.sat3(phi.cnf())
        dpllHeu2.append(time.time() - start)
    results = "Testirali smo na sudoku %s z %d ponovitvami\n" \
            "DPLL:                    \tpovprecno %.4f z odklonom %.4f\n" \
            "DPLL z prvo hevristiko:  \tpovprecno %.4f z odklonom %.4f\n" \
            "DPLL z drugo hevristiko: \tpovprecno %.4f z odklonom %.4f\n" %(sudokuFile, n, np.mean(dpll), np.std(dpll),
                                                                            np.mean(dpllHeu1), np.std(dpllHeu1),
                                                                            np.mean(dpllHeu2), np.std(dpllHeu2))
    print results
    print "porabili smo %.3f s" %(time.time()-start2)
    with open("resutlsOfTest3.txt", "w") as f:
        f.write(results)


# Vstopna tocka 
if __name__ == "__main__":
    test1() # Primeri uporabe 
    # test2() # Preprost casovni test razlicnih sat solverjev
    # test3() # Eksperimentiramo na sudoku, kateri sat solver je hitrejsi, z n ponovitvami in na koncu izpisemo rezultate
