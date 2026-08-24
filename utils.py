import networkx as nx
import matplotlib.pyplot as plt
import random
from itertools import combinations, product
from z3 import *
import sympy as sp
import numpy as np
from fractions import Fraction
import time
import csv
from collections import deque

def is_vertex_cover(E, S):
    S = set(S)
    for u, v in E:
        if u not in S and v not in S:
            return False
    return True

def plot_admg(G,B):
    options = {
    "font_size": 10,
    "node_size": 300,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 1,
    "width": 1,
    }
    G_B = nx.Graph()
    G_B.add_nodes_from(G.nodes)
    G_B.add_edges_from(B)
    jitter_strength = 0.1
    for layer, nodes in enumerate(nx.topological_generations(G)):
        for node in nodes:
            G.nodes[node]["layer"] = layer
    pos = nx.multipartite_layout(G, subset_key="layer")
    pos = {
    node: (x + random.uniform(-jitter_strength, jitter_strength),
        y + random.uniform(-jitter_strength, jitter_strength))
    for node, (x, y) in pos.items()
    }
    nx.draw_networkx(G, pos=pos, **options)
    nx.draw_networkx_edges(G_B, pos, edge_color="red", arrows=True, arrowstyle="<->", connectionstyle="arc3, rad=0.5", style="dashed")
    ax = plt.gca()
    ax.margins(0.20)
    plt.show()

def path_rank(G, X, Y):
    if not X or not Y:
        return 0
    H = nx.DiGraph()
    for v in G.nodes():
        H.add_edge((v, 'in'), (v, 'out'), capacity=1)
    for u, v in G.edges():
        H.add_edge((u, 'out'), (v, 'in'), capacity=len(G))
    S = 'S'
    T = 'T'
    for x in X:
        H.add_edge(S, (x, 'in'), capacity=len(G))
    for y in Y:
        H.add_edge((y, 'out'), T, capacity=len(G))
    flow_value, _ = nx.maximum_flow(H, S, T)
    return flow_value

def non_connected_pairs(vertices, edgelist):
    edge_set = {tuple(sorted((u, v))) for u, v in edgelist}
    return [
        (u, v)
        for u, v in combinations(vertices, 2)
        if (u, v) not in edge_set
    ]

def extended_pairs(vertices, edgelist):
    self_pairs = [(i, i) for i in vertices]
    symB1 = [(j, i) for i, j in edgelist]
    return edgelist + symB1 + self_pairs

def induced_graph(V,B1,B2):
    IG = nx.Graph()
    for i in V:
        for j in V:
            IG.add_node((i, j))
    for u, v in non_connected_pairs(V, B2):
        for i,j in extended_pairs(V, B1):
            IG.add_edge((u,i),(v,j))
    return IG

def plot_induced(IG):
    options = {
    "font_size": 6,
    "node_size": 500,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 1,
    "width": 1,
    }
    pos = {(i, j): (j, i) for i, j in IG.nodes()}
    nx.draw_networkx(IG,pos, arrows=True, **options, connectionstyle="arc3,rad=0.2")
    plt.gca().invert_yaxis()
    ax = plt.gca()
    ax.margins(0.20)
    ax.set_axis_off()
    plt.show()

def trivial_row(V, edges):
    vertices = set(V)
    endpoints = set()
    for u, v in non_connected_pairs(V, edges):
        endpoints.add(u)
        endpoints.add(v)
    return list(vertices - endpoints)

def get_removable(V, G1, G2, B2):
    removable = []
    unremovable = []
    for i in V:
        if i not in trivial_row(V, B2):
            for j in V:
                if path_rank(G1, [j], list(G2.predecessors(i)) + [i]) == 0:
                    removable.append((i,j))
                else:
                    if path_rank(G1, [j], list(G2.predecessors(i))) == 0:
                        unremovable.append((i,j))
        else:
            for j in V:
                removable.append((i,j))

    return removable, unremovable

def IG_clean_up(IG, G1, G2, B2):
    V = list(G1.nodes())
    V.sort()
    remain = set(IG.nodes)-set(get_removable(V, G1, G2, B2)[0])
    IG_re = IG.subgraph(remain).copy()
    IG_re.remove_nodes_from(list(nx.isolates(IG_re)))
    return IG_re

def neighbors_of_set(G, S):
    result = set()
    for u in S:
        result.update(G.neighbors(u))
    return result - set(S)

