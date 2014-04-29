import random
import sys
import prop
import math
import re
from Queue import PriorityQueue
from collections import defaultdict
# Zdruzljivost za Python 2 in Python 3
from prop import isLiteral
#from src.prop import allVariables, Literal, Fls

try:
	basestring
except NameError:
	basestring = str

# NOTE: Predpostavljamo, da je phi v CNF 
def sat(phi, d=None, variables=None):
    #Ustvarimo si slovar in mnozico vseh spremenljivk, ce jih ze nimamo
    if not type(d) == dict:
            d = {}
    if not type(variables) == set:
        variables=set()
        prop.allVariables(phi,variables)
    cleanVariables = set()
    unCleanVariables = set()
    if isinstance(phi, prop.Tru): return prop.Tru(), d
    elif isinstance(phi, prop.Fls): return prop.Fls(), None
    elif isinstance(phi, prop.Or) and len(phi.l) == 0: return prop.Fls(), None #Vcasih se zgodi, da dobimo prazen Or namesto prop.Fls
    elif isinstance(phi, prop.And):
        if len(phi.l) == 0: return prop.Tru(), d #prazen And pomeni prop.Tru()
        #print len(phi.l)
        for lit in phi.l:
            if isinstance(lit, prop.Fls): return prop.Fls(), None #ce je vsaj eden od elementov Fls, vrnemo fls
            elif isinstance(lit, prop.Or):
                if len(lit.l)==0: return prop.Fls(), None #Prazen stavek, zgolj zaradi varnosti, ampak mislim, da vcasih funkcija apply vrne prazen Or

                for lit2 in lit.l: #Literali v Or
                    if isinstance(lit2, prop.Not):
                        if lit2.t in unCleanVariables: pass #spremenljivka je umazana
                        elif lit2 in cleanVariables: pass #spremenljivka ostaja cista
                        elif lit2.t in cleanVariables: # spremenljivka se je umazala
                            unCleanVariables.add(lit2.t) #spremenljivka gre v umazano sobo
                            cleanVariables.remove(lit2.t)
                        elif lit2 not in cleanVariables and lit2.t not in cleanVariables: #spremenljivka ima moznost postati cista
                            cleanVariables.add(lit2)
                        else: assert False, "Tu ni vec nic za narediti"
                    elif isinstance(lit2, prop.Literal):
                        if lit2 in unCleanVariables: pass #spremenljivka je umazana, zanjo ni resitve
                        elif lit2 in cleanVariables: pass #spremenljivka je cista, se je upanje
                        elif prop.Not(lit2) in cleanVariables: #umazali smo spremenljivko
                            cleanVariables.remove(prop.Not(lit2))
                            unCleanVariables.add(lit2)
                        elif lit2 not in cleanVariables and prop.Not(lit2) not in cleanVariables:#spremenljivka ima moznost postati cista
                            cleanVariables.add(lit2)
                        else: assert False, "Tu ni vec nic za narediti"
                    else: assert False, "You shall not pass this door"

            elif isinstance(lit,prop.Not):
                if lit.t.p not in d: #ce spremenljivke se nismo obravnavali
                    d[lit.t.p]=prop.Fls()
                    variables.remove(lit.t.p) #smo jo nastavili
                elif lit.t.p in d and d[lit.t.p] == prop.Tru(): return prop.Fls(), None #ce smo jo obravnavali in jo postavili obratno
                else: pass #enkrat smo ze nastavljali to spremenljivko
            elif isinstance(lit,prop.Literal):
                #naredimo skoraj enako kot prej
                if lit.p not in d: #ce spremenljivke se nismo obravnavali
                    d[lit.p]=prop.Tru()
                    #phi = phi.apply(d)
                    variables.remove(lit.p) #smo jo nastavili
                elif lit.p in d and d[lit.p] == prop.Fls(): return prop.Fls(), None
                else: pass #enkrat smo ze nastavljali to spremenljivko
            else:
                print lit.__class__.__name__
                assert False, "NNemogoce: Je formula res CNF?"

    #pogledamo, ali imamo kaksne ciste spremenljivke, ki jih se nismo spremenili
    for clean in cleanVariables:
        if isinstance(clean,prop.Not):
            if clean.t.p in variables: #spremenljivke se nismo nastavljali
                d[clean.t.p] = prop.Fls()
                variables.remove(clean.t.p)
            else: pass
        elif isinstance(clean, prop.Literal):
            if clean.p in variables: #spremenljivke se nismo nastavljali
                d[clean.p] = prop.Tru()
                variables.remove(clean.p)

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

