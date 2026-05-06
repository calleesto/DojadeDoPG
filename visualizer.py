import time
import plotly.graph_objects as go
from graph_models import TransitStop

DEFAULT_EDGE_LIMIT = 15_000

def draw_graph(graph_nodes: dict[str, TransitStop], edge_limit=DEFAULT_EDGE_LIMIT):
    start_time = time.perf_counter() # function timer

    edge_x, edge_y = [], []
    edge_mid_x, edge_mid_y, edge_text = [], [], []

    edges_drawn = 0

    for node_id, node in graph_nodes.items():
        for edge in node.edges.values():
            if edges_drawn >= edge_limit:
                break

            a = edge.source
            b = edge.target

            edge_x.extend([a.lon, b.lon, None])
            edge_y.extend([a.lat, b.lat, None])

            # calculate midpoint of edge
            mid_x = (a.lon + b.lon) / 2
            mid_y = (a.lat + b.lat) / 2
            edge_mid_x.append(mid_x)
            edge_mid_y.append(mid_y)

            # format transit time
            minutes = int(edge.weight // 60)
            seconds = int(edge.weight % 60)
            time_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
            #edge_text.append(time_str)

            hover_label = f"{a.name} ➔ {b.name}<br>Duration: {time_str}"
            edge_text.append(hover_label)

            edges_drawn += 1

        # to stop the outer loop as well when edge_limit is reached
        if edges_drawn >= edge_limit:
            break

    node_x, node_y, node_text = [], [], []

    for node_id, node in graph_nodes.items():
        node_x.append(node.lon)
        node_y.append(node.lat)
        node_text.append(node.name)



    # ===user interface===
    fig = go.Figure()

    # draw edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#445555'),
        hoverinfo='none',
        mode='lines'
    ))

    # draw transit time on edge hover
    fig.add_trace(go.Scatter(
        x=edge_mid_x, y=edge_mid_y,
        mode='markers',
        marker=dict(size=4, color='rgba(0,0,0,0)'),
        text=edge_text,
        hoverinfo='text'
    ))

    # draw nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',  # ensure hoverinfo is set to 'text' for displaying node names
        text=node_text,  # correctly link node_text to provide hover labels
        marker=dict(showscale=False, color='#00ffcc', size=3, line_width=0)
    ))

    # the rest
    fig.update_layout(
        #title="NeptuNet: Topology of Gdańsk Transit Network",
        #title_font_size=18,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        plot_bgcolor='#050505',
        paper_bgcolor='#050505',
        font=dict(color='#00ffcc'),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )


    end_time = time.perf_counter() # function timer
    print(f"draw_graph took {end_time - start_time:.4f} seconds to finish.")

    return fig