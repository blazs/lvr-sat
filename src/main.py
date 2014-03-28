#!/usr/bin/python

import math
import re
import itertools
import prop
import freser_sat as mf
import prevedbe as p
import generate_tests as gen

# Primer uporabe DPLL SAT solverja 
def dpll_sat_test():
	pass

# Primer uporabe bruteforce SAT solverja 
def bf_sat_test():
	pass

# Primer uporabe funkcije za generiranje SAT instanc 
def generate_test():
	pass

# Primer uporabe funkcij za racunanje prevedb odlocitvenih problemov na SAT 
def prevedbe_test():
	pass

# Vstopna tocka 
if __name__ == "__main__":
	print mf.sat(p.graph_coloring([3, [(0,1), (0,2), (1,2)]], 2).cnf())
