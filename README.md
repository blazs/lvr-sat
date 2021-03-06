lvr
===

``_I can't get no [SAT](http://en.wikipedia.org/wiki/Boolean_satisfiability_problem)isfaction._'' --- The Rolling Stones

Borja Bovcon, Martin Freser, Blaz Sovdat.

# Dokumentacija 

## Struktura projekta 
 * `doc/` vsebuje opis nekaterih prevedb odlocitvenih problemov na SAT. 
 * `src/` vsebuje izvorno kodo:
   * `src/main.py` glavna datoteka s primeri uporabe;
   * `src/prop.py` osnovne podatkovne strukture.;
   * `src/prevedbe.py` implementacija prevedb nekaterih odlocitvenih problemov na SAT;
   * `src/sat.py` naiven bruteforce SAT solver in DPLL SAT solver [[2](#literatura)]; predpostavlja, da je vhodna formula v CNF;
   * `src/generate_tests.py` preprost generator testnih instanc;
   * `src/helpers.py` pomozne funkcije za pretvarjanje med formati (sudoku v nas interni format, ipd.);
   * `src/sat14.cc` C++ program [3], ki sta ga objavila [B. Konev](http://cgi.csc.liv.ac.uk/~konev/) in [A. Lisista](https://cgi.csc.liv.ac.uk/~alexei/); implementira njuno prevedbo Erdosevega problema diskrepance na SAT;
   * `src/trash/` po  smeteh ne brskamo.
[//]: # (Vsebuje tudi naiven SAT solver, ki iterativno preisce vseh 2^n prireditev vrednosti izrazu, a je nedokoncan.)
## Primer uporabe 
 To je kratek opis uporabe nase implementacije. 
### Manipuliranje Boolovih formul
  Boolove formule definiramo v datoteki `prop.py`. Definirajmo preprosto formulo `phi = prop.And(["a","b",prop.Or(prop.Not("a"),"b")])`. Klic nam shrani v objekt `phi` formulo: `a /\ b /\ (~a \/ b)`. Njeno CNF obliko lahko izracunamo z naslednjim klicem: `phi_cnf = phi.cnf()`. Za vec primerov glej kodo. 

### SAT solver  
  Naj bo `phi` Boolova formula v CNF obliki; glej prejšnji podrazdelek za več o formulah. Ko uvozimo modul `src/sat.py` (ukaz `import sat`), lahko kličemo `sat.sat(phi)`; to je DPLL [2] solver. Za bruteforce solver kličemo `sat.satBruteFroce(phi)`.

### Prevedbe
  Prevedbe so implementirane v modulu `src/prevedbe.py`. Na voljo so naslednje funkcije:
   * `graph_coloring2sat(G, k)` vrne SAT instanco, ki je zadovoljiva natanko tedaj, ko je (neusmerjen) graf `G` `k`-obarvljiv. Pri tem je `G=(n, E)`, pri cemer je `n` stevilo povezav in je `E=[(i,j),...,(k,r)]` seznam povezav; vsaka povezava je predstavljena s parom vozlisc; vozlisca so cela stevila `{1,2,...,n}`.
   * `sudoku2sat(sudoku)` vrne SAT instanco, ki je zadovoljiva natanko tedaj, ko je `sudoku` resljiv. Pri tem je `sudoku=h.get_sudoku(sudoku01a.in)`, kjer je `sudoku01a.in` sudoku v formatu [4]. Funkcijo `get_sudoku` najdemo v modulu `helper` (ukaz `import helper as h`).
   * `hadamard2sat(n)` vrne SAT instanco, ki je zadovoljiva natanko tedaj, ko obstaja `n`-krat-`n` Hadamardova matrika. 
   * `edp2sat(C, L)` vrne SAT instanco, ki je zadovoljiva natanko tedaj, ko obstaja +/- zaporedje dolzine `L` diskrepance `C`. (Absolutna vrednost vsote je enaka `C`.)

## Komentar
  Uporabili smo seznam benchmark sudokujev [4].
 
  Primerjave hitrosti sat solverjev si lahko ogledate v `src/resutlsOfTest3.txt`, kjer smo testirali na težkem sudokuju.
 
  Prevedbe problemov smo na grobo opisali v `doc/lvr-docs.pdf`; implementacije prevedb najdemo v `src`; glej opis strukture projekta. 
 
  Za Erdosev problem diskrepance (EDP) smo vzeli C++ program `sat14` [3], ki za dane parametre --- dolzina zaporedja, diskrepanca, in stevilo bitov --- generira SAT instanco v CNF obliki. Nasa koda prevede in pozene `sat14`, pocisti njegov izhod ter ga prevede iz [DIMACS](http://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/satformat.ps) formata v nas format.
[//]: #  (Nas solver po nekaj urah ne konca na vhodu C=1 za dolzino 11; to je najkrajsa dolzina za katero ne obstaja +/- zaporedje diskrepance kvecjemu 1 [3].)
  
  SAT solver smo izboljšali z dvema enostavnima hevristikama:
   * Izberemo spremenljivko, ki se je pojavila v najmanjšem izrazu; v primeru izenačenja izberemo tisto, ki se je pojavila največkrat.
   * Definirajmo `a` kot kolikokrat se je spremenljivka pojavila v izrazu in `b` kot dolžino najmanjšega izraza, v katerem je sodelovala spremenljivka. Izberemo spremenljivko, katera ima največjo vrednost `a/b`. Za to hevristiko smo se odločili, saj želimo imeti čim večji `a` in čim manjši `b`.

## Literatura 
 * [1] Huth and Ryan. [Logic in Computer Science: Modelling and Reasoning about Systems](http://www.amazon.com/Logic-Computer-Science-Modelling-Reasoning/dp/052154310X), second edition, 2004.
 * [2] Wikipedia. [DPLL algorithm](http://en.wikipedia.org/wiki/DPLL_algorithm), Wikipedia, accessed 28 March 2014.
 * [3] Boris Konev and Alexei Lisista. [SAT encoding of the Erdős discrepancy problem](http://cgi.csc.liv.ac.uk/~konev/SAT14/).
 * [4] Timo Mantere and Janne Koljonen. [Sudoku research page](http://lipas.uwasa.fi/~timan/sudoku/). 
