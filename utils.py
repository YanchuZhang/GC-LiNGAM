import networkx as nx
import matplotlib.pyplot as plt
import random
from itertools import combinations

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
    plt.show()
    return(is_vertex_cover(IG_cleaned.edges, unremovable_neighbors | unremovable))

def st_plot_auxiliary(G1, G2, B1, B2):
    V = list(G1.nodes())
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
    result = is_vertex_cover(
        IG_cleaned.edges,
        unremovable_neighbors | unremovable
    )
    return fig, result
    
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
    IG = induced_graph(V, B1, B2)
    IG_cleaned = IG_clean_up(IG, G1, G2, B2)
    unremovable = get_removable(V, G1, G2, B2)[1] & IG_cleaned.nodes
    unremovable_neighbors = neighbors_of_set(IG_cleaned, unremovable)
    return(is_vertex_cover(IG_cleaned.edges, unremovable_neighbors | unremovable))

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

def get_j(S, i):
    return {j for x, j in S if x == i}

def check_inclusion(G1,G2,B1,B2):
    V = list(G1.nodes())
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