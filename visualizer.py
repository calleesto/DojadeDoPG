import time
import plotly.graph_objects as go
from graph_builder import graph_nodes

def draw_graph(edge_limit=15000):
    start_time = time.perf_counter()
    edge_x = []
    edge_y = []

    edges_drawn = 0

    for node_id, node in graph_nodes.items():
        for edge in node.edges.values():
            if edges_drawn >= edge_limit:
                break

            A = edge.source
            B = edge.target

            edge_x.extend([A.lon, B.lon, None])
            edge_y.extend([A.lat, B.lat, None])

            edges_drawn += 1

        if edges_drawn >= edge_limit:
            break

    node_x = []
    node_y = []
    node_text = []

    for node_id, node in graph_nodes.items():
        node_x.append(node.lon)
        node_y.append(node.lat)
        node_text.append(node.name)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#445555'),
        hoverinfo='none',
        mode='lines'
    ))

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=False,
            color='#00ffcc',
            size=3,
            line_width=0
        )
    ))

    fig.update_layout(
        title="NeptuNet: Topology of Gdańsk Transit Network",
        title_font_size=18,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        plot_bgcolor='#050505',
        paper_bgcolor='#050505',
        font=dict(color='#00ffcc'),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    filename = "NeptuNet.html"
    fig.write_html(filename)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"draw_graph took {execution_time:.4f} seconds to finish.")