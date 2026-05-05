from dash import Dash, dcc, html
from graph_builder import get_or_build_graph
from visualizer import draw_graph

FORCE_REBUILD = False
nodes, total_edges = get_or_build_graph(force_build=FORCE_REBUILD)

app = Dash(__name__)


app.layout = html.Div(
    style={'backgroundColor': '#050505', 'height': '100vh', 'margin': '0', 'overflow': 'hidden'},
    children=[
        dcc.Graph(
            id='transit-graph',
            figure=draw_graph(graph_nodes=nodes, edge_limit=total_edges),
            style={'height': '100vh', 'width': '100vw'}
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)