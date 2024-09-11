from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = []
        self._edges = []
        self._graph = nx.DiGraph()
        self._idMap = {}

    def get_year(self):
        return DAO.get_year()

    def get_shapes(self, anno):
        return DAO.get_shapes(anno)

    def build_graph(self, anno, forma):
        self._nodes.clear()
        self._edges.clear()
        self._graph.clear()
        self._nodes = DAO.get_nodes(anno, forma)
        for node in self._nodes:
            self._idMap[node.id] = node
        self._graph.add_nodes_from(self._nodes)
        self._edges = DAO.get_edges(anno, forma, self._idMap)
        print(len(self._edges))
        for edge in self._edges:
            self._graph.add_edge(edge[0], edge[1], weight=abs(edge[0].longitude - edge[1].longitude))


    def get_archi_peso_maggiore(self):
        archi_ordinati = sorted(self._graph.edges(data=True), key=lambda edge: edge[2].get("weight"), reverse=True)
        return archi_ordinati[0:5]

    def get_num_nodes(self):
        return len(self._graph.nodes)

    def get_num_edges(self):
        return len(self._graph.edges)