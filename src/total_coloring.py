
# witam  w projekcie numer 6
# totalnym kolorowaniem grafu G o k kolorach nazywamy funckje f: V \cup E -> [k] tż:
#    * dla każdej krawędzi uv zachodzi f(u) =! f(v),
#    * dla każdych dwóch różnych krawędzi uv, ux zachodzi f(uv) =! f(ux),
#    * dla każdej krawędzi uv zachodzi f(u) =! f(uv) and f(v) =!f(uv)
# 1. zamodelować formułę logiczną kodującą problem istnienia totalnego kolorowania grafów grafu G przy użyciu k kolorów
# 2. napisać program, który dla zadanego wejścia generuje formułę CNF w formacie dimacs kodującą problem zgodnie z formułą
# 3. przeprowadzić eksperymenty przy użyciu wybranych grafów testowych dla wygenerowanych formuł:
#       uruchomienie obliczeń SAT-solvera, weryfikacja przy pomocy narzędzia drat-trim.


import sys

# Wczytanie grafu w formacie DIMACS Graph

def read_graph(filename):
    """
    Czyta graf w formacie:

    c komentarz
    p edge n m
    e u v
    e u v
    ...

    Zwraca:
        vertices - lista wierzchołków
        edges    - lista krawędzi
    """

    vertices = set()
    edges = []

    with open(filename, "r") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            # komentarze pomijamy
            if line.startswith("c"):
                continue

            # linia p edge n m
            if line.startswith("p"):
                continue

            # krawędź
            if line.startswith("e"):

                _, u, v = line.split()

                u = int(u)
                v = int(v)

                edges.append((u, v))

                vertices.add(u)
                vertices.add(v)

    vertices = sorted(vertices)

    return vertices, edges

# Generowanie CNF dla totalnego kolorowania
def generate_total_coloring_cnf(vertices, edges, k):

    clauses = []

    # Wszystkie obiekty grafu: wierzchołki + krawędzie

    objects = []

    for v in vertices:
        objects.append(v)

    for e in edges:
        objects.append(e)

    # Numeracja zmiennych SAT:  x_(obiekt, kolor)

    var = {}

    next_var = 1

    for obj in objects:
        for color in range(1, k + 1):

            var[(obj, color)] = next_var
            next_var += 1

    # 1. Każdy obiekt ma przynajmniej jeden kolor

    for obj in objects:

        clause = []

        for color in range(1, k + 1):
            clause.append(var[(obj, color)])

        clauses.append(clause)

    # 2. Każdy obiekt ma co najwyżej jeden kolor

    for obj in objects:

        for c1 in range(1, k + 1):
            for c2 in range(c1 + 1, k + 1):

                clauses.append([
                    -var[(obj, c1)],
                    -var[(obj, c2)]
                ])

    # 3. Sąsiednie wierzchołki: f(u) != f(v)

    for (u, v) in edges:

        for color in range(1, k + 1):

            clauses.append([
                -var[(u, color)],
                -var[(v, color)]
            ])

    # 4. Sąsiednie krawędzie: f(e1) != f(e2)

    m = len(edges)

    for i in range(m):

        e1 = edges[i]

        for j in range(i + 1, m):

            e2 = edges[j]

            # wspólny wierzchołek
            if len(set(e1) & set(e2)) > 0:

                for color in range(1, k + 1):

                    clauses.append([
                        -var[(e1, color)],
                        -var[(e2, color)]
                    ])

    # 5. Krawędź i jej końce:  f(u) != f(uv),  f(v) != f(uv)

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

# Zapis CNF do DIMACS
def save_dimacs(filename, clauses, num_vars):

    with open(filename, "w") as f:

        f.write(f"p cnf {num_vars} {len(clauses)}\n")

        for clause in clauses:

            line = " ".join(map(str, clause))
            f.write(line + " 0\n")


def main():

    if len(sys.argv) != 4:

        print("Użycie:")
        print("python total_coloring.py graph.txt k output.cnf")
        return

    graph_file = sys.argv[1]
    k = int(sys.argv[2])
    output_file = sys.argv[3]

    # wczytanie grafu
    vertices, edges = read_graph(graph_file)

    print("Liczba wierzchołków:", len(vertices))
    print("Liczba krawędzi:", len(edges))
    print("Liczba kolorów:", k)

    # generowanie CNF
    clauses, num_vars = generate_total_coloring_cnf(
        vertices,
        edges,
        k
    )

    print("Liczba zmiennych:", num_vars)
    print("Liczba klauzul:", len(clauses))

    # zapis DIMACS
    save_dimacs(
        output_file,
        clauses,
        num_vars
    )

    print("Zapisano:", output_file)


if __name__ == "__main__":
    main()

    