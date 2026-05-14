import time
import plotly.graph_objects as go
from graph_models import TransitStop

THRESHOLD = 0.05

def draw_graph(graph_nodes: dict[str, TransitStop], selected_time_sec: int = None):
    start_time = time.perf_counter()

    # 4 buckets for each type of coloring
    green_x, green_y = [], []  # faster than average
    red_x, red_y = [], []  # slower than average
    orange_x, orange_y = [], []  # average time
    grey_x, grey_y = [], []  # no busses

    time_window = 1800  #  1800s = 30min
    drawn_streets = set()

    for node_id, node in graph_nodes.items():
        for edge in node.edges.values():
            a = edge.source
            b = edge.target
            street_id = f"{a.id}-{b.id}"

            if street_id not in drawn_streets:
                drawn_streets.add(street_id)

                coords_x = [a.lon, b.lon, None]
                coords_y = [a.lat, b.lat, None]

                if selected_time_sec is None:
                    grey_x.extend(coords_x)
                    grey_y.extend(coords_y)
                    continue

                valid_trips = [
                    t for t in edge.schedules
                    if abs(t['departure'] - selected_time_sec) <= time_window
                ]

                if not valid_trips:
                    grey_x.extend(coords_x)
                    grey_y.extend(coords_y)
                else:
                    current_duration = sum(t['duration'] for t in valid_trips) / len(valid_trips)

                    threshold = THRESHOLD

                    if current_duration < edge.avg_weight * (1 - threshold):
                        green_x.extend(coords_x)
                        green_y.extend(coords_y)
                    elif current_duration > edge.avg_weight * (1 + threshold):
                        red_x.extend(coords_x)
                        red_y.extend(coords_y)
                    else:
                        orange_x.extend(coords_x)
                        orange_y.extend(coords_y)

    node_x, node_y, node_text = [], [], []
    for node in graph_nodes.values():
        node_x.append(node.lon)
        node_y.append(node.lat)
        node_text.append(node.name)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=grey_x, y=grey_y, line=dict(width=0.5, color='#333333'), mode='lines', hoverinfo='none'))
    fig.add_trace(
        go.Scatter(x=green_x, y=green_y, line=dict(width=1.5, color='#00ff44'), mode='lines', hoverinfo='none'))
    fig.add_trace(
        go.Scatter(x=orange_x, y=orange_y, line=dict(width=1.5, color='#ffa500'), mode='lines', hoverinfo='none'))
    fig.add_trace(go.Scatter(x=red_x, y=red_y, line=dict(width=2.5, color='#ff0033'), mode='lines', hoverinfo='none'))

    # Rysowanie węzłów na wierzchu
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y, mode='markers', hoverinfo='text', text=node_text,
        marker=dict(color='#00ffcc', size=3, line_width=0)
    ))

    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        plot_bgcolor='#050505',
        paper_bgcolor='#050505',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    end_time = time.perf_counter()
    print(f"draw_graph took {end_time - start_time:.4f}s to finish")

    return fig