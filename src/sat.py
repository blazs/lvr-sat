#!/usr/bin/python

import prop

# Generates {0,1}^n in lexiographic order 
# See Knuth, TAOCP, 4th ed., 2011 
# XXX: Incementally compute combinations? 
def comb(L):
	R = []
	L.append(0)
	j = n = len(L)
	while True:
		R.append(L[1:])
		j = n-1
		# NOTE: Changing `L[j] == 1' to `L[j] == mi' will generate [m1] x [m2] x ... x [mn], where [mi] denotes {1,2, ..., mi}
		while j > 0 and L[j] == 1:
			L[j] = 0
			j = j-1
		L[j] = L[j]+1
		if j == 0: break
	return R

# tries all possible assignments 
def brute_force(phi):
	for asg in comb([0,0,0,0,0,0,0,0]):
		print asg
		# print { i : asg[i] for i in range(len(asg)) }
