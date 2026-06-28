import streamlit as st
import utils
import networkx as nx
import matplotlib.pyplot as plt
import random

st.title("Model Inclusion")

n = st.number_input("Enter number of nodes", value = 4)
G1 = nx.DiGraph()
G2 = nx.DiGraph()
V = range(1,n+1)
G1.add_nodes_from(V)
G2.add_nodes_from(V)

num_confounding = st.number_input("Enter number of bidirected edges", value = 1)
B1 = utils.random_confounding(n,num_confounding)
B2 = utils.random_confounding(n,num_confounding)
E1 = utils.random_dag(n,random.random()).edges()
E2 = utils.random_dag(n,random.random()).edges()

E1_in = st.text_input("Enter directed edges for G1", value = E1)
if E1_in:
    E1 = eval(E1_in)

E2_in = st.text_input("Enter directed edges for G2", value = E2)
if E2_in:
    E2 = eval(E2_in)

B1_in = st.text_input("Enter bidirected edges for G1", value = B1)
if B1_in:
    B1 = eval(B1_in)

B2_in = st.text_input("Enter bidirected edges for G2", value = B2)
if B2_in:
    B2 = eval(B2_in)

if st.button("Show auxiliary graph"):
    G1.add_edges_from(E1)
    G2.add_edges_from(E2)
    fig, is_trac = utils.st_plot_auxiliary(G1, G2, B1, B2)
    st.pyplot(fig)
    st.write("Is tractable:", is_trac)
    is_inc = utils.check_inclusion(G1,G2,B1,B2)
    st.write("G1 is included in G2:", is_inc)