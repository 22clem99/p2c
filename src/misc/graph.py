class Graph:
    def __init__(self):
        self.nodes = dict()
        self.edges = list()

    def add_node(self, node, node_name):
        if self.nodes[node_name] != None:
            print(f"A node {node_name} already exit in the graph")
        self.nodes[node_name] = node

    def add_edge(self, src, dest):
        if self.nodes[src] == None:
            print(f"The node {src} doesn't exit in the graph")
            exit(2)
        if self.nodes[src] == None:
            print(f"The node {dest} doesn't exit in the graph")
            exit(2)

        self.edges.append((src, dest))

    def remove_node(self, node_name):
        try:
            del self.nodes[node_name]
        except KeyError:
            print(f"The node {node_name} doesn't exit in the graph and can not be remove")

        self.purge_all_edge_link_to_node(node_name)

    def remove_edge(self, src, dest):
        try:
            self.edges.remove((src, dest))
        except ValueError:
            print(f"The edge with {src=} and {dest=} doesn't exit in the graph and can not be remove")

    def purge_all_edge_link_to_node(self, node_name):
        new_edge_list = list()

        for edge in self.edges:
            if node_name in edge:
                new_edge_list.append(edge)

        self.edges = new_edge_list