def plot_auxiliary(G1, G2, B1, B2):
    V = list(G1.nodes())
    V.sort()
    IG = induced_graph(V, B1, B2)
    IG_cleaned = IG_clean_up(IG, G1, G2, B2)
    unremovable = get_removable(V, G1, G2, B2)[1] & IG_cleaned.nodes
    unremovable_neighbors = neighbors_of_set(IG_cleaned, unremovable)
    node_colors = [
    "#d62728" if node in unremovable else
    "#1f77b4" if node in unremovable_neighbors else
    "white"
    for node in IG_cleaned.nodes()
    ]
    options = {
    "font_size": 6,
    "node_size": 500,
    "node_color": node_colors,
    "edgecolors": "black",
    "linewidths": 1,
    "width": 1,
    }
    pos = {(i, j): (j, i) for i, j in IG_cleaned.nodes()}
    nx.draw_networkx(IG_cleaned, pos, arrows=True, **options, connectionstyle="arc3,rad=0.2")
    plt.gca().invert_yaxis()
    ax = plt.gca()
    ax.margins(0.20)
    ax.set_axis_off()
    plt.show()
    if IG_cleaned.subgraph(unremovable).number_of_edges() > 0:
        return True # Is tractable
    return(is_vertex_cover(IG_cleaned.edges, unremovable_neighbors))

def st_plot_auxiliary(G1, G2, B1, B2):
    V = list(G1.nodes())
    V.sort()
    IG = induced_graph(V, B1, B2)
    IG_cleaned = IG_clean_up(IG, G1, G2, B2)
    unremovable = get_removable(V, G1, G2, B2)[1] & IG_cleaned.nodes
    unremovable_neighbors = neighbors_of_set(IG_cleaned, unremovable)
    node_colors = [
        "#d62728" if node in unremovable else
        "#1f77b4" if node in unremovable_neighbors else
        "white"
        for node in IG_cleaned.nodes()
    ]
    options = {
        "font_size": 6,
        "node_size": 500,
        "node_color": node_colors,
        "edgecolors": "black",
        "linewidths": 1,
        "width": 1,
    }
    pos = {(i, j): (j, i) for i, j in IG_cleaned.nodes()}
    fig, ax = plt.subplots()
    nx.draw_networkx(
        IG_cleaned,
        pos,
        arrows=True,
        ax=ax,
        **options,
        connectionstyle="arc3,rad=0.2"
    )
    ax.invert_yaxis()
    ax.margins(0.20)
    plt.close(fig)
    return fig
    
def random_dag(n, p=0.3, seed=None):
    if seed is not None:
        random.seed(seed)
    G = nx.DiGraph()
    nodes = list(range(1, n + 1))
    random.shuffle(nodes)
    G.add_nodes_from(nodes)
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                G.add_edge(nodes[i], nodes[j])
    return G

def random_confounding(n, k, seed=None):
    if seed is not None:
        random.seed(seed)
    nodes = range(1, n + 1)
    all_edges = list(combinations(nodes, 2))
    if k > len(all_edges):
        raise ValueError(f"Too many edges: max for n={n} is {len(all_edges)}")
    return list(random.sample(all_edges, k))

def is_good(G1, G2, B1, B2):
    V = list(G1.nodes())
    V.sort()
    IG = induced_graph(V, B1, B2)
    removable, unremovable = get_removable(V,G1,G2,B2)
    remain = set(IG.nodes)-set(removable)
    IG_re = IG.subgraph(remain).copy()
    IG_re.remove_nodes_from(list(nx.isolates(IG_re)))
    unremovable = unremovable & IG_re.nodes
    unremovable_neighbors = neighbors_of_set(IG_re, unremovable)
    return(is_vertex_cover(IG_re.edges, unremovable_neighbors | unremovable))

def is_finished(G1, G2, B1, B2):
    V = list(G1.nodes())
    V.sort()
    IG = induced_graph(V, B1, B2)
    removable, unremovable = get_removable(V,G1,G2,B2)
    remain = set(IG.nodes)-set(removable)
    IG_re = IG.subgraph(remain).copy()
    IG_re.remove_nodes_from(list(nx.isolates(IG_re)))
    unremovable = unremovable & IG_re.nodes
    unremovable_neighbors = neighbors_of_set(IG_re, unremovable)
    if IG_re.subgraph(unremovable).number_of_edges() > 0:
        return True
    for i in V:
        X = get_j(unremovable_neighbors,i)
        Y = list(G2.predecessors(i))
        if not path_rank(G1, X, Y + [i]) == path_rank(G1, X, Y):
            return True
    if is_vertex_cover(IG_re.edges, unremovable_neighbors | unremovable):
        return True
    return False

