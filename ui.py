import streamlit as st
from utils import *
import networkx as nx
import matplotlib.pyplot as plt
import random

st.title("Check Model Inclusion (If M(G1) is in M(G2)")

n = st.number_input("Enter Number of Nodes", value = 3)

G1 = nx.DiGraph()
G2 = nx.DiGraph()

V = range(1,n+1)
G1.add_nodes_from(V)
G2.add_nodes_from(V)

E1_in = st.text_input("Enter Directed Edges for G1", value = "[(1,2),(2,3)]")
if E1_in:
    E1 = eval(E1_in)

E2_in = st.text_input("Enter Directed Edges for G2", value = "[(1,2),(1,3)]")
if E2_in:
    E2 = eval(E2_in)

B1_in = st.text_input("Enter Bidirected Edges for G1", value = "[2,3]")
if B1_in:
    B1 = eval(B1_in)

B2_in = st.text_input("Enter Bidirected Edges for G2", value = "[2,3]")
if B2_in:
    B2 = eval(B2_in)

G1.add_edges_from(E1)
G2.add_edges_from(E2)

if st.button("Show Auxilary and Reduced Graph"):
    fig = st_plot_auxiliary(G1, G2, B1, B2)
    st.pyplot(fig)
    fig2 = st_plot_reduced(G1, G2, B1, B2)
    st.pyplot(fig2)

if st.button("Check Model Inclusion"):
    if is_finished(G1,G2,B1,B2):
        st.write("NO Exhaustive Search Required")
        res = check_inclusion_full(G1,G2,B1,B2)
        st.write("M(G1) is in M(G2)", res)
    else:
        st.write("Require Exhaustive Search:")
        if st.button("Search!"):
            IG = induced_graph(V, B1, B2)
            IG_cleaned = IG_clean_up(IG, G1, G2, B2)
            unremovable = get_removable(V, G1, G2, B2)[1] & IG_cleaned.nodes
            unremovable_neighbors = neighbors_of_set(IG_cleaned, unremovable)
            remain = IG_cleaned.nodes - unremovable - unremovable_neighbors
            IG_remain = IG_cleaned.subgraph(remain).copy()
            IG_remain.remove_nodes_from(list(nx.isolates(IG_remain)))
            P = powerset(IG_remain.nodes())
            covers = inclusive_minimal_covers(IG_remain,P)
            st.write("All Candidate Covers", covers)
            res2 = check_inclusion_full(G1,G2,B1,B2)
            st.write("M(G1) is in M(G2)", res2)

    