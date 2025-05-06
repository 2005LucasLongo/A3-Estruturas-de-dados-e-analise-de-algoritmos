import networkx as nx
import heapq

class GrafoNetworkX:
    """
    Representa um grafo não direcionado onde os vértices são cidades e as arestas representam estradas com distâncias associadas.
    """
    def __init__(self):
        """
        Inicializa um grafo vazio utilizando NetworkX.
        """
        self.grafo = nx.Graph()  # Grafo não direcionado

    def adicionar_aresta(self, origem, destino, distancia):
        """
        Adiciona uma aresta bidirecional entre duas cidades com uma distância específica.
        
        Args:
            origem (str): Cidade de origem.
            destino (str): Cidade de destino.
            distancia (float): Distância entre origem e destino.
        """
        self.grafo.add_edge(origem, destino, weight=distancia)

    def dijkstra(self, origem):
        """
        Executa o algoritmo de Dijkstra para encontrar o menor caminho de uma cidade origem até todas as outras.

        Args:
            origem (str): Cidade de origem.

        Returns:
            dict: Mapeamento de cidades para suas menores distâncias desde a origem.
            dict: Mapeamento de cada cidade para seu antecessor no caminho mais curto.
        """
        # Usando o algoritmo de Dijkstra do NetworkX
        distancias, anterior = nx.single_source_dijkstra(self.grafo, origem)
        
        return distancias, anterior

    def caminho_mais_curto(self, origem, destino):
        """
        Encontra o caminho mais curto entre duas cidades utilizando Dijkstra.

        Args:
            origem (str): Cidade de origem.
            destino (str): Cidade de destino.

        Returns:
            tuple:
                list: Caminho mais curto como lista de cidades.
                float: Distância total do caminho.
        """
        distancias, anterior = self.dijkstra(origem)
        caminho = []
        atual = destino
        while atual is not None:
            caminho.insert(0, atual)
            predecessores = anterior.get(atual, [None])
            if len(predecessores) < 2:
                break  # Se não houver antecessor válido, encerre o caminho
            atual = predecessores[-2]
        return caminho, distancias.get(destino, float('inf'))

    def __repr__(self):
        """
        Retorna uma representação em string do grafo.

        Returns:
            str: Quantidade de cidades no grafo.
        """
        return f"Grafo com {len(self.grafo.nodes)} cidades e {len(self.grafo.edges)} estradas"
