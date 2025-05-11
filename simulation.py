import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

status_colors = {
    'S': 'blue',       # Susceptible
    'I': 'red',        # Infected
    'R': 'green'       # Recovered
}

# def draw_network(G, step=None):
#     pos = nx.spring_layout(G, seed=42)  # fixed layout for consistent positioning
#
#     node_colors = [status_colors[G.nodes[n]['status']] for n in G.nodes()]
#
#     plt.figure(figsize=(10, 8))
#     nx.draw(
#         G, pos,
#         node_color=node_colors,
#         node_size=15,
#         with_labels=False,
#         edge_color='gray',
#         alpha=0.7
#     )
#     if step is not None:
#         plt.title(f"Network at Time Step {step}")
#     plt.axis('off')
#     plt.show()


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter


def visualize_simulation(G, infection_stats, pos, initial_infected):
    fig, ax = plt.subplots(figsize=(10, 8))

    status_colors = {
        'S': 'blue',
        'I': 'red',
        'R': 'green'
    }

    def update(frame):
        ax.clear()
        current_status = infection_stats[frame]

        # Build node color and size lists
        node_colors = []
        node_sizes = []
        node_border_colors = []
        for n in G.nodes():
            status = current_status[n]
            node_colors.append(status_colors[status])
            if n in initial_infected:
                node_border_colors.append('black')  # border for patient zeros
            else:
                node_border_colors.append('gray')

            # Adjust node size based on status
            if status == 'I':
                node_sizes.append(80)
            elif status == 'R':
                node_sizes.append(50)
            else:
                node_sizes.append(20)

        # Highlight transmission edges (edges between I and S at this step)
        transmission_edges = []
        for u, v in G.edges():
            if current_status[u] == 'I' and current_status[v] == 'S':
                transmission_edges.append((u, v))
            elif current_status[v] == 'I' and current_status[u] == 'S':
                transmission_edges.append((u, v))

        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.3, ax=ax, edge_color='lightgray')
        nx.draw_networkx_edges(G, pos, edgelist=transmission_edges, edge_color='red', width=1.5, ax=ax)

        # Draw nodes
        nx.draw_networkx_nodes(
            G, pos,
            node_color=node_colors,
            edgecolors=node_border_colors,
            node_size=node_sizes,
            ax=ax
        )

        ax.set_title(f"Time Step {frame}", fontsize=14)
        ax.axis("off")

        # Legend
        legend_elements = [
            mpatches.Patch(color='blue', label='Susceptible'),
            mpatches.Patch(color='red', label='Infected'),
            mpatches.Patch(color='green', label='Recovered'),
            mpatches.Patch(facecolor='white', edgecolor='black', label='Initial Infected'),
            mpatches.Patch(color='red', label='New Infection Edge')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=9)

    anim = animation.FuncAnimation(
        fig, update,
        frames=len(infection_stats),
        interval=800,
        repeat=False
    )

    anim.save("disease_spread.gif", writer=PillowWriter(fps=1))
    plt.show()