# NOTE: Predpostavljamo, da je phi v CNF
def sat2(phi, d=None, variables=None):
    #Izboljsan sta solver z hevristiko. Izberemo spremenljivko, ki se je pojavila v najmanjsem izrazu;
    # v primeru izenacenja izberemo tisto, ki se je pojavila najveckrat
    #Ustvarimo si slovar in mnozico vseh spremenljivk, ce jih ze nimamo
    if not type(d) == dict:
            d = {}
    if not type(variables) == set:
        variables=set()
        prop.allVariables(phi,variables)
    cleanVariables = set()
    unCleanVariables = set()
    expressionSize = PriorityQueue() #struktura bo shranjevala, v kako velikem izrazu se spremenljivka pojavi.
    nrOfApperances = defaultdict(lambda: 0)
    if isinstance(phi, prop.Tru): return prop.Tru(), d
    elif isinstance(phi, prop.Fls): return prop.Fls(), None
    elif isinstance(phi, prop.Or) and len(phi.l) == 0: return prop.Fls(), None #Vcasih se zgodi, da dobimo prazen Or namesto prop.Fls
    elif isinstance(phi, prop.And):
        if len(phi.l) == 0: return prop.Tru(), d #prazen And pomeni prop.Tru()
        #print len(phi.l)
        for lit in phi.l:
            if isinstance(lit, prop.Fls): return prop.Fls(), None #ce je vsaj eden od elementov Fls, vrnemo fls
            elif isinstance(lit, prop.Or):
                if len(lit.l)==0: return prop.Fls(), None #Prazen stavek, zgolj zaradi varnosti, ampak mislim, da vcasih funkcija apply vrne prazen Or

                for lit2 in lit.l: #Literali v Or
                    if isinstance(lit2, prop.Not):
                        expressionSize.put((len(lit.l),lit2.t.p))
                        nrOfApperances[lit2.t.p]+=1;
                        if lit2.t in unCleanVariables: pass #spremenljivka je umazana
                        elif lit2 in cleanVariables: pass #spremenljivka ostaja cista
                        elif lit2.t in cleanVariables: # spremenljivka se je umazala
                            unCleanVariables.add(lit2.t) #spremenljivka gre v umazano sobo
                            cleanVariables.remove(lit2.t)
                        elif lit2 not in cleanVariables and lit2.t not in cleanVariables: #spremenljivka ima moznost postati cista
                            cleanVariables.add(lit2)
                        else: assert False, "Tu ni vec nic za narediti"
                    elif isinstance(lit2, prop.Literal):
                        expressionSize.put((len(lit.l),lit2.p))
                        nrOfApperances[lit2.p]+=1;
                        if lit2 in unCleanVariables: pass #spremenljivka je umazana, zanjo ni resitve
                        elif lit2 in cleanVariables: pass #spremenljivka je cista, se je upanje
                        elif prop.Not(lit2) in cleanVariables: #umazali smo spremenljivko
                            cleanVariables.remove(prop.Not(lit2))
                            unCleanVariables.add(lit2)
                        elif lit2 not in cleanVariables and prop.Not(lit2) not in cleanVariables:#spremenljivka ima moznost postati cista
                            cleanVariables.add(lit2)
                        else: assert False, "Tu ni vec nic za narediti"
                    else: assert False, "You shall not pass this door"

            elif isinstance(lit,prop.Not):
                if lit.t.p not in d: #ce spremenljivke se nismo obravnavali
                    d[lit.t.p]=prop.Fls()
                    variables.remove(lit.t.p) #smo jo nastavili
                elif lit.t.p in d and d[lit.t.p] == prop.Tru(): return prop.Fls(), None #ce smo jo obravnavali in jo postavili obratno
                else: pass #enkrat smo ze nastavljali to spremenljivko
            elif isinstance(lit,prop.Literal):
                #naredimo skoraj enako kot prej
                if lit.p not in d: #ce spremenljivke se nismo obravnavali
                    d[lit.p]=prop.Tru()
                    #phi = phi.apply(d)
                    variables.remove(lit.p) #smo jo nastavili
                elif lit.p in d and d[lit.p] == prop.Fls(): return prop.Fls(), None
                else: pass #enkrat smo ze nastavljali to spremenljivko
            else:
                print lit.__class__.__name__
                assert False, "Nemogoce: Je formula res CNF?"

    #pogledamo, ali imamo kaksne ciste spremenljivke, ki jih se nismo spremenili
    for clean in cleanVariables:
        if isinstance(clean,prop.Not):
            if clean.t.p in variables: #spremenljivke se nismo nastavljali
                d[clean.t.p] = prop.Fls()
                variables.remove(clean.t.p)
            else: pass
        elif isinstance(clean, prop.Literal):
            if clean.p in variables: #spremenljivke se nismo nastavljali
                d[clean.p] = prop.Tru()
                variables.remove(clean.p)

    if len(variables) != 0:#Nismo se porabili vseh spremenljivk
        candidates = []
        if (expressionSize.empty() == True): assert False, "Morajo biti vsaj nekatere spremenljivke"
        cand=expressionSize.get()
        while(cand[1] not in variables): #Izberemo prvo spremenljivko, ki se ni bila dolocena
            if (expressionSize.empty() == True): assert False, "Morajo biti vsaj nekatere spremenljivke"
            cand=expressionSize.get()
        candidates.append(cand)
        while (not (expressionSize.empty() == True)): #dodamo vse, ki so izenacene
            cand=expressionSize.get()
            if candidates[0][0]!=cand[0]: break
            candidates.append(cand)
        candidates=sorted([(nrOfApperances[cand[1]], cand[1]) for cand in candidates],reverse=True)
        i=0
        var=candidates[i][1]
        while (var not in variables):
            i+=1
            var=candidates[i][1]
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

