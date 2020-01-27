import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import networkx as nx

# create dataframe using data scraped
df = pd.read_csv('data.tsv', '\t')

# create a graph using networkx
G = nx.Graph()

# loop over the rows of the dataframe
for index, row in df.iterrows():

    # get the business title, owner, agent information.
    # to differentiate between title, owner, agent nodes with
    #   the same name, append string with a flag.
    nodes = list(G.nodes)
    title = 't-' + row['Title']
    owner = row['Owner'] \
        if pd.isnull(row['Owner']) \
        else 'o-' + row['Owner']
    ra    = row['Registered_Agent'] \
        if pd.isnull(row['Registered_Agent']) i\
        else 'r-' + row['Registered_Agent']
    cra   = row['Commercial_Registered_Agent'] \
        if pd.isnull(row['Commercial_Registered_Agent']) \
        else 'c-' + row['Commercial_Registered_Agent']

    # add the node and edge to the graph
    # add t attribute for each node to add coloring when drawing
    # add weight attribute to edge to control the distance of nodes
    #   within a component
    if title not in nodes:
        G.add_node(title, t='title')
    if not pd.isnull(owner):
        if owner not in nodes:
            G.add_node(owner, t='owner')
        G.add_edge(title, owner, weight=0.1)
    if not pd.isnull(ra):
        if ra not in nodes:
            G.add_node(ra, t='ra')
        G.add_edge(title, ra, weight=0.1)
    if not pd.isnull(cra):
        if cra not in nodes:
            G.add_node(cra, t='cra')
        G.add_edge(title, cra, weight=0.1)

# create a list which contains the color for each type of node.
color_map = []
for i, d in G.nodes(data=True):
    if d['t'] == 'title':
        color_map.append('blue')
    if d['t'] == 'owner':
        color_map.append('green')
    if d['t'] == 'ra':
        color_map.append('yellow')
    if d['t'] == 'cra':
        color_map.append('red')

# create a legend
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Business',
                          markerfacecolor='b', markersize=15),
                   Line2D([0], [0], marker='o', color='w', label='Owner',
                          markerfacecolor='g', markersize=15),
                   Line2D([0], [0], marker='o', color='w', label='RA',
                          markerfacecolor='y', markersize=15),
                   Line2D([0], [0], marker='o', color='w', label='CRA',
                          markerfacecolor='r', markersize=15)]

# plot the network
f = plt.figure(figsize=(10,10))
f.add_subplot(111)
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos=pos, node_color=color_map, node_size=50, with_labels=False)
plt.legend(handles=legend_elements, loc=0)
plt.savefig('plot.png')
