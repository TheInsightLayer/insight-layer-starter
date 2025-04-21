import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from pyvis.network import Network
from streamlit.components.v1 import html

def display_placeholder_graph():
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    net.add_node(1, label="Insight A", color="blue")
    net.add_node(2, label="Insight B", color="green")
    net.add_edge(1, 2, title="Link")
    return net

def main():
    st.set_page_config(page_title="Insight Layer: Graph View", layout="wide")
    st.title("Insight Relationship Graph")

    st.markdown("""
    This page will visualize relationships between insights using an interactive graph. 
    Features to expect:
    - **Node-based visualization** of insights and their links.
    - **Filters** for themes, roles, and other metadata.
    - **Integration** with Neo4j for dynamic graph queries.
    """)

    with st.sidebar:
        st.subheader("Graph Options")
        node_size = st.slider("Node Size", 10, 100, 50)
        edge_weight = st.slider("Edge Weight", 1, 10, 5)
        st.info("Adjust these settings to customize the graph.")

    with st.spinner("Loading graph..."):
        graph = display_placeholder_graph()
        html(graph.generate_html())

if __name__ == "__main__":
    main()
