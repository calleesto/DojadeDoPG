


from graph_builder import get_or_build_graph, edge_counter
from visualizer import draw_graph

if __name__ == "__main__":
    FORCE_REBUILD = False
    get_or_build_graph(force_build=FORCE_REBUILD)

    draw_graph(edge_limit=edge_counter)
