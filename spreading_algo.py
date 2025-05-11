import matplotlib.pyplot as plt
import networkx as nx
from social_network import assign_demographics
import random
from simulation import visualize_simulation
import copy

def run_simulation(G, initial_infected, recovery_time=10, max_steps=100):
    status_history = []
    infection_stats = []

    for node in initial_infected:
        G.nodes[node]['status'] = 'I'
        G.nodes[node]['infected_since'] = 0

    for step in range(max_steps):
        new_infections = []
        recoveries = []

        for node in G.nodes():
            if G.nodes[node]['status'] == 'I':
                for neighbor in G.neighbors(node):
                    if G.nodes[neighbor]['status'] == 'S':
                        p = G[node][neighbor]['transmission_prob'] * G.nodes[neighbor]['susceptibility']
                        if random.random() < p:
                            new_infections.append(neighbor)
                G.nodes[node]['infected_since'] += 1
                if G.nodes[node]['infected_since'] >= recovery_time:
                    recoveries.append(node)

        for node in new_infections:
            G.nodes[node]['status'] = 'I'
            G.nodes[node]['infected_since'] = 0
        for node in recoveries:
            G.nodes[node]['status'] = 'R'

        snapshot = {n: G.nodes[n]['status'] for n in G.nodes()}
        status_history.append(copy.deepcopy(snapshot))

        S_count = sum(1 for n in G.nodes if G.nodes[n]['status'] == 'S')
        I_count = sum(1 for n in G.nodes if G.nodes[n]['status'] == 'I')
        R_count = sum(1 for n in G.nodes if G.nodes[n]['status'] == 'R')

        infection_stats.append({'step': step, 'S': S_count, 'I': I_count, 'R': R_count})

        if I_count == 0:
            print(f"Infection died out at step {step}")
            break

    return status_history, infection_stats


# steps = [s['step'] for s in infection_stats]
# S = [s['S'] for s in infection_stats]
# I = [s['I'] for s in infection_stats]
# R = [s['R'] for s in infection_stats]
#
# plt.plot(steps, S, label='Susceptible')
# plt.plot(steps, I, label='Infected')
# plt.plot(steps, R, label='Recovered')
# plt.xlabel('Time Step')
# plt.ylabel('Number of Individuals')
# plt.title('SIR Disease Spread Simulation')
# plt.legend()
# plt.grid()
# plt.show()
