import matplotlib.pyplot as plt
import networkx as nx


class ConceptVisualizer:

    def create_graph(self, concept):

        concept = concept.strip()

        graph = nx.DiGraph()

        # Main concept
        graph.add_node(concept)

        # Main branches
        branches = {
            "Definition": [
                "Meaning",
                "Purpose"
            ],
            "Architecture": [
                "Components",
                "Layers",
                "Processing"
            ],
            "Working": [
                "Input",
                "Processing",
                "Output"
            ],
            "Advantages": [
                "Performance",
                "Efficiency"
            ],
            "Limitations": [
                "Computational Cost",
                "Data Requirements"
            ],
            "Applications": [
                "Research",
                "Industry",
                "Real World"
            ]
        }

        # Connect main concept to branches
        for branch in branches:

            graph.add_edge(
                concept,
                branch
            )

        # Connect branches to sub-concepts
        for branch, children in branches.items():

            for child in children:

                graph.add_edge(
                    branch,
                    child
                )

        # Create figure
        figure, ax = plt.subplots(
            figsize=(14, 10)
        )

        # Calculate positions
        positions = nx.spring_layout(
            graph,
            seed=42,
            k=1.5
        )

        # Draw edges
        nx.draw_networkx_edges(
            graph,
            positions,
            ax=ax,
            arrows=True,
            arrowsize=15
        )

        # Draw nodes
        nx.draw_networkx_nodes(
            graph,
            positions,
            ax=ax,
            node_size=2500
        )

        # Draw labels
        nx.draw_networkx_labels(
            graph,
            positions,
            ax=ax,
            font_size=9
        )

        # Title
        ax.set_title(
            "Concept Map: " + concept,
            fontsize=18
        )

        # Remove axes
        ax.axis("off")

        # Return figure to Streamlit
        return figure