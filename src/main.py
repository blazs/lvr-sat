#!/usr/bin/python

# 
# Nekaj primerov uporabe 
# 

import math
import re
import itertools
import prop
import sat as sat
import prevedbe as p
import generate_tests as gen
import helpers as h

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
	sudoku = parseSudoku(fname)
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

# Vstopna tocka 
if __name__ == "__main__":
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
