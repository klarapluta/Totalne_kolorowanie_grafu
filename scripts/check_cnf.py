import sys
from pysat.formula import CNF
from pysat.solvers import Glucose3

if len(sys.argv) != 2:
    print("Użycie: python check_cnf.py plik.cnf")
    sys.exit(1)

cnf_file = sys.argv[1]

formula = CNF(from_file=cnf_file)

with Glucose3(bootstrap_with=formula.clauses) as solver:
    result = solver.solve()

print("SAT" if result else "UNSAT")