import pandas as pd
substations_df = pd.read_csv('substations.csv')
import networkx as nx 
import matplotlib.pyplot as plt 
G = nx.Graph() 

for index, row in substations_df.iterrows():
    G.add_node(row['Substation ID'], region=row['Region'], voltage=row['Voltage (kV)'],latitude=row['Latitude'],longitude=row['Longitude'],capacity=row['Capacity (MVA)'])
print(G.number_of_nodes())

lines_df = pd.read_csv('lines.csv')
for index, row in lines_df.iterrows():
    G.add_edge(row['Source Substation ID'], row['Destination Substation ID'],length=row['Length (km)'],capacity=row['Capacity (MVA)'])
print(G.number_of_edges())

degree_centrality = nx.degree_centrality(G)
#sorts the first 5 pairs in descending
sorted_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
print(sorted_centrality[:5])
#betweenness
betweenness_centrality = nx.betweenness_centrality(G)
#closeness
closeness_centrality = nx.closeness_centrality(G)
#pagerank
pagerank = nx.pagerank(G)

def top_5(centrality_dict, label):
    sorted_items = sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)
    print(f"{label}: {sorted_items[:5]}")

top_5(degree_centrality, "Degree")
top_5(betweenness_centrality, "Betweenness")
top_5(closeness_centrality, "Closeness")
top_5(pagerank, "PageRank")

components = list(nx.connected_components(G))
print(f"Number of components: {len(components)}")
print([len(c) for c in components])
largest_component = max(nx.connected_components(G), key=len)
G_main = G.subgraph(largest_component)

#diameter and average path length 
diameter = nx.diameter(G_main)
avg_path_length = nx.average_shortest_path_length(G_main)
print(f"Diameter: {diameter}")
print(f"Average path length: {avg_path_length}")

avg_clustering = nx.average_clustering(G_main)
print(f"Average clustering coefficient: {avg_clustering}")

#community detection using Louvain method 
from networkx.algorithms.community import louvain_communities
communities = louvain_communities(G_main)
print(f"Number of communities: {len(communities)}")
for i, community in enumerate(communities):
    print(f"Community {i}: {len(community)} substations")

#bridge lines 
bridges = list(nx.bridges(G_main))
print(f"Number of bridge lines: {len(bridges)}")
print(bridges)

#measuring network efficiency
efficiency = nx.global_efficiency(G)
print(f"Global efficiency: {efficiency}")