def estimate_good_probability(N, num_vertex, num_confounding):
    count_true = 0
    for _ in range(N):
        G1 = random_dag(num_vertex,random.random())
        B1 = random_confounding(num_vertex,num_confounding)
        G2 = random_dag(num_vertex,random.random())
        B2 = random_confounding(num_vertex,num_confounding)
        if is_good(G1,G2,B1,B2):
            count_true += 1
    return count_true / N

def plot_reduced(G1,G2,B1,B2):
    V = list(G1.nodes())
    V.sort()
    IG = induced_graph(V, B1, B2)
    IG_cleaned = IG_clean_up(IG, G1, G2, B2)
    unremovable = get_removable(V, G1, G2, B2)[1] & IG_cleaned.nodes
    unremovable_neighbors = neighbors_of_set(IG_cleaned, unremovable)

    remain = IG_cleaned.nodes - unremovable - unremovable_neighbors
    IG_remain = IG_cleaned.subgraph(remain).copy()
    IG_remain.remove_nodes_from(list(nx.isolates(IG_remain)))

    options = {
    "font_size": 6,
    "node_size": 500,
    "edgecolors": "black",
    "node_color": "white",
    "linewidths": 1,
    "width": 1,
    }
    pos = {(i, j): (j, i) for i, j in IG_remain.nodes()}
    nx.draw_networkx(IG_remain, pos, arrows=True, **options, connectionstyle="arc3,rad=0.2")
    plt.gca().invert_yaxis()
    ax = plt.gca()
    ax.margins(0.20)
    ax.set_axis_off()
    plt.show()

def st_plot_reduced(G1,G2,B1,B2):
    V = list(G1.nodes())
    V.sort()
    IG = induced_graph(V, B1, B2)
    IG_cleaned = IG_clean_up(IG, G1, G2, B2)
    unremovable = get_removable(V, G1, G2, B2)[1] & IG_cleaned.nodes
    unremovable_neighbors = neighbors_of_set(IG_cleaned, unremovable)

    remain = IG_cleaned.nodes - unremovable - unremovable_neighbors
    IG_remain = IG_cleaned.subgraph(remain).copy()
    IG_remain.remove_nodes_from(list(nx.isolates(IG_remain)))

    options = {
    "font_size": 6,
    "node_size": 500,
    "edgecolors": "black",
    "node_color": "white",
    "linewidths": 1,
    "width": 1,
    }
    pos = {(i, j): (j, i) for i, j in IG_remain.nodes()}
    fig, ax = plt.subplots()
    nx.draw_networkx(IG_remain, pos, arrows=True, ax=ax, **options, connectionstyle="arc3,rad=0.2")
    ax.invert_yaxis()
    ax.margins(0.20)
    plt.close(fig)
    return fig


def find_not_good_pair(N, num_vertex, num_confounding):
    for _ in range(N):
        G1 = random_dag(num_vertex,random.random())
        B1 = random_confounding(num_vertex,num_confounding)
        G2 = random_dag(num_vertex,random.random())
        B2 = random_confounding(num_vertex,num_confounding)
        if not is_finished(G1,G2,B1,B2):
            return G1,G2,B1,B2

def get_j(S, i):
    return {j for x, j in S if x == i}

def check_inclusion(G1,G2,B1,B2):
    V = list(G1.nodes())
    V.sort()
    IG = induced_graph(V, B1, B2)
    IG_cleaned = IG_clean_up(IG, G1, G2, B2)
    unremovable = get_removable(V, G1, G2, B2)[1] & IG_cleaned.nodes
    unremovable_neighbors = neighbors_of_set(IG_cleaned, unremovable)
    if not is_vertex_cover(IG_cleaned.edges, unremovable_neighbors | unremovable):
        return "Not tractable"
    if IG_cleaned.subgraph(unremovable).number_of_edges() > 0:
        return False
    for i in V:
        X = get_j(unremovable_neighbors,i)
        Y = list(G2.predecessors(i))
        if not path_rank(G1, X, Y + [i]) == path_rank(G1, X, Y):
            return False
    return True

def powerset(s):
    s = list(s)
    n = len(s)
    result = []
    for i in range(1 << n):
        subset = {s[j] for j in range(n) if (i & (1 << j))}
        result.append(subset)
    return result

