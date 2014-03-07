#!/usr/bin/python

"""
Assume values is a dictionary, mapping variables to their values, i.e., values["p"] = True. 
values = { "p" :  True, ..., "q": False } 

-- borjab, blazs, martinf
"""

import os
import sys
import time

# constants 
class Fls:
	def __init__(self):
		pass
	def value(self, assignment = None):
		return False
	def repr(self):
		return "F"

class Tru:
	def __init__(self):
		pass
	def value(self, assignment = None):
		return True
	def repr(self):
		return "T"

# variables 
class Var:
	def __init__(self, name):
		self.name = name
	def value(self, values):
		return values[self.name]
	def repr(self):
		return self.name

# formulas 
class Or:
	def __init__(self, varLst):
		self.varLst = varLst
	def value(self, values):
		return reduce(lambda p, q: p or q, [varName.value(assignment) for varName in self.varLst])
	def repr(self):
		return "("+"".join([var.repr()+"|" for var in self.varLst])[:-1]+")"

class And:
	def __init__(self, varLst):
		self.varLst = varLst
	def value(self, values):
		return reduce(lambda p, q: p and q, [varName.value(assignment) for varName in self.varLst])
	def repr(self):
		return "("+"".join([var.repr()+"&" for var in self.varLst])[:-1]+")"

class Not:
	def __init__(self, formula):
		self.formula = formula
	def value(self, assignment):
		return not self.formula.value(assignment)
	def repr(self):
		return "~("+self.formula.repr()+")"

# nnf
def nnf(f):
	if isinstance(f, Not):
		if isinstance(f.formula, And): # de morgan 
			return Or([nnf(Not(fml)) for fml in f.formula.varLst])
		elif isinstance(f.formula, Or): # de morgan 
			return And([nnf(Not(fml)) for fml in f.formula.varLst])
		elif isinstance(f.formula, Not): return f.formula.formula
		elif isinstance(f.formula, Tru): return Fls()
		elif isinstance(f.formula, Fls): return Tru()
		elif isinstance(f.formula, Var): return f
	else: return f

def simplify(f):
	pass

def parser(s):
	pass

# entry point 
if __name__ == '__main__':
	p = Var("p")
	q = Var("q")
	
	notP = Not(Or([And([p, q]), And([Not(p), Not(q)]), Fls()]))
	print notP.repr()
	
	print nnf(notP).repr()
	
	assignment = { "p" : False, "q" : True }
	print notP.value(assignment)
