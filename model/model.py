import copy
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMap = {}
        for v in self._nodes:
            self._idMap[v.object_id] = v
        self._bestPath = []
        self._bestCost = 0


    def getOptPath(self, source, lun):
        self._bestPath = []
        self._bestCost = 0

        parziale = [source]

        for n in self._graph.neighbors(source):
            if parziale[-1].classification == n.classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()

        return self._bestPath, self._bestCost


    def _ricorsione(self, parziale, lun):
        if len(parziale) == lun:
            # allora parziale ha la lunghezza desiderata, quindi verifico se è soluzione
            # migliore ed in ogni caso esco (CONDIZIONE TERMINALE)
            if self.costo(parziale) > self._bestCost:
                self._bestCost = self.costo(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return

        else: # se arrivo qui, allora parziale può acnora ammettere altri nodi (CONDIZIONE RICORSIVA)
            for n in self._graph.neighbors(parziale[-1]):
                if parziale[-1].classification == n.classification and n not in parziale:
                    parziale.append(n)
                    self._ricorsione(parziale, lun)
                    parziale.pop()



    def costo(self, listObjects):
        totCosto = 0
        for i in range(0, len(listObjects)-1): # numero archi
            totCosto += self._graph[listObjects[i]][listObjects[i+1]]["weight"]
        return totCosto


    def getInfoConnessa(self, idInput):
        """
        Identifica la componente connessa che contiene
        idInput e ne restituisce la dimensione.
        """
        if not self.hasNode(idInput):
            return None
        source = self._idMap[idInput]

        #Modo 1: conto i successori
        succ = nx.dfs_successors(self._graph, source)
        res = []
        for s in succ:
            res.append(s)
        print("Size connessa con nodo 1: ", len(succ.values()))

        #Modo 2: conto i predecessori
        pred = nx.dfs_predecessors(self._graph, source)
        print("Size connessa con nodo 2: ", len(pred.values()))

        #Modo 3: conto i nodi dell'albero di visita
        dfsTree = nx.dfs_tree(self._graph, source)
        print("Size connessa con nodo 3: ", len(dfsTree.nodes()))

        #Modo 4: uso il metodo nodes_connected_components di networkx
        conn = nx.node_connected_component(self._graph, source)
        print("Size connessa con nodo 4: ", len(conn))

        return len(conn)

    def hasNode(self, idInput):
        #return self._idMap[idInput] in self._graph
        return idInput in self._idMap

    def buildGraph(self):
        self._graph.add_nodes_from(self._nodes)
        self.addAllEdges()

    def addEdgesV1(self):
        """Metodo ottimo per grafi con pochi nodi, nel nostro caso
        ci vorrebbe tantissimo ---> sotto lo scriviamo in un modo
        migliore per il nostro caso."""
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getPeso(u,v)
                if peso != None:
                    self._graph.add_edge(u, v, weight=peso)

    def addAllEdges(self):
        """Lo facciamo direttamente in buildGraph di solito."""
        allEdges = DAO.getAllArchi(self._idMap)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)

    def addEdgesV2(self):
        pass

    def getNumNodes(self):
        return len(self._graph.nodes())

    def getNumEdges(self):
        return len(self._graph.edges())

    def getIdMap(self):
        return self._idMap

    def getObjectFromId(self, id):
        return self._idMap[id]