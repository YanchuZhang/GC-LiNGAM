# Model Equivalence in Linear Non-Gaussain Causal Models Under General Confounding

This repository contains the code accompanying my master's thesis, *"Model Equivalence in Linear Non-Gaussian Causal Models Under General Confounding"*.


## Repository Structure

```text
.
├── utils.py                        # Main graphical tools for checking equivalence
├── z3_solver.ipynb                 # SMT based approach
├── traversal.ipynb                 # Traversal analysis
├── reversal.ipynb                  # Reversal conjecture testing
├── demo_graphical_methods.ipynb    # Demo of the proposed graphical method
├── data/                           # Performance testing
├── requirements.txt                # Python dependencies
└── README.md
```

## Overview

### 1. Basics

After installing all dependencies, run `from utils import *` to access all basic tools needed.

To define an ADMG, we first create an empty `nx.DiGraph()` object. We then define the set of vertices ${1,\dots,n}$ and the set of directed edges, and add them to the `nx.DiGraph()` object to create the DAG.

```python
# Define the number of vertices
n = 3

# Define empty DAGs
G1 = nx.DiGraph()
G2 = nx.DiGraph()

# Define and add vertices to DAGs
V = range(1,n+1)
G1.add_nodes_from(V)
G2.add_nodes_from(V)

# Define edge sets
E1 = [(1,2),(2,3)]
E2 = [(1,2),(1,3)]
B1 = [(2,3)]
B2 = [(2,3)]

# Add edges to the DAGs
G1.add_edges_from(E1)
G2.add_edges_from(E2)
```

We define the bidirected parts of the ADMGs separately.

```python
B1 = [(2,3)]
B2 = [(2,3)]
```

Finally, we determine model inclusion using `check_inclusion_full(G1, G2, B1, B2)`.

### 2. Practical Tools

* Plot ADMGs using `plot_admg(G,B)`
* Define the induced graph using `induced_graph(V,B1,B2)`, and plot it using `plot_induced(IG)`
* To plot the induced graph with details on the intrinsic properties of its vertices, run `plot_auxiliary(G1,G2,B1,B2)`
* Plot the reduced induced graph using `plot_reduced(G1,G2,B1,B2)`
* To check whether a given set of edges is a vertex cover, run `is_vertex_cover(E, S)`
* To compute the path rank from $X$ to $Y$ in $G$, run `path_rank(G, X, Y)`
* To generate a random DAG, run `random_dag(n, p)`, where $p$ is the edge density
* To generate random confounding, run `random_confounding(n, k)`, where $k$ is the number of bidirected edges
* Enumerate inclusive minimal vertex covers using `minimal_vertex_covers_fast(G)`
* To find model-equivalent graphs using DFS/BFS, run `find_equivalence_class_traversal(E,B,n)`. This does not always return the entire equivalence class, but it is very fast for listing all equivalent graphs connected in the Hasse diagram.
* To find model equivalent graphs by exhaustive search, run `find_equivalent_graphs_exhaustive(E,B,n)`. This is not suitable for $n > 5$.

### 3. SMT-based Methods
For the SMT-based approach, see `z3_solver.ipynb`.

