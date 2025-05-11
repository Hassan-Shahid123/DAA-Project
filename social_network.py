import random

import networkx as nx


def assign_demographics(G):
    for node in G.nodes():
        age = random.choices(
            population=[random.randint(0, 17), random.randint(18, 49), random.randint(50, 64), random.randint(65, 90)],
            weights=[0.2, 0.5, 0.2, 0.1],  # More adults, fewer elderly/kids
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

        # Add small random variation to simulate health diversity
        susceptibility = min(1.0, max(0.0, base_sus + random.uniform(-0.05, 0.05)))

        # Set node attributes
        G.nodes[node]['age'] = age
        G.nodes[node]['status'] = 'S'
        G.nodes[node]['susceptibility'] = susceptibility

def create_social_network(n=250, k=6, p=0.1, infection_prob=0.05):
    G = nx.watts_strogatz_graph(n=n, k=k, p=p)
    assign_demographics(G)
    for u, v in G.edges():
        G[u][v]['transmission_prob'] = infection_prob
    return G