def remove_strict_supersets(P, S):
    S = set(S)
    result = []
    for subset in P:
        subset_set = set(subset)
        if not (S < subset_set):
            result.append(subset)
    return result

def inclusive_minimal_covers(IG_remain,P):
    n = len(P)
    k = 0
    for _ in range(n):
        if k == len(P):
            break
        if not is_vertex_cover(IG_remain.edges(),P[k]):
            P.pop(k)
        else:
            P = remove_strict_supersets(P,P[k])
            k = k+1
    return P

def minimal_vertex_covers_fast(G):
    H = nx.complement(G)
    V = set(G.nodes())
    for clique in nx.find_cliques(H):
        independent_set = set(clique)

        yield V - independent_set

def check_inclusion_full(G1,G2,B1,B2):

    if len(B1) != len(B2):
        return False
    
    V = list(G1.nodes())
    V.sort()
    IG = induced_graph(V, B1, B2)
    IG_cleaned = IG_clean_up(IG, G1, G2, B2)
    unremovable = get_removable(V, G1, G2, B2)[1] & IG_cleaned.nodes
    unremovable_neighbors = neighbors_of_set(IG_cleaned, unremovable)

    if IG_cleaned.subgraph(unremovable).number_of_edges() > 0:
        return False

    for i in V:
        X = get_j(unremovable_neighbors,i)
        Y = list(G2.predecessors(i))
        if not path_rank(G1, X, Y + [i]) == path_rank(G1, X, Y):
            return False
    
    if is_vertex_cover(IG_cleaned.edges, unremovable_neighbors):
        return True

    remain = IG_cleaned.nodes - unremovable - unremovable_neighbors
    IG_remain = IG_cleaned.subgraph(remain).copy()
    IG_remain.remove_nodes_from(list(nx.isolates(IG_remain)))

    for cover in minimal_vertex_covers_fast(IG_remain):
        for i in V:
            X = list(get_j(unremovable_neighbors,i)) + list(get_j(cover,i))
            Y = list(G2.predecessors(i))
            if path_rank(G1, X, Y + [i]) != path_rank(G1, X, Y):
                break
        else:
            return True
            
    return False

def create_z3_variables(E):
    return {
        (u, v): Real(f"x_{u}_{v}")
        for u, v in E
    }

def create_random_B(E, n):
    L = sp.zeros(n, n)

    for u, v in E:
        # random rational number
        numerator = random.randint(-1000, 1000)
        denominator = random.randint(1, 1000)
        L[u-1, v-1] = sp.Rational(numerator, denominator)

    I = sp.eye(n)
    return (I - L).inv().T

def create_equation(i, j, n, x_vars, B):

    expr = B[i-1,j-1]

    for k in range(n):
        if (k+1, i) in x_vars and B[k,j-1]!=0:
            expr -= x_vars[(k+1, i)] * B[k,j-1]

    return expr

def create_variables(edge_list):
    return {(u, v): sp.Symbol(f"m_{u}_{v}") for u, v in edge_list}


def get_M_matrix(edge_list, n):
    vars = create_variables(edge_list)
    M = sp.zeros(n)

    for (u, v), var in vars.items():
        M[u-1, v-1] = var

    return M, list(vars.values())

def get_L_matrix(edge_list, n, low=-1.0, high=1.0):
    L = np.zeros((n, n))

    for u, v in edge_list:
        L[u-1, v-1] = np.random.uniform(low, high)

    return L

def get_J(B2, n):
    B2 = set(B2)
    return [(i, j) for i in range(1, n+1)
                   for j in range(i+1, n+1)
                   if (i, j) not in B2]

def get_K(B1, n):
    symmetric_B1 = set(B1) | {(j, i) for i, j in B1}
    return [(i, j)
            for i in range(1, n+1)
            for j in range(1, n+1)
            if i == j or (i, j) in symmetric_B1]

def map_pairs(JK):
    return [((a, c), (b, d)) for ((a, b), (c, d)) in JK]

def filter_pairs(JK, A):
    return [((a, b), (c, d)) 
            for ((a, b), (c, d)) in JK
            if A[a-1, b-1] != 0 and A[c-1, d-1] != 0]

def create_equations(JK, A):
    return [
        A[a-1, b-1] * A[c-1, d-1]
        for ((a, b), (c, d)) in JK
    ]

def get_both_linear_equations(JK, A):
    return [
        [A[a-1, b-1] , A[c-1, d-1]]
        for ((a, b), (c, d)) in JK
    ]

