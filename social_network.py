import random

import networkx as nx


def assign_demographics(G, vaccinated_nodes=None):
    if vaccinated_nodes is None:
        vaccinated_nodes = set()

    for node in G.nodes():
        age = random.choices(
            population=[random.randint(0, 17), random.randint(18, 49), random.randint(50, 64), random.randint(65, 90)],
            weights=[0.2, 0.5, 0.2, 0.1],
            k=1
        )[0]

        # Assign susceptibility based on age group
        if age <= 17:
            base_sus = 0.3
        elif age <= 49:
            base_sus = 0.6
        elif age <= 64:
            base_sus = 0.8
        else:
            base_sus = 0.95

        # Add small random variation
        susceptibility = min(1.0, max(0.0, base_sus + random.uniform(-0.05, 0.05)))

        # Vaccination reduces susceptibility
        is_vaccinated = node in vaccinated_nodes
        if is_vaccinated:
            susceptibility *= 0.1  # 90% effective
        G.nodes[node]['vaccinated'] = is_vaccinated

        G.nodes[node]['age'] = age
        G.nodes[node]['status'] = 'S'
        G.nodes[node]['susceptibility'] = susceptibility

def mark_super_spreaders(G, fraction=0.05, multiplier=2.0):
    # Use degree centrality or betweenness
    centrality = nx.degree_centrality(G)
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    top_k = int(len(G) * fraction)

    for i, (node, _) in enumerate(sorted_nodes):
        if i < top_k:
            G.nodes[node]['super_spreader'] = True
            G.nodes[node]['spread_multiplier'] = multiplier
        else:
            G.nodes[node]['super_spreader'] = False
            G.nodes[node]['spread_multiplier'] = 1.0



def create_social_network(infection_prob=0.1, vaccination_rate=0.3):
    G = nx.barabasi_albert_graph(n=250, m=3)

    # Randomly pick vaccinated nodes
    num_vaccinated = int(len(G.nodes) * vaccination_rate)
    vaccinated_nodes = set(random.sample(list(G.nodes), num_vaccinated))

    assign_demographics(G, vaccinated_nodes)
    mark_super_spreaders(G)

    for u, v in G.edges():
        G[u][v]['transmission_prob'] = infection_prob

    return G
