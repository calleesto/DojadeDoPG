import pandas as pd
from graph_models import TransitStop, TransitConnection


# were using '{}' instead of '[]' because we want to be able to access the node by its id
# {} - dictionary/hash table
# [] - list/dynamic array

# key: stop_id (string)
# value: TransitStop object
graph_nodes = {}


def load_nodes():
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


def gtfs_time_to_seconds(time_str):
    h, m, s = map(int, str(time_str).split(':'))
    return h * 3600 + m * 60 + s


def load_edges():
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

                edge = TransitConnection(
                    source_node=graph_nodes[node_a_id],
                    target_node=graph_nodes[node_b_id],
                    weight=weight,
                    trip_id=trip_id,
                    route_type="unknown"
                )

                graph_nodes[node_a_id].edges.append(edge)



if __name__ == "__main__":
    load_nodes()
    load_edges()