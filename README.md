lvr
===

Logika v racunalnistvu --- koda iz vaj.

# Dokumentacija 

## Struktura projekta 
 * `doc/` vsebuje opis nekaterih prevedb odlocitvenih problemov na SAT. 
 * `src/` vsebuje izvorno kodo:
   * `src/main.py` glavna datoteka s primeri uporabe.
   * `src/prop.py` osnovne podatkovne strukture, rahlo spremenjena @jaanos koda. 
   * `src/simplify.sat` poenostavljanje izrazov. 
   * `src/sat.py` naiven SAT solver.
   * `src/freser_sat.py` DPLL SAT solver [2](##literatura), predpostavlja, da je vhodna formula v CNF.
   * `src/generate_tests.py` preprost generator testnih instanc.

## Primer uporabe 
 V delu.

## Literatura 
 * [1] Huth and Ryan, [Logic in Computer Science: Modelling and Reasoning about Systems](http://www.amazon.com/Logic-Computer-Science-Modelling-Reasoning/dp/052154310X), 2nd ed., 2004.
 * [2] Wikipedia, [DPLL algorithm](http://en.wikipedia.org/wiki/DPLL_algorithm), Wikipedia, accessed 28-Mar-2014.
