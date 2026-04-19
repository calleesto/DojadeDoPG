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

    print(f"successfully loaded \033[1m{len(graph_nodes)}\033[0m stops into the graph")


if __name__ == "__main__":
    load_nodes()

    # testing the dicitonary
    sample_id = list(graph_nodes.keys())[0]
    sample_node = graph_nodes[sample_id]
    print(f"\ntest node id: {sample_node.id}\nname: {sample_node.name}\ncoordinates: ({sample_node.lat}, {sample_node.lon})")