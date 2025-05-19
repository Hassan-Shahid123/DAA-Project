from social_network import create_social_network
from spreading_algo import run_simulation
from simulation import visualize_simulation
from analysis import plot_age_group_distribution, plot_simulation_summary, final_outcomes_by_age_group
import networkx as nx

# --- Take user input interactively ---
try:
    n = int(input("Enter number of individuals in the network (e.g., 250): "))
except ValueError:
    n = 250
    print("Invalid input, using default:", n)

try:
    vaccination_rate = float(input("Enter vaccination rate (0 to 1, e.g., 0.3): "))
except ValueError:
    vaccination_rate = 0.3
    print("Invalid input, using default:", vaccination_rate)

try:
    initial_infected_count = int(input("Enter number of initially infected individuals (e.g., 10): "))
except ValueError:
    initial_infected_count = 10
    print("Invalid input, using default:", initial_infected_count)

# --- Create the social network ---
G = create_social_network(n=n, vaccination_rate=vaccination_rate)

# --- Pick initial infected nodes ---
candidates = [node for node in G.nodes if 18 <= G.nodes[node]['age'] <= 49]
central_nodes = sorted(candidates, key=lambda n: G.degree(n), reverse=True)
initial_infected = central_nodes[:initial_infected_count]

# --- Run the simulation ---
status_history, infection_stats, transmission_history, all_infected = run_simulation(G, initial_infected)

# --- Analysis ---
plot_age_group_distribution(G)
final_outcomes_by_age_group(G)
plot_simulation_summary(infection_stats, all_infected)

# --- Visualize dynamic animation ---
pos = nx.spring_layout(G)
visualize_simulation(G, status_history, pos, initial_infected, transmission_history)
