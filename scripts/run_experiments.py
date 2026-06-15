import csv
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Glucose3


ROOT_DIR = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT_DIR / "examples"
CNF_DIR = ROOT_DIR / "results" / "cnf"
RESULTS_FILE = ROOT_DIR / "results" / "results.csv"

K_VALUES = list(range(2, 14))
TIMEOUT_SECONDS = 30


def read_graph(filename):
    vertices = set()
    edges = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("c"):
                continue

            if line.startswith("p"):
                continue

            if line.startswith("e"):
                _, u, v = line.split()
                u = int(u)
                v = int(v)

                edges.append((u, v))
                vertices.add(u)
                vertices.add(v)

    return sorted(vertices), edges


def generate_total_coloring_cnf(vertices, edges, k):
    clauses = []

    objects = []

    for v in vertices:
        objects.append(v)

    for e in edges:
        objects.append(e)

    var = {}
    next_var = 1

    for obj in objects:
        for color in range(1, k + 1):
            var[(obj, color)] = next_var
            next_var += 1

    for obj in objects:
        clauses.append([var[(obj, color)] for color in range(1, k + 1)])

    for obj in objects:
        for c1 in range(1, k + 1):
            for c2 in range(c1 + 1, k + 1):
                clauses.append([
                    -var[(obj, c1)],
                    -var[(obj, c2)]
                ])

    for (u, v) in edges:
        for color in range(1, k + 1):
            clauses.append([
                -var[(u, color)],
                -var[(v, color)]
            ])

    m = len(edges)

    for i in range(m):
        e1 = edges[i]

        for j in range(i + 1, m):
            e2 = edges[j]

            if len(set(e1) & set(e2)) > 0:
                for color in range(1, k + 1):
                    clauses.append([
                        -var[(e1, color)],
                        -var[(e2, color)]
                    ])

    for (u, v) in edges:
        e = (u, v)

        for color in range(1, k + 1):
            clauses.append([
                -var[(u, color)],
                -var[(e, color)]
            ])

            clauses.append([
                -var[(v, color)],
                -var[(e, color)]
            ])

    return clauses, next_var - 1


def save_dimacs(filename, clauses, num_vars):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"p cnf {num_vars} {len(clauses)}\n")

        for clause in clauses:
            line = " ".join(map(str, clause))
            f.write(line + " 0\n")


def solve_cnf(cnf_path):
    formula = CNF(from_file=str(cnf_path))

    with Glucose3(bootstrap_with=formula.clauses) as solver:
        solver.conf_budget(TIMEOUT_SECONDS * 100000)

        result = solver.solve_limited(expect_interrupt=True)

    if result is True:
        return "SAT"

    if result is False:
        return "UNSAT"

    return "TIMEOUT"


def run_single_experiment(graph_path, k):
    graph_name = graph_path.stem
    cnf_path = CNF_DIR / f"{graph_name}_k{k}.cnf"

    vertices, edges = read_graph(graph_path)

    clauses, variables = generate_total_coloring_cnf(
        vertices,
        edges,
        k
    )

    save_dimacs(
        cnf_path,
        clauses,
        variables
    )

    solver_result = solve_cnf(cnf_path)

    return {
        "graph": graph_name,
        "vertices": len(vertices),
        "edges": len(edges),
        "k": k,
        "variables": variables,
        "clauses": len(clauses),
        "solver_result": solver_result
    }


def main():
    CNF_DIR.mkdir(parents=True, exist_ok=True)

    graph_files = sorted(EXAMPLES_DIR.glob("*.txt"))

    rows = []

    for graph_path in graph_files:
        for k in K_VALUES:
            print(f"Running {graph_path.name}, k={k}...")

            row = run_single_experiment(graph_path, k)
            rows.append(row)

            print(
                f"  {row['solver_result']} | "
                f"vars={row['variables']} | "
                f"clauses={row['clauses']}"
            )

            if row["solver_result"] == "SAT":
                print(f"  First SAT found for {graph_path.name}: k={k}")
                break

    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "graph",
                "vertices",
                "edges",
                "k",
                "variables",
                "clauses",
                "solver_result"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    print()
    print(f"Results saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    main()