def get_solver(E1,E2,B1,B2,n):

    L = get_L_matrix(E1, n)
    M, vars = get_M_matrix(E2, n)
    I = np.eye(n)
    A = (I-M).T @ np.linalg.inv(I - L).T
    J = get_J(B2,n)
    K = get_K(B1,n)
    JK = map_pairs(list(product(J,K)))
    JK_reduced = filter_pairs(JK, A)
    JK_reduced

    constant_indices = [
        (i+1, j+1)
        for i in range(A.rows)
        for j in range(A.cols)
        if not (A[i, j].free_symbols & set(vars))
    ]

    x = create_z3_variables(E2)
    B = create_random_B(E1, n)

    s = Solver()

    for (a,b),(c,d) in JK_reduced:

        if (a,b) in constant_indices:
            if (c,d) in constant_indices:
                return False
            else:
                s.add(create_equation(c, d, n, x, B)==0)
        elif (c,d) in constant_indices:
            s.add(create_equation(a,b,n,x,B)==0)
        else:    
            f = create_equation(a, b, n, x, B)
            g = create_equation(c, d, n, x, B)
            b = Bool(f"choose_{(a,b,c,d)}")
            s.add(If(b, f == 0, g == 0))

    if s.check() == sat:
        return True
    else:
        return False

def canonical(edges):
    """Convert edge list to hashable representation."""
    return tuple(sorted(edges))


def is_acyclic(edges):
    """Check whether directed edge set is a DAG."""
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return nx.is_directed_acyclic_graph(G)


def generate_neighbors(edges, n):
    """
    Generate all DAGs differing by one edge addition or removal.
    """
    edges = set(edges)
    neighbors = []

    for e in edges:
        new_edges = edges.copy()
        new_edges.remove(e)

        neighbors.append(new_edges)

    for u in range(1, n + 1):
        for v in range(1, n + 1):

            if u == v:
                continue

            if (u, v) in edges:
                continue

            new_edges = edges.copy()
            new_edges.add((u, v))

            if is_acyclic(new_edges):
                neighbors.append(new_edges)

    return neighbors


def find_equivalence_class_traversal(edges, confounding, n):
    # Searching for equivalent graphs by adding/removing edges
    # Fixing confounding
    start = set(edges)
    visited = {canonical(start)}
    result = [start]
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in generate_neighbors(current, n):
            key = canonical(neighbor)
            if key in visited:
                continue
            G1 = nx.DiGraph()
            G2 = nx.DiGraph()
            V = range(1,n+1)
            G1.add_nodes_from(V)
            G2.add_nodes_from(V)
            G1.add_edges_from(start)
            G2.add_edges_from(neighbor)
            if check_inclusion_full(G1, G2, confounding, confounding) and check_inclusion_full(G2, G1, confounding, confounding):
                visited.add(key)
                result.append(neighbor)
                queue.append(neighbor)
    return result

def enumerate_dags(n):
    vertices = range(1, n + 1)

    edges = [(u, v)
             for u in vertices
             for v in vertices
             if u != v]

    G = nx.DiGraph()
    G.add_nodes_from(vertices)

    def dfs(i):
        if i == len(edges):
            yield G.copy()
            return

        yield from dfs(i + 1)

        u, v = edges[i]
        if not nx.has_path(G, v, u):
            G.add_edge(u, v)
            yield from dfs(i + 1)
            G.remove_edge(u, v)

    yield from dfs(0)

def find_equivalent_graphs_exhaustive(E,B,n):
    # Exhaustive search fixing bidirected part
    # n should not be larger than 5
    print ("Confounding:")
    print (B)
    print ("---Edges---")
    G1 = nx.DiGraph()
    G1.add_nodes_from(range(1,n+1))
    G1.add_edges_from(E)
    for G in enumerate_dags(n):
        if check_inclusion_full(G1,G,B,B) and check_inclusion_full(G,G1,B,B):
            print (G.edges())


def find_equivalent_graphs_exhaustive_to_compare(E,B,n):
    # Exhaustive search fixing bidirected part
    # n should not be larger than 5
    G1 = nx.DiGraph()
    G1.add_nodes_from(range(1,n+1))
    G1.add_edges_from(E)
    result = []
    for G in enumerate_dags(n):
        if check_inclusion_full(G1,G,B,B) and check_inclusion_full(G,G1,B,B):
            result.append(set(G.edges()))

    return result
    