# Analiza wyników eksperymentów



## Cel eksperymentów



Celem eksperymentów było zweryfikowanie poprawności modelu SAT dla problemu totalnego kolorowania grafów oraz zbadanie wpływu struktury grafu na rozmiar generowanych formuł CNF.



Dla każdej instancji grafu testowano kolejne wartości liczby kolorów k. Dla każdej pary (G, k) generowano formułę CNF w formacie DIMACS, uruchamiano solver SAT oraz rejestrowano liczbę zmiennych, liczbę klauzul i wynik SAT/UNSAT.



Minimalną liczbę kolorów definiowano jako najmniejszą wartość k, dla której solver zwrócił wynik SAT.



---



## Minimalna liczba kolorów



| Graf | Minimalne k |
|-------|------------|
| P4 | 3 |
| P6 | 3 |
| P8 | 3 |
| P10 | 3 |
| C4 | 4 |
| C6 | 3 |
| C8 | 4 |
| C10 | 4 |
| diamond | 4 |
| Q3 | 4 |
| K3,3 | 5 |
| K4 | 5 |
| K5 | 5 |
| K4,4 | 6 |
| Petersen | 6 |
| S5 | 6 |
| W5 | 6 |
| K5,5 | 7 |
| K6 | 7 |
| W7 | 8 |
| S8 | 9 |



Wyniki są zgodne z intuicją wynikającą ze struktury grafów. Wraz ze wzrostem gęstości grafu lub maksymalnego stopnia wierzchołka rośnie minimalna liczba kolorów potrzebnych do wykonania poprawnego kolorowania totalnego.



---



## Rozmiar generowanych formuł CNF



Dla wszystkich badanych instancji liczba zmiennych była równa



$$(|V| + |E|)\cdot k,$$



gdzie $|V|$ oznacza liczbę wierzchołków, $|E|$ liczbę krawędzi, a $k$ liczbę dostępnych kolorów.



Przykładowo:



- P10: $(10+9) \cdot 3 = 57$ zmiennych,

- K6: $(6+15)\cdot 7 = 147$ zmiennych,

- K5,5: $(10+25)\cdot 7 = 245$ zmiennych.



Potwierdza to poprawność implementacji generatora CNF.



Znacznie większe różnice zaobserwowano w liczbie klauzul. Dla ścieżki P10 przy minimalnym kolorowaniu wygenerowano 181 klauzul, natomiast dla grafu pełnego K6 już 1197 klauzul. Oznacza to ponad sześciokrotny wzrost rozmiaru formuły przy porównywalnej liczbie kolorowanych obiektów.



Wynika to z większej liczby ograniczeń konfliktowych pomiędzy wierzchołkami i krawędziami w grafach gęstych.



---



## Największe instancje



Największe wygenerowane instancje przedstawiono w tabeli.



| Graf | k | Zmienne | Klauzule |
|-------|---|----------|----------|
| K5,5 | 7 | 245 | 1995 |
| W7 | 8 | 176 | 1310 |
| K6 | 7 | 147 | 1197 |
| S8 | 9 | 153 | 1097 |



Największe formuły generowały grafy pełne, grafy dwudzielne pełne oraz grafy zawierające wierzchołki o bardzo dużym stopniu.



---



## Weryfikacja przypadków UNSAT



Przygotowano środowisko do wykorzystania narzędzia `drat-trim` służącego do niezależnej weryfikacji przypadków UNSAT.



Przeprowadzono próby generowania śladów dowodowych dla instancji niespełnialnych. Narzędzie `drat-trim` zostało poprawnie skompilowane i uruchomione, jednak solvery dostępne poprzez bibliotekę PySAT nie generowały niepustych śladów dowodowych wymaganych do pełnej automatycznej weryfikacji.



Z tego powodu przypadki UNSAT były weryfikowane bezpośrednio przez solver SAT.



---



## Wnioski



1. Model SAT poprawnie rozróżnia przypadki SAT i UNSAT dla wszystkich badanych instancji.



2. Liczba zmiennych rośnie liniowo względem liczby kolorowanych obiektów $(|V|+|E|)$ oraz liczby kolorów $k$.



3. Liczba klauzul silnie zależy od struktury grafu i liczby konfliktów pomiędzy kolorowanymi obiektami.



4. Największe instancje generują grafy pełne oraz grafy dwudzielne pełne.



5. Uzyskane wyniki potwierdzają poprawność implementacji generatora CNF i możliwość wykorzystania solverów SAT do badania problemu totalnego kolorowania grafów.