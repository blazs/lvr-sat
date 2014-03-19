import random
import prop
import math
import re
# Zdruzljivost za Python 2 in Python 3
from prop import isLiteral
#from src.prop import allVariables, Literal, Fls

try:
	basestring
except NameError:
	basestring = str

def sat(phi, d=None, variables=None):
    #Ustvarimo si slovar in mnozico vseh spremenljivk, ce jih ze nimamo
    if not type(d) == dict:
            d = {}
    if not type(variables) == set:
        variables=set()
        prop.allVariables(phi,variables)
    #Predpostavljamo, da sprejmemo v obliki cnf
    if isinstance(phi, prop.Tru): return prop.Tru(), d
    elif isinstance(phi, prop.Fls): return prop.Fls(), None
    elif isinstance(phi, prop.Or) and len(phi.l) == 0: return prop.Fls(), None #Vcasih se zgodi, da dobimo prazen Or namesto prop.Fls
    elif isinstance(phi, prop.And):
        if len(phi.l) == 0: return prop.Tru(), d #prazen And pomeni prop.Tru()
        #print len(phi.l)
        for lit in phi.l:
            if isinstance(lit, prop.Fls): return prop.Fls(), None #ce je vsaj eden od elementov Fls, vrnemo fls
            #elif isinstance()
            elif isinstance(lit, prop.Or):
                if len(lit.l)==0: return prop.Fls(), None #Prazen stavek, zgolj zaradi varnosti
            elif isinstance(lit,prop.Not):
                if lit.t.p not in d: #ce spremenljivke se nismo obravnavali
                    d[lit.t.p]=prop.Fls()
                    phi = phi.apply(d)
                    variables.remove(lit.t.p) #smo jo nastavili
                elif lit.t in d and d[lit.t] == prop.Tru(): return prop.Fls(), None #ce smo jo obravnavali in jo postavili obratno
                else: pass #enkrat smo ze nastavljali to spremenljivko
            elif isinstance(lit,prop.Literal):
                #naredimo skoraj enako kot prej
                if lit.p not in d: #ce spremenljivke se nismo obravnavali
                    d[lit.p]=prop.Tru()
                    phi = phi.apply(d)
                    variables.remove(lit.p) #smo jo nastavili
                elif lit.p in d and d[lit.p] == prop.Fls(): return prop.Fls(), None
                else: pass #enkrat smo ze nastavljali to spremenljivko
            else:
                assert "Nemogoce"
        if len(variables) != 0:#Nismo se porabili vseh spremenljivk
            var=random.sample(variables,1)[0] #si izberemo eno
            variables.remove(var)
            d1=dict(d)
            d1[var]=prop.Tru()
            result, d1 = sat(phi.apply(d1),d1,set(variables))
            if result==prop.Tru(): return result, d1
            d2 = dict(d)
            d2[var]=prop.Fls()
            result, d2 = sat(phi.apply(d2),d2,set(variables))
            if result == prop.Tru(): return result, d2
            return prop.Fls(), None
        else:
            return sat(phi.apply(d),d,variables) #koncali delo, stavki na zacetku funkcije poskrbijo za uspesno koncanje metode

def satBruteForce(phi, d=None, variables=None):
    #Ustvarimo si slovar in mnozico vseh spremenljivk, ce jih ze nimamo
    if not type(d) == dict:
            d = {}
    if not type(variables) == set:
        variables=set()
        prop.allVariables(phi,variables)
    if isinstance(phi, prop.Tru): return prop.Tru(), d
    elif isinstance(phi, prop.Fls): return prop.Fls(), None
    elif isinstance(phi, prop.Or) and len(phi.l) == 0: return prop.Fls(), None #Vcasih se zgodi, da dobimo prazen Or namesto prop.Fls
    elif isinstance(phi, prop.And) and len(phi.l) == 0: return prop.Tru(), d

    #Izberemo si eno spremenljivko in resimo formulo s obema vrednostima te spremenljivke
    var=random.sample(variables,1)[0] #si izberemo eno
    variables.remove(var)
    d1=dict(d)
    d1[var]=prop.Tru()
    result, d1 = satBruteForce(phi.apply(d1),d1,set(variables))
    if result==prop.Tru(): return result, d1
    d2 = dict(d)
    d2[var]=prop.Fls()
    result, d2 = satBruteForce(phi.apply(d2),d2,set(variables))
    if result == prop.Tru(): return result, d2
    return prop.Fls(), None

if __name__ == "__main__":
    d={"a": prop.Fls(),
        "b": prop.Tru(),
        "c": prop.Tru()
        }

    phi=prop.And([prop.Not("a"),prop.Or(prop.Not("b"),"d"),"c",prop.Or([prop.Not("b"),"a"])]).cnf()
    print phi
    print satBruteForce(phi)