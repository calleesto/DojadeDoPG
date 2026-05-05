from graph_builder import get_or_build_graph
from visualizer import draw_graph

if __name__ == "__main__":
    FORCE_REBUILD = False
    nodes, total_edges = get_or_build_graph(force_build=FORCE_REBUILD)

    draw_graph(graph_nodes=nodes, edge_limit=total_edges)
