import pandas as pd
from graph_models import TransitStop, TransitConnection
import time, os, pickle

# were using '{}' instead of '[]' because we want to be able to access the node by its id
# {} - dictionary/hash table
# [] - list/dynamic array

# key: stop_id (string)
# value: TransitStop object
graph_nodes = {}
edge_counter = 0
node_counter = 0
CACHE_FILE = "graph_cache.pkl"

def load_nodes():
    start_time = time.perf_counter()
    global node_counter
    stops_df = pd.read_csv('./gtfs_data/stops.txt')

    for index, row in stops_df.iterrows():
        stop_id = str(row['stop_id'])

        node = TransitStop(
            node_id=stop_id,
            name=row['stop_name'],
            lat=row['stop_lat'],
            lon=row['stop_lon']
        )

        graph_nodes[stop_id] = node
        node_counter += 1

    print(f"loaded {node_counter} nodes")
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"load_nodes took {execution_time:.4f} seconds to finish.")

def gtfs_time_to_seconds(time_str):
    h, m, s = map(int, str(time_str).split(':'))
    return h * 3600 + m * 60 + s


def load_edges():
    start_time = time.perf_counter()
    global edge_counter

    df = pd.read_csv('./gtfs_data/stop_times.txt')
    df = df.sort_values(by=['trip_id', 'stop_sequence'])
    grouped = df.groupby('trip_id')

    for trip_id, group in grouped:
        stops_in_trip = group.to_dict('records')

        for i in range(len(stops_in_trip) - 1):
            stop_a_data = stops_in_trip[i]
            stop_b_data = stops_in_trip[i + 1]

            node_a_id = str(stop_a_data['stop_id'])
            node_b_id = str(stop_b_data['stop_id'])

            if node_a_id in graph_nodes and node_b_id in graph_nodes:
                time_a = gtfs_time_to_seconds(stop_a_data['departure_time'])
                time_b = gtfs_time_to_seconds(stop_b_data['arrival_time'])
                weight = time_b - time_a

                trip_info = {
                    'departure': time_a,
                    'duration': weight,
                    'trip_id': trip_id
                }

                existing = graph_nodes[node_a_id].edges.get(node_b_id)

                if existing is None:
                    edge = TransitConnection(
                        source_node=graph_nodes[node_a_id],
                        target_node=graph_nodes[node_b_id],
                        weight=weight,
                        trip_id=trip_id,
                        route_type="unknown"
                    )
                    edge.schedules.append(trip_info)

                    graph_nodes[node_a_id].edges[node_b_id] = edge
                    edge_counter += 1
                else:
                    existing.schedules.append(trip_info)

                    if weight < existing.weight:
                        existing.weight = weight

    print(f"loaded {edge_counter} edges")
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"load_edges took {execution_time:.4f} seconds to finish.")


def get_or_build_graph(force_build = False):
    global graph_nodes
    global edge_counter
    global node_counter

    if force_build or not os.path.exists(CACHE_FILE):
        if force_build:
            print("rebuild flag set to TRUE. forcing rebuild")
        else:
            print("cache empty")
        graph_nodes.clear()

        load_nodes()
        load_edges()

        # wb stands for write binary
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump((graph_nodes, node_counter, edge_counter), f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        print("cache contains graph. loading from cache...")
        # rb stands for read binary
        with open(CACHE_FILE, 'rb') as f:
            graph_nodes, node_counter, edge_counter = pickle.load(f)
        print(f"loaded {edge_counter} edges and {node_counter} nodes")

    return graph_nodes, edge_counter

