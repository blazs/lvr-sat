#!/usr/bin/python

import prop
import math
import re
import itertools
import freser_sat as mf
import prevedbe as p

# Vstopna tocka 
if __name__ == "__main__":
	print mf.sat(p.graph_coloring([3, [(0,1), (0,2), (1,2)]], 2).cnf())
