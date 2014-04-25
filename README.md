lvr
===

Koda in dokumentacija za predmet [Logika v racunalnistvu](http://ucilnica.fmf.uni-lj.si/course/view.php?id=252).

# Dokumentacija 

## Struktura projekta 
 * `doc/` vsebuje opis nekaterih prevedb odlocitvenih problemov na SAT. 
 * `src/` vsebuje izvorno kodo:
   * `src/main.py` glavna datoteka s primeri uporabe;
   * `src/prop.py` osnovne podatkovne strukture.;
   * `src/prevedbe.py` implementacija prevedb nekaterih odlocitvenih problemov na SAT;
   * `src/sat.py` naiven bruteforce SAT solver in DPLL SAT solver [[2](#literatura)]; predpostavlja, da je vhodna formula v CNF;
   * `src/generate_tests.py` preprost generator testnih instanc;
   * `src/sat14.cc` C++ program [3], ki sta ga objavila B. Konev in A. Lisista; implementira njuno prevedbo Erdosevega problema diskrepance na SAT.
[//]: # (Vsebuje tudi naiven SAT solver, ki iterativno preisce vseh 2^n prireditev vrednosti izrazu, a je nedokoncan.)
## Primer uporabe 
 To je kratek opis uporabe nase implementacije. 
### Manipuliranje Boolovih formul
  Primer.
### Uporaba SAT solverja
  Primer.
### Uporaba prevedb
  Primeri.

## Komentar
 Uporabili smo seznam benchmark sudokujev [4].
 
 Prevedbe problemov smo na grobo opisali v `doc/lvr-docs.pdf`; implementacije prevedb najdemo v `src`; glej opis strukture projekta. 
 
 Za Erdosev problem diskrepance (EDP) smo vzeli C++ program `sat14` [3], ki za dane parametre --- dolzina zaporedja, diskrepanca, in stevilo bitov --- generira SAT instanco v CNF obliki. Nasa koda prevede in pozene `sat14`, pocisti njegov izhod ter ga prevede iz [DIMACS](http://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/satformat.ps) formata v nas format. (Nas solver po nekaj urah ne konca na vhodu C=1 za dolzino 11; to je najkrajsa dolzina za katero ne obstaja +/- zaporedje diskrepance kvecjemu 1 [3].)
## Literatura 
 * [1] Huth and Ryan. [Logic in Computer Science: Modelling and Reasoning about Systems](http://www.amazon.com/Logic-Computer-Science-Modelling-Reasoning/dp/052154310X), second edition, 2004.
 * [2] Wikipedia. [DPLL algorithm](http://en.wikipedia.org/wiki/DPLL_algorithm), Wikipedia, accessed 28 March 2014.
 * [3] Boris Konev and Alexei Lisista. [SAT encoding of the Erdős discrepancy problem](http://cgi.csc.liv.ac.uk/~konev/SAT14/).
 * [4] Timo Mantere and Janne Koljonen. [Sudoku research page](http://lipas.uwasa.fi/~timan/sudoku/). 
