from social_network import create_social_network
from spreading_algo import run_simulation
from simulation import visualize_simulation
import networkx as nx
import random

# Build the graph
G = create_social_network()

# Pick patient zeros
initial_infected = random.sample(list(G.nodes), 10)

# Run the simulation
status_history, infection_stats = run_simulation(G, initial_infected)

# Visualize
pos = nx.spring_layout(G, seed=42)
visualize_simulation(G, status_history, pos, initial_infected)