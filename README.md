# Totalne kolorowanie grafu jako problem SAT

## Opis projektu

Projekt realizuje redukcję problemu totalnego kolorowania grafu do problemu SAT.

Dla zadanego grafu i liczby kolorów k generowana jest formuła CNF w formacie DIMACS. Następnie solver SAT sprawdza, czy istnieje poprawne totalne kolorowanie wykorzystujące k kolorów.

## Struktura repozytorium

src/

* total\_coloring.py – generator formuł CNF

examples/

* grafy testowe

scripts/

* check\_cnf.py – sprawdzanie SAT/UNSAT
* run\_experiments.py – automatyczne eksperymenty
* verify\_unsat.py – próby weryfikacji UNSAT

results/

* results.csv – wyniki eksperymentów
* analysis.md – analiza wyników

tools/

* drat-trim

## Uruchomienie

Generowanie CNF:

python src/total\_coloring.py examples/P4.txt 3 output.cnf

Sprawdzenie SAT/UNSAT:

python scripts/check\_cnf.py output.cnf

Uruchomienie eksperymentów:

python scripts/run\_experiments.py

## Wyniki

Wyniki eksperymentów znajdują się w:

results/results.csv

Analiza wyników znajduje się w:

results/analysis.md

Autorzy 
Klaudia Buczek  
Klara Pluta

Gabriela Warchoł

