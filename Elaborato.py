class Node:
    def __init__(self, name):
        """
        Inizializza un nodo con un nome e una tabella di routing vuota.
        """
        self.name = name
        self.routing_table = {name: (0, name)}  # Distanza a se stesso è 0

    def update_routing_table(self, neighbor, neighbor_table, adjacency_matrix):
        """
        Aggiorna la tabella di routing in base alle informazioni del vicino.
        """
        updated = False
        for dest, (neighbor_dist, _) in neighbor_table.items():
            # Ignora se stesso
            if dest == self.name:
                continue
            
            # Considera solo percorsi validi attraverso il vicino diretto
            if adjacency_matrix[ord(self.name) - ord('A')][ord(neighbor) - ord('A')] != float('inf'):
                new_distance = neighbor_dist + self.routing_table[neighbor][0]
                if dest not in self.routing_table or new_distance < self.routing_table[dest][0]:
                    self.routing_table[dest] = (new_distance, neighbor)
                    updated = True
        return updated


def print_routing_table(node):
    """
    Stampa la tabella di routing di un nodo.
    """
    print(f"Routing Table for {node.name}:")
    print("Destination\tDistance\tNext Hop")
    for dest, (distance, next_hop) in sorted(node.routing_table.items()):
        print(f"{dest}\t\t{distance}\t\t{next_hop}")
    print()


def simulate_network(nodes, adjacency_matrix):
    """
    Simula l'aggiornamento delle tabelle di routing nella rete.
    """
    stable = False
    iteration = 0
    while not stable:
        iteration += 1
        print(f"Iteration {iteration}:")
        stable = True
        for i, node in enumerate(nodes):
            for j, neighbor in enumerate(nodes):
                if adjacency_matrix[i][j] != float('inf'):  # Sono vicini
                    neighbor_name = neighbor.name
                    if neighbor_name in node.routing_table:
                        if node.update_routing_table(neighbor_name, neighbor.routing_table, adjacency_matrix):
                            stable = False
        # Stampa lo stato dopo ogni iterazione
        for node in nodes:
            print_routing_table(node)
        print("-" * 40)


def main():
    """
    Funzione principale per configurare la rete e avviare la simulazione.
    """
    # Creazione dei nodi
    node_A = Node('A')
    node_B = Node('B')
    node_C = Node('C')
    node_D = Node('D')

    nodes = [node_A, node_B, node_C, node_D]

    # Configurazione della matrice di adiacenza
    # float('inf') rappresenta l'assenza di collegamento diretto
    adjacency_matrix = [
        [0, 1, float('inf'), 4],  # A
        [1, 0, 2, float('inf')],  # B
        [float('inf'), 2, 0, float('inf')],  # C
        [4, float('inf'), float('inf'), 0]   # D
    ]

    # Inizializza le tabelle di routing dei nodi con i loro vicini diretti
    for i, node in enumerate(nodes):
        for j, cost in enumerate(adjacency_matrix[i]):
            if cost != float('inf') and i != j:
                node.routing_table[nodes[j].name] = (cost, nodes[j].name)

    # Stampa lo stato iniziale delle tabelle
    print("Initial state of routing tables:")
    for node in nodes:
        print_routing_table(node)
    print("-" * 40)

    # Simula l'aggiornamento delle tabelle di routing
    simulate_network(nodes, adjacency_matrix)


if __name__ == "__main__":
    main()
