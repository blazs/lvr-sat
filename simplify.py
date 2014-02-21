#!/usr/bin/python

"""
Assume values is a dictionary, mapping variables to their values, i.e., values["p"] = True. 
values = { "p" :  True, ..., "q": False } 
"""

import os
import sys
import time

# variable 
class Var:
	def __init__(self, name):
		self.name = name
	def value(self, values):
		return values[self.name]

# logical or 
class Or:
	def __init__(self, varLst):
		self.varLst = varLst
	def value(self, values):
		return reduce(lambda p, q: p or q, [varName.value(assignment) for varName in self.varLst])

class And:
	def __init__(self, varLst):
		self.varLst = varLst
	def value(self, values):
		return reduce(lambda p, q: p and q, [varName.value(assignment) for varName in self.varLst])

def Not:
	def __init__(self, formula):
		self.formula = formula
	def value(self, assignment):
		return not self.formula.value(assignment)
	def str(self):
		return "~", self.formula.str()

# entry point 
if __name__ == '__main__':
	p = Var("p")
	q = Var("q")
	
	notP = Not(p)
	
	assignment = { "p" : False, "q" : True }
	
	print notP.value(assignment)
	
	print And([p, q]).value(assignment)
	print Or([p, q]).value(assignment)
