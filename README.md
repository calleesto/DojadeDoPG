# NeptuNet: GTFS to Graph Converter for AI

## Overview
This project processes raw General Transit Feed Specification (GTFS) data from the ZTM Gdańsk API and transforms it into a fully functional, Time-Dependent directed graph structure. 

While not an AI model in itself, this tool performs the crucial **Data Engineering** step required to run advanced Artificial Intelligence and Graph Machine Learning algorithms on real-world urban transit networks.

## AI & Graph Theory Applications
The generated graph dataset is designed to be directly compatible with:
* **Search Algorithms:** Applying A* (A-star) or Dijkstra's algorithm for optimal route planning.
* **Time-Dependent Routing:** The graph stores dynamic schedules, allowing algorithms to calculate different optimal paths depending on the time of day (e.g., peak hours vs. night transit).
* **Graph Neural Networks (GNNs):** Providing a foundational topological dataset for predictive modeling.

## Core Architecture & Optimizations

### 1. Nodes (Vertices)
Nodes represent physical transit stops. 
* **Storage:** Stored in a Python `dictionary` (Hash Map) using `stop_id` as the key, ensuring $\mathcal{O}(1)$ lookup time.
* **Attributes:** `id`, `name`, `latitude`, `longitude`, `edges`.

### 2. Edges (Transit Connections)
Edges represent a direct, physical street segment between two consecutive stops. 
* **Deduplication:** The graph is optimized to represent physical topology. Multiple bus trips traversing the same street do not create redundant edges. The raw dataset of over 2 million trips is compressed into a clean network of unique street segments.
* **Dynamic Schedules:** Each edge contains a `schedules` array, storing every single departure and traversal time that occurs on that street. This enables Time-Dependent AI pathfinding.
* **Weight:** Defaults to the best-case (minimum) travel time on that segment.

### 3. Binary Caching System
Parsing raw GTFS `.txt` files is CPU-intensive. To improve Developer Experience (DX) and AI training loops, the project utilizes Python's `pickle` module (with `HIGHEST_PROTOCOL`). 
* The parsed graph is serialized into a binary `graph_cache.pkl` file.
* Load times are reduced from **~30 seconds** to **under 0.1 seconds**.
* A `force_build` flag is available for cache invalidation when fetching new API data.

## Visualization
The project includes a custom rendering engine built with **Plotly**. It plots the raw geographic coordinates of the nodes and edges onto a topological interface, allowing developers to visually verify the graph structure without relying on external map APIs.

## Setup & Usage

### Prerequisites
```bash
pip install pandas requests plotly