# NOTE: Predpostavljamo, da je phi v CNF
def sat3(phi, d=None, variables=None):
    #Izboljsan sta solver z hevristiko, in sicer definirajmo a kot kolikokrat se je pojavila spremenljivka,
    #in b kot dolzino najmanjsega izraza, kjer je spremenljivka nastopala. Hevristika je enaka a/b.
    #Ustvarimo si slovar in mnozico vseh spremenljivk, ce jih ze nimamo
    if not type(d) == dict:
            d = {}
    if not type(variables) == set:
        variables=set()
        prop.allVariables(phi,variables)
    cleanVariables = set()
    unCleanVariables = set()
    heuristicInfo = defaultdict(lambda: [0, -1*sys.maxint+1])#prva komponenta shranjuje, kolikokrat se je spremenljivka
                                    #pojavila, druga pa, kaksna je velikost najmanjsega izraza, v katerem je sodelovala
    if isinstance(phi, prop.Tru): return prop.Tru(), d
    elif isinstance(phi, prop.Fls): return prop.Fls(), None
    elif isinstance(phi, prop.Or) and len(phi.l) == 0: return prop.Fls(), None #Vcasih se zgodi, da dobimo prazen Or namesto prop.Fls
    elif isinstance(phi, prop.And):
        if len(phi.l) == 0: return prop.Tru(), d #prazen And pomeni prop.Tru()
        #print len(phi.l)
        for lit in phi.l:
            if isinstance(lit, prop.Fls): return prop.Fls(), None #ce je vsaj eden od elementov Fls, vrnemo fls
            elif isinstance(lit, prop.Or):
                if len(lit.l)==0: return prop.Fls(), None #Prazen stavek, zgolj zaradi varnosti, ampak mislim, da vcasih funkcija apply vrne prazen Or

                for lit2 in lit.l: #Literali v Or
                    if isinstance(lit2, prop.Not):
                        heuristicInfo[lit2.t.p][1]=min(len(lit.l),heuristicInfo[lit2.t.p][1])
                        heuristicInfo[lit2.t.p][0]+=1;
                        if lit2.t in unCleanVariables: pass #spremenljivka je umazana
                        elif lit2 in cleanVariables: pass #spremenljivka ostaja cista
                        elif lit2.t in cleanVariables: # spremenljivka se je umazala
                            unCleanVariables.add(lit2.t) #spremenljivka gre v umazano sobo
                            cleanVariables.remove(lit2.t)
                        elif lit2 not in cleanVariables and lit2.t not in cleanVariables: #spremenljivka ima moznost postati cista
                            cleanVariables.add(lit2)
                        else: assert False, "Tu ni vec nic za narediti"
                    elif isinstance(lit2, prop.Literal):
                        heuristicInfo[lit2.p][1]=min(len(lit.l),heuristicInfo[lit2.p][1])
                        heuristicInfo[lit2.p][0]+=1;
                        if lit2 in unCleanVariables: pass #spremenljivka je umazana, zanjo ni resitve
                        elif lit2 in cleanVariables: pass #spremenljivka je cista, se je upanje
                        elif prop.Not(lit2) in cleanVariables: #umazali smo spremenljivko
                            cleanVariables.remove(prop.Not(lit2))
                            unCleanVariables.add(lit2)
                        elif lit2 not in cleanVariables and prop.Not(lit2) not in cleanVariables:#spremenljivka ima moznost postati cista
                            cleanVariables.add(lit2)
                        else: assert False, "Tu ni vec nic za narediti"
                    else: assert False, "You shall not pass this door"

            elif isinstance(lit,prop.Not):
                if lit.t.p not in d: #ce spremenljivke se nismo obravnavali
                    d[lit.t.p]=prop.Fls()
                    variables.remove(lit.t.p) #smo jo nastavili
                elif lit.t.p in d and d[lit.t.p] == prop.Tru(): return prop.Fls(), None #ce smo jo obravnavali in jo postavili obratno
                else: pass #enkrat smo ze nastavljali to spremenljivko
            elif isinstance(lit,prop.Literal):
                #naredimo skoraj enako kot prej
                if lit.p not in d: #ce spremenljivke se nismo obravnavali
                    d[lit.p]=prop.Tru()
                    #phi = phi.apply(d)
                    variables.remove(lit.p) #smo jo nastavili
                elif lit.p in d and d[lit.p] == prop.Fls(): return prop.Fls(), None
                else: pass #enkrat smo ze nastavljali to spremenljivko
            else:
                print lit.__class__.__name__
                assert False, "Nemogoce: Je formula res CNF?"

    #pogledamo, ali imamo kaksne ciste spremenljivke, ki jih se nismo spremenili
    for clean in cleanVariables:
        if isinstance(clean,prop.Not):
            if clean.t.p in variables: #spremenljivke se nismo nastavljali
                d[clean.t.p] = prop.Fls()
                variables.remove(clean.t.p)
            else: pass
        elif isinstance(clean, prop.Literal):
            if clean.p in variables: #spremenljivke se nismo nastavljali
                d[clean.p] = prop.Tru()
                variables.remove(clean.p)

    if len(variables) != 0:#Nismo se porabili vseh spremenljivk
        candidates = sorted([(1.0*value[0]/(1.0*value[1]),key) for key, value in heuristicInfo.iteritems()],reverse=True)

        i=0
        while(candidates[i][1] not in variables): i+=1
        var=candidates[i][1]
        while (var not in variables):
            i+=1
            var=candidates[i][1]
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

### NOTE: Spodnji kodni odsek iterativno generira vse {0,1}^n, kot opisano v [Knuth, TAOCP, Volume 4, 2011]. Nedokoncano.
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
	# TODO: Get a list of variables from phi; then feed the list to comb() to get all possible assignments 
	for asg in comb([0,0,0,0,0,0,0,0]):
		print asg
		# print { i : asg[i] for i in range(len(asg)) }

# Vstopna tocka 
if __name__ == "__main__":
    phi = prop.And([("a"),"a",prop.Or(prop.Not("b"),"d"),"c",prop.Or([prop.Not("b"),"a"])]).cnf()
    print phi
    print satBruteForce(phi)
    print sat(phi)
    print sat3(phi)
