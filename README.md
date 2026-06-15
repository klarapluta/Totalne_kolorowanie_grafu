# Totalne kolorowanie grafu jako problem SAT

## Opis projektu

Projekt realizuje redukcję problemu totalnego kolorowania grafu do problemu SAT.

Dla zadanego grafu i liczby kolorów k generowana jest formuła CNF w formacie DIMACS. Następnie solver SAT sprawdza, czy istnieje poprawne totalne kolorowanie wykorzystujące k kolorów.

## Struktura repozytorium

src

* total\_coloring.py - generator formuł CNF

examples

* grafy testowe

scripts

* check\_cnf.py - sprawdzanie SAT/UNSAT
* run\_experiments.py - automatyczne eksperymenty
* verify\_unsat.py - próby weryfikacji UNSAT

results

* results.csv - wyniki eksperymentów
* analysis.md - analiza wyników

tools

* drat-trim

## Uruchomienie

Generowanie CNF:

python src/total\_coloring.py examples/P4.txt 3 output.cnf

Sprawdzenie SAT/UNSAT:

python scripts/check\_cnf.py output.cnf

Uruchomienie eksperymentów:

python scripts/run\_experiments.py

## Eksperymenty

W ramach projektu przeprowadzono eksperymenty dla różnych rodzin grafów, m.in. ścieżek, cykli, grafów pełnych, grafów dwudzielnych pełnych, gwiazd, kół, grafu Petersena oraz grafu kostki Q3.

Dla każdego grafu testowano kolejne wartości liczby kolorów k. Dla każdej pary (G, k) generowano formułę CNF, uruchamiano solver SAT oraz zapisywano liczbę zmiennych, liczbę klauzul i wynik SAT/UNSAT.

Pozwoliło to wyznaczyć minimalną liczbę kolorów dla badanych grafów oraz przeanalizować rozmiary generowanych instancji SAT.

## Wyniki

Tabela wyników eksperymentów znajduje się w pliku: results/results.csv

Szczegółowa analiza otrzymanych wyników znajduje się w pliku: results/analysis.md

### Autorzy

Klaudia Buczek  
Klara Pluta
Gabriela Warchoł

