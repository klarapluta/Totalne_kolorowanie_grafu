import sys
from pysat.formula import CNF
from pysat.solvers import Glucose3

# Oczekiwana nazwa pliku CNF jako argumnent
if len(sys.argv) != 2:
    print("Użycie: python check_cnf.py plik.cnf")
    sys.exit(1)

# Wczytanie formuły CNF z pliku
cnf_file = sys.argv[1]

# Wczytanie formuły CNF zapisanej w formacie DIMACS
formula = CNF(from_file=cnf_file)

# Uruchomienie solvera SAT na wczytanej formule
with Glucose3(bootstrap_with=formula.clauses) as solver:
    result = solver.solve()

print("SAT" if result else "UNSAT")