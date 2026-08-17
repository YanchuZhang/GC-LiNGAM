# Model Equivalence in Linear Non-Gaussain Causal Models Under General Confounding

This repository contains the code accompanying my master's thesis, *"Model Equivalence in Linear Non-Gaussain Causal Models Under General Confounding"*.


## Repository Structure

```text
.
├── utils.py                        # Main graphical tools for checking equivalence
├── z3_solver.ipynb                 # SMT based approach
├── meek.ipynb                      # Meek conjecture testing
├── reversal.ipynb                  # Reversal conjecture testing
├── demo_graphical_methods.ipynb    # Demo of the proposed graphical method
├── data/                           # Performance testing
├── requirements.txt                # Python dependencies
└── README.md
```

## Overview

### 1. Basic 

Run `from utils import *` to access all basic tools we need.

To define ADMGs, we need to first create empty `nx.Digraph()` objects, and then define the set of vertices $\{1,\dots,n\}$ and set of directed edges. Add them to `nx.Digraph()` to create DAGs.

```python
# Number of Vertices
n = 3

# Generate DAGs
G1 = nx.DiGraph()
G2 = nx.DiGraph()

# Define vertices
V = range(1,n+1)
G1.add_nodes_from(V)
G2.add_nodes_from(V)

# Edge Sets
E1 = [(1,2),(2,3)]
E2 = [(1,2),(1,3)]
B1 = [(2,3)]
B2 = [(2,3)]

# Add Edges
G1.add_edges_from(E1)
G2.add_edges_from(E2)
```

We define the bidirected parts of the ADMGs separatly.

```
B1 = [(2,3)]
B2 = [(2,3)]
```

Then, we determine model inclusion by running `check_inclusion_full(G1, G2, B1, B2)`.

### 2. Practical Tools

* Plot ADMGs by `plot_admg(G,B)`
* Define induced graph by `induced_graph(V,B1,B2)`, plot this afterwards by `plot_induced(IG)`
* To Plot induced graph with details on intrinsic properties of the vertices, run `plot_auxiliary(G1,G2,B1,B2)`
* Plot induced graph reduction by `plot_reduced(G1,G2,B1,B2)`
* To check if a given set of edges is a vertex cover, run `is_vertex_cover(E, S)`
* To check path rank from $X$ to $Y$ in $G$, run `path_rank(G, X, Y)`
* To get a random DAG, run `random_dag(n, p)` with density $p$
* To get random confounding, run `random_confounding(n, k)` with $k$ bidirected edges
* Enumerate inclusive minimal vertex covers by `minimal_vertex_covers_fast(G)`
* To find model equivalent graphs by DFS/BFS, run `find_equivalence_class_meek(E,B,n)` This does not always give the entire equivalence class, but this is very fast to list all equivalent graphs connected in the Hasse diagram.
* To find model equivalent graphs by exhaustive search, run `find_equivalent_graphs_exhaustive(E,B,n)`. This is not suitable for $n>5$.

### 3. Others
For SMT based, approach, see the demo in `z3_solver.ipynb`.

