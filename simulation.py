import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import networkx as nx

def visualize_simulation(G, infection_stats, pos, initial_infected, transmission_history):
    fig, ax = plt.subplots(figsize=(12, 10))

    status_colors = {
        'S': 'blue',
        'I': 'red',
        'R': 'green',
        'D': 'black'
    }

    def update(frame):
        ax.clear()
        current_status = infection_stats[frame]

        # Draw red edges for current transmissions
        active_edges = transmission_history[frame] if frame < len(transmission_history) else []
        nx.draw_networkx_edges(G, pos, edgelist=active_edges, edge_color='red', width=2, ax=ax)

        node_colors = []
        node_sizes = []
        node_border_colors = []

        for n in G.nodes():
            status = current_status[n]
            node_colors.append(status_colors.get(status, 'gray'))

            if status == 'I':
                node_sizes.append(300)
            elif status == 'R':
                node_sizes.append(250)
            elif status == 'D':
                node_sizes.append(180)
            else:  # Susceptible
                node_sizes.append(220)

            # Border color: black if initial infected, green if vaccinated, gray otherwise
            if n in initial_infected:
                node_border_colors.append('black')
            elif G.nodes[n].get('vaccinated', False):
                node_border_colors.append('green')
            else:
                node_border_colors.append('lightgray')

        # Draw light background edges
        nx.draw_networkx_edges(G, pos, alpha=0.03, edge_color='gray', ax=ax)

        # Draw nodes
        nx.draw_networkx_nodes(
            G, pos,
            node_color=node_colors,
            edgecolors=node_border_colors,
            node_size=node_sizes,
            linewidths=4,
            ax=ax
        )

        ax.set_title(f"Time Step {frame}", fontsize=14)
        ax.axis("off")

        # Updated legend
        legend_elements = [
            mpatches.Patch(color='blue', label='Susceptible'),
            mpatches.Patch(color='red', label='Infected'),
            mpatches.Patch(color='green', label='Recovered'),
            mpatches.Patch(color='black', label='Dead'),
            mpatches.Patch(facecolor='white', edgecolor='black', label='Initial Infected'),
            mpatches.Patch(facecolor='white', edgecolor='green', label='Vaccinated'),
            mpatches.Patch(facecolor='white', edgecolor='lightgray', label='Not Vaccinated')

        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=9)

    anim = animation.FuncAnimation(
        fig, update,
        frames=len(infection_stats),
        interval=700,
        repeat=False
    )

    anim.save("disease_spread.gif", writer=animation.PillowWriter(fps=1))
    plt.show()
