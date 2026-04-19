# NeptuNet: GTFS to Graph Converter for AI

## Overview
This project processes raw General Transit Feed Specification (GTFS) data from the ZTM Gdańsk API and transforms it into a fully functional, directed graph structure. 

While not an AI model in itself, this tool performs the crucial **Data Engineering** step required to run advanced Artificial Intelligence and Graph Machine Learning algorithms on real-world urban transit networks.

## AI & Graph Theory Applications
The generated graph dataset is designed to be directly compatible with:
* **Search Algorithms:** Applying A* (A-star) or Dijkstra's algorithm for optimal route planning (using time as the edge weight and geographic coordinates for spatial heuristics).
* **Community Detection:** Unsupervised learning algorithms to automatically identify major transit hubs and transfer bottlenecks in Gdańsk.
* **Graph Neural Networks (GNNs):** Providing a foundational topological dataset for predictive modeling (e.g., predicting traffic load or delay propagation).

## Project Structure
The project uses an Object-Oriented approach to cleanly separate mathematical graph theory from the GTFS domain logic.

```text
📁 project_root/
├── 📄 downloader.py      # Automates downloading and extracting the latest GTFS ZIP
├── 📄 graph_models.py    # Contains the OOP class structures (Nodes & Edges)
├── 📄 main.py            # The main pipeline (loads nodes, builds edges)
├── 📄 .gitignore         # Prevents large GTFS text files from being pushed to Git
└── 📁 gtfs_data/         # (Ignored by Git) Local storage for extracted .txt files