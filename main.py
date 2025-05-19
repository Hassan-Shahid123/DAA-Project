from social_network import create_social_network
from spreading_algo import run_simulation
from simulation import visualize_simulation
from analysis import plot_age_group_distribution, plot_simulation_summary
import networkx as nx
from analysis import final_outcomes_by_age_group

# Build the graph
G = create_social_network(vaccination_rate=0.3)  # 30% vaccinated

# Pick patient zeros
# More realistic: Infect high-degree centrality nodes who are adults
candidates = [n for n in G.nodes if 18 <= G.nodes[n]['age'] <= 49]
central_nodes = sorted(candidates, key=lambda n: G.degree(n), reverse=True)
initial_infected = central_nodes[:10]


# Run the simulation
status_history, infection_stats, transmission_history, all_infected = run_simulation(G, initial_infected)
plot_age_group_distribution(G)
final_outcomes_by_age_group(G)
plot_simulation_summary(infection_stats, all_infected)

# Visualize
pos = nx.spring_layout(G)
visualize_simulation(G, status_history, pos, initial_infected, transmission_history)
