"""
File name: HCUF_module.py
Author: Daniele La Prova, Lorenzo Mei, Mihai Jianu
Python version: 3.x

Modulo contenente la definizione di hasCycleUF e delle sue funzioni e classi
ausiliarie.
Tale modulo è progettato per lavorare su grafi rappresentati come matrici di 
adiacienza.
"""

from unionFind.quickFind import *
#from unionFind.quickUnion import *
from Graph.graph.Graph_AdjacencyMatrix import *

class CustomQFB(QuickFindBalanced):
    """
    Versione custom della QFB, implementa il metodo findNode.
    """

    def findNode(self, e):
        """
        @param e: valore dell'elemento cercato
        @return UFB node, None if not found

        Dato un elemento come input, restituisce il nodo che lo contiene tra tutti
        i nodi presenti nella struttura unionFind.
        Se l'elemento passato proviene da un nodo di un grafo si evitano ambiguità,
        dato che ogni nodo possiede un ID unico.
        """
        touchedRoots = []
        for i in self.nodes:
            currentRoot = self.findRoot(i)
            if currentRoot not in touchedRoots:
                for son in currentRoot.sons:
                    if son.elem == e:
                        return son
                touchedRoots.append(currentRoot)
        return None

def edgeGenerator(G, maxTail, maxHead):
    """
    @param G: Graph
    @param maxTail: int, maximum range of sources
    @param maxHead: int, maximum range of destinations
    @return iterable
    
    Genera un iterabile che scorre gli archi di G t.c. tail, head <= maxTail, maxHead
    """
    
    for src in range(maxTail + 1):
            for dst in range(maxHead + 1):
                if G.adj[src][dst] is not None and G.adj[src][dst] != GraphAdjacencyMatrix.EMPTY and src != dst:
                    yield Edge(src, dst, G.adj[src][dst])

def hasCycleUF(G, debug=False):
    """
    @param G: Graph (as adjacency matrix)
    @return bool

    Verifica se nel grafo G è presente almeno un ciclo, sfruttando la struttura dati
    UnionFind e un iterator per scandirne tutti gli archi.

    procedure hasCycleUF(Graph G) → bool
        uf ← UnionFind
        for all unvisited (u, v) ∈ E(G) do
            if uf.find(u) == uf.find(v) then cycle detected
            else uf.union(u, v)
        return no cycle present

    """ 
    
    #uf = QuickUnionBalanced
    uf = CustomQFB()
    exit = False
    previousTail = 0
    edges = edgeGenerator(G, len(G.adj) - 1, len(G.adj) - 1)

    while not exit:
        try:
            if debug == True:
                print(f"previous tail was {previousTail}")
            
            currentEdge = next(edges)
            if debug == True:
                print(f"current edge is {currentEdge}")

            if uf.findNode(currentEdge.tail) == None:   # se gli elementi non appartengono a nessun nodo, vengono creati nuovi set con tali elementi all'interno (uno per elemento)
                uf.makeSet(currentEdge.tail)

            if uf.findNode(currentEdge.head) == None:    
                uf.makeSet(currentEdge.head)

            if debug == True:
                uf.print()

            tailNode, headNode = uf.findNode(currentEdge.tail), uf.findNode(currentEdge.head)   # trova il nodo nella uf contenente tali elementi
            if debug == True:
                print(f"tailNode is {tailNode}, headNode is {headNode}")
            
            if not currentEdge.tail > previousTail and uf.find(tailNode) == uf.find(headNode):
                return True
            else:
                uf.union(uf.findRoot(tailNode), uf.findRoot(headNode))
                if debug == True:
                    print(f"made an Union!")
                    uf.print()
                previousTail = currentEdge.tail # necessario per evitare di esplorare lo stesso arco in entrambi i sensi

        except StopIteration:
            if debug == True:
                print("iteration terminated, exiting ...")
            exit = True
                    
    return False
