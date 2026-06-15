import sys
from pysat.formula import CNF
from pysat.solvers import Solver

if len(sys.argv) != 3:
    print("Usage:")
    print("python verify_unsat.py input.cnf proof.drat")
    sys.exit(1)

cnf_file = sys.argv[1]
proof_file = sys.argv[2]

formula = CNF(from_file=cnf_file)

with Solver(
    name="cadical195",
    bootstrap_with=formula.clauses,
    with_proof=True
) as solver:

    result = solver.solve()

    if result:
        print("SAT")
        sys.exit(0)

    proof = solver.get_proof()

with open(proof_file, "w") as f:
    for line in proof:
        f.write(line)
        if not line.endswith("\n"):
            f.write("\n")

print("UNSAT proof saved to:", proof_file)