import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodes = []
        self._cammino_ottimo = []
        self._lunghezza_ottima = 0
        self.loadShapes()

    def get_years(self):
        return DAO.get_years()

    def get_shapes_year(self, year: int):
        return DAO.get_shapes_year(year)

    def create_graph(self, year: int, shape: str):
        self._grafo.clear()
        self._nodes = DAO.get_nodes(year, shape)
        self._grafo.add_nodes_from(self._nodes)

        # calcolo degli edges in modo programmatico
        for i in range(0, len(self._nodes) - 1):
            for j in range(i + 1, len(self._nodes)):
                if self._nodes[i].state == self._nodes[j].state and self._nodes[i].longitude < self._nodes[j].longitude:
                    weight = self._nodes[j].longitude - self._nodes[i].longitude
                    self._grafo.add_edge(self._nodes[i], self._nodes[j], weight= weight)

    def get_top_edges(self):
        sorted_edges = sorted(self._grafo.edges(data=True), key=lambda edge: edge[2].get('weight'), reverse=True)
        return sorted_edges[0:5]


    def get_nodes(self):
        return self._grafo.nodes()

    # def get_edges(self):
    #     return list(self._grafo.edges(data=True))

    def get_num_of_nodes(self):
        return self._grafo.number_of_nodes()

    def get_num_of_edges(self):
        return self._grafo.number_of_edges()

    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._lunghezza_ottima = 0

        for nodo in self._nodes:
            successivi_durata_crescente = self._calcola_successivi(nodo)
            self._calcola_cammino_ricorsivo([nodo], successivi_durata_crescente)
        return self._cammino_ottimo

    def _calcola_successivi(self, nodo):
        """
        Calcola il sottoinsieme dei successivi ad un nodo che hanno durata superiore a quella del nodo.
        """
        successivi = self._grafo.neighbors(nodo)
        successivi_ammissibili = []
        for s in successivi:
            if s.duration > nodo.duration:
                successivi_ammissibili.append(s)
        return successivi_ammissibili

    def _calcola_cammino_ricorsivo(self, parziale, successivi):
        if len(successivi) == 0:
            if len(parziale) > self._lunghezza_ottima:
                self._lunghezza_ottima = len(parziale)
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for nodo in successivi:
                if len(parziale) == 0 or parziale[-1].latitude < nodo.latitude:
                    parziale.append(nodo)
                    # nuovi successivi
                    nuovi_successivi = self._calcola_successivi(nodo)
                    # ricorsione
                    self._calcola_cammino_ricorsivo(parziale, nuovi_successivi)
                    # backtracking
                    parziale.pop()


    def loadShapes(self):
        self._listShapes = DAO.getAllShapes()

        return self._listShapes