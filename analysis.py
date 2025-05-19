def plot_sird(infection_stats):
    steps = [s['step'] for s in infection_stats]
    S = [s['S'] for s in infection_stats]
    I = [s['I'] for s in infection_stats]
    R = [s['R'] for s in infection_stats]
    D = [s['D'] for s in infection_stats]

    plt.figure(figsize=(10, 6))
    plt.plot(steps, S, label='Susceptible', color='blue')
    plt.plot(steps, I, label='Infected', color='red')
    plt.plot(steps, R, label='Recovered', color='green')
    plt.plot(steps, D, label='Deceased', color='black')
    plt.xlabel('Time Step')
    plt.ylabel('Number of Individuals')
    plt.title('SIRD Disease Spread Simulation')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("sird_plot.png")
    plt.show()


def print_simulation_statistics(infection_stats, all_infected):
    total_infected = len(all_infected)
    total_deaths = infection_stats[-1]['D']
    peak_infections, peak_step = max((s['I'], s['step']) for s in infection_stats)
    duration = infection_stats[-1]['step']

    print("\nSimulation Summary:")
    print(f"Total infected (cumulative): {total_infected}")
    print(f"Total deaths: {total_deaths}")
    print(f"Peak infections: {peak_infections} at step {peak_step}")
    print(f"Duration of outbreak: {duration} time steps")


import matplotlib.pyplot as plt

def plot_age_group_distribution(G):
    age_groups = {
        '0–17': 0,
        '18–49': 0,
        '50–64': 0,
        '65+': 0
    }

    for node in G.nodes:
        age = G.nodes[node]['age']
        if age <= 17:
            age_groups['0–17'] += 1
        elif age <= 49:
            age_groups['18–49'] += 1
        elif age <= 64:
            age_groups['50–64'] += 1
        else:
            age_groups['65+'] += 1

    labels = list(age_groups.keys())
    counts = list(age_groups.values())

    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Age Group Distribution")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig("age_distribution.png")
    plt.show()


import matplotlib.pyplot as plt


def final_outcomes_by_age_group(G):
    age_groups = {
        '0–17': {'Infected': 0, 'Recovered': 0, 'Deceased': 0},
        '18–49': {'Infected': 0, 'Recovered': 0, 'Deceased': 0},
        '50–64': {'Infected': 0, 'Recovered': 0, 'Deceased': 0},
        '65+': {'Infected': 0, 'Recovered': 0, 'Deceased': 0},
    }

    for node in G.nodes:
        age = G.nodes[node]['age']
        status = G.nodes[node]['status']

        if age <= 17:
            group = '0–17'
        elif age <= 49:
            group = '18–49'
        elif age <= 64:
            group = '50–64'
        else:
            group = '65+'

        if status in ['R', 'D', 'I']:
            age_groups[group]['Infected'] += 1
        if status == 'R':
            age_groups[group]['Recovered'] += 1
        if status == 'D':
            age_groups[group]['Deceased'] += 1

    # Plot grouped bar chart
    labels = list(age_groups.keys())
    infected = [age_groups[g]['Infected'] for g in labels]
    recovered = [age_groups[g]['Recovered'] for g in labels]
    deceased = [age_groups[g]['Deceased'] for g in labels]

    x = range(len(labels))
    width = 0.25

    plt.figure(figsize=(8, 6))
    plt.bar([i - width for i in x], infected, width=width, label='Infected', color='red')
    plt.bar(x, recovered, width=width, label='Recovered', color='green')
    plt.bar([i + width for i in x], deceased, width=width, label='Deceased', color='black')

    plt.xticks(x, labels)
    plt.xlabel("Age Group")
    plt.ylabel("Number of People")
    plt.title("Final Infection Outcomes by Age Group")
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("final_outcomes_by_age_group.png")
    plt.show()


import matplotlib.pyplot as plt


def plot_simulation_summary(infection_stats, all_infected):
    total_infected = len(all_infected)
    total_deaths = infection_stats[-1]['D']
    peak_infections, peak_step = max((s['I'], s['step']) for s in infection_stats)
    duration = infection_stats[-1]['step']

    labels = ['Total Infected', 'Total Deaths', 'Peak Infections', 'Duration (Steps)']
    values = [total_infected, total_deaths, peak_infections, duration]
    colors = ['orange', 'black', 'red', 'blue']

    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, values, color=colors)

    # Annotate values on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{int(height)}',
                 ha='center', va='bottom', fontsize=10)

    plt.title("Simulation Summary")
    plt.ylabel("Count")
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("simulation_summary.png")
    plt.show()
