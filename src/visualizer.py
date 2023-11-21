import networkx as nx
import matplotlib.pyplot as plt
from topo_generator import get_optimal_connections


def generate_connected_network(n, k):
    G = nx.Graph()

    # Add nodes to the graph
    G.add_nodes_from(range(n))

    # Connect each node to k other nodes
    for node, connections in enumerate(get_optimal_connections(n, k)):
        G.add_edges_from([(node, other_node) for other_node in connections])

    return G


def main():
    # Example usage

    n = 5  # Number of nodes
    k = 3  # Number of connections per node

    graph = generate_connected_network(n, k)

    # Print the edges of the graph
    print("Edges:")
    for edge in graph.edges():
        print(edge)

    # Visualize the graph
    # layouts = tuple(l for l in dir(nx) if l.endswith("layout") and l != "layout")
    # layouts = ("circular_layout", *(("planar_layout",) if k < 4 else ()), "fruchterman_reingold_layout")
    layouts = ("circular_layout",)
    for layout in layouts:
        if layout.startswith("bipartite"):
            pos = nx.bipartite_layout(graph, graph.nodes)
        elif layout.startswith("kamada") or layout.startswith("multipartite") or layout.startswith("rescale"):
            continue
        else:
            pos = getattr(nx, layout)(graph)
        print(layout)
        nx.draw(
            graph,
            pos,
            label=layout,
            with_labels=True,
            font_weight="bold",
            node_size=700,
            node_color="skyblue",
            font_size=8,
            font_color="black",
            edge_color="gray",
            linewidths=1,
            alpha=0.7,
        )
        plt.title = layout
        plt.show()


if __name__ == "__main__":
    main()
