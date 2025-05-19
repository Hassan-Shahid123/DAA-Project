import random
from analysis import plot_sird
from analysis import print_simulation_statistics
import copy

def run_simulation(
        G, initial_infected,
        recovery_time=10,
        death_prob_base=0.01,
        max_steps=100,
        quarantine_enabled=True,
        quarantine_start_threshold=40,
        quarantine_delay=7,
        quarantine_compliance_rate=0.8,
        quarantine_effectiveness=0.7
):
    status_history = []
    infection_stats = []
    transmission_history = []

    # Initialize nodes
    for node in G.nodes():
        G.nodes[node]['infected_since'] = None  # Not infected yet
        G.nodes[node]['quarantine_compliant'] = random.random() < quarantine_compliance_rate

    # Infect initial nodes
    for node in initial_infected:
        G.nodes[node]['status'] = 'I'
        G.nodes[node]['infected_since'] = 0

    all_infected = set(initial_infected)
    quarantine_active = False

    for step in range(max_steps):
        new_infections = []
        recoveries = []
        deaths = []

        for node in G.nodes():
            if G.nodes[node]['status'] == 'I':
                if G.nodes[node]['infected_since'] is None:
                    G.nodes[node]['infected_since'] = 0
                G.nodes[node]['infected_since'] += 1

                is_quarantined = (
                    quarantine_enabled and
                    quarantine_active and
                    G.nodes[node]['infected_since'] >= quarantine_delay and
                    G.nodes[node]['quarantine_compliant']
                )

                for neighbor in G.neighbors(node):
                    if G.nodes[neighbor]['status'] == 'S':
                        multiplier = G.nodes[node].get('spread_multiplier', 1.0)
                        p = G[node][neighbor]['transmission_prob'] * G.nodes[neighbor]['susceptibility'] * multiplier

                        if is_quarantined:
                            p *= (1 - quarantine_effectiveness)

                        if random.random() < p:
                            new_infections.append(neighbor)

                # Check for recovery or death
                if G.nodes[node]['infected_since'] >= recovery_time:
                    age = G.nodes[node]['age']
                    if age <= 17:
                        death_prob = 0.1
                    elif age <= 49:
                        death_prob = 0.2
                    elif age <= 64:
                        death_prob = 0.3
                    else:
                        death_prob = 0.5

                    if random.random() < death_prob:
                        deaths.append(node)
                    else:
                        recoveries.append(node)

        # Apply state changes
        for node in new_infections:
            G.nodes[node]['status'] = 'I'
            G.nodes[node]['infected_since'] = 0
            all_infected.add(node)
        for node in recoveries:
            G.nodes[node]['status'] = 'R'
        for node in deaths:
            G.nodes[node]['status'] = 'D'

        # Activate quarantine if threshold is reached
        if not quarantine_active and len(all_infected) >= quarantine_start_threshold:
            print(f"\n[Step {step}] Quarantine policy activated due to rising infections.")
            quarantine_active = True

        # Save snapshot
        snapshot = {n: G.nodes[n]['status'] for n in G.nodes()}
        status_history.append(copy.deepcopy(snapshot))

        # Save transmission edges
        transmission_edges = [(src, tgt) for src in G.nodes() if G.nodes[src]['status'] == 'I'
                              for tgt in G.neighbors(src) if tgt in new_infections]
        transmission_history.append(transmission_edges)

        # Count statuses
        S_count = sum(1 for n in G.nodes if G.nodes[n]['status'] == 'S')
        I_count = sum(1 for n in G.nodes if G.nodes[n]['status'] == 'I')
        R_count = sum(1 for n in G.nodes if G.nodes[n]['status'] == 'R')
        D_count = sum(1 for n in G.nodes if G.nodes[n]['status'] == 'D')

        infection_stats.append({'step': step, 'S': S_count, 'I': I_count, 'R': R_count, 'D': D_count})

        if I_count == 0:
            print(f"\nInfection died out at step {step}.")
            break

    plot_sird(infection_stats)
    print_simulation_statistics(infection_stats, all_infected)

    return status_history, infection_stats, transmission_history, all_infected
