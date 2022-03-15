import networkx as nx
import itertools
import sys


def calculate_centrality(G):
    # network energy calculations
    laplacian_centrality = {}

    cumulative_weight_sum = 0
    for node in G.nodes():
        node_weight_sum = 0
        for i in list(G.edges(data="weight", nbunch=node)):
            node_weight_sum += i[2]
        cumulative_weight_sum += node_weight_sum ** 2

    cumulative_edge_weight = 0
    for edge in G.edges(data="weight"):
        cumulative_edge_weight += 2 * (edge[2] ** 2)

    # network's laplacian energy (sum of nodes' weight sum to the power of two + 2 * (sum of every edge's weight to the power of two ) )
    net_lap_energy = cumulative_weight_sum + cumulative_edge_weight

    
    # calculating walks and centrality for each node
    for n in G.nodes():

        clsd_wlk = 0
        for i in list(G.edges(data="weight", nbunch=n)):
            clsd_wlk += i[2] ** 2

        opn_wlk_mid = 0
        for i, j in itertools.combinations(
            [i[2] for i in G.edges(data="weight", nbunch=n)], 2
        ):
            opn_wlk_mid += i * j

        opn_wlk_end = 0
        for i in G.edges(data="weight", nbunch=n):
            for j in G.edges(data="weight", nbunch=i[1]):
                if j[1] != i[0]:
                    opn_wlk_end += i[2] * j[2]

        # making up a dict of (node: node laplacian energy) pairs
        laplacian_centrality.update(
            {n: (4 * clsd_wlk + 2 * opn_wlk_end + 2 * opn_wlk_mid) / net_lap_energy}
        )

    return laplacian_centrality


with open(sys.argv[-1]) as f:
    G = nx.parse_edgelist(f, nodetype=int, data=(("weight", int),))

for edge in G.edges(data=True):
    if edge[2] == {}:
        edge[2].update({"weight": 1})

# set laplacian centrality as node attribute
nx.set_node_attributes(G, calculate_centrality(G), "lap_cen")
print(nx.classes.function.get_node_attributes(G, "lap_cen"))
