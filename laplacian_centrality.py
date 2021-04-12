import networkx as nx
import itertools
import sys


def lap_cen(G):
    # network energy calculations
    lap_cen = {}

    acum_weight_sum = 0
    for node in G.nodes():
        node_weight_sum = 0
        for i in list(G.edges(data="weight", nbunch=node)):
            node_weight_sum += i[2]
        acum_weight_sum += node_weight_sum ** 2

    acum_edge_weight = 0
    for edge in G.edges(data="weight"):
        acum_edge_weight += 2 * (edge[2] ** 2)

    # network's laplacian energy (sum of nodes' weight sum to the power of two + 2 * (sum of every edge's weight to the power of two )  )
    net_lap_energy = acum_weight_sum + acum_edge_weight

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

        #       making up a dict of (node: node laplacian energy) pairs
        lap_cen.update(
            {n: (4 * clsd_wlk + 2 * opn_wlk_end + 2 * opn_wlk_mid) / net_lap_energy}
        )

    return lap_cen


with open(sys.argv[-1]) as f:
    G = nx.parse_edgelist(f, nodetype=int, data=(("weight", int),))

for edge in G.edges(data=True):
    if edge[2] == {}:
        edge[2].update({"weight": 1})

# set laplacian centrality as node attribute
nx.set_node_attributes(G, lap_cen(G), "lap_cen")
print(nx.classes.function.get_node_attributes(G, "lap_cen"))
