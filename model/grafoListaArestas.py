import heapq

class GrafoListaArestas:
    def __init__(self):
        """
        Inicializa o grafo com uma lista de arestas.
        Cada aresta é uma tupla (origem, destino, peso).
        """
        self.arestas = []  # Lista de arestas, cada aresta é uma tupla (origem, destino, peso)

    def adicionar_aresta(self, origem, destino, peso):
        """
        Adiciona uma aresta bidirecional entre duas cidades com uma distância específica.

        Args:
            origem (str): Cidade de origem.
            destino (str): Cidade de destino.
            peso (float): Distância entre origem e destino.
        """
        self.arestas.append((origem, destino, peso))
        self.arestas.append((destino, origem, peso))  # Grafo não-direcionado

    def vizinhos(self, no):
        """
        Retorna os vizinhos de um nó, ou seja, todas as cidades conectadas a este nó.

        Args:
            no (str): O nó (cidade) para o qual se quer obter os vizinhos.

        Returns:
            list: Lista de tuplas (vizinho, peso) que representam as cidades vizinhas.
        """
        return [(destino, peso) for (origem, destino, peso) in self.arestas if origem == no]

    def obter_nos(self):
        """
        Retorna a lista de nós (cidades) do grafo, sem repetições.

        Returns:
            list: Lista de nós.
        """
        return list(set(origem for origem, destino, peso in self.arestas) | set(destino for origem, destino, peso in self.arestas))

    def dijkstra(self, origem):
        """
        Executa o algoritmo de Dijkstra para encontrar o menor caminho de uma cidade origem até todas as outras.

        Args:
            origem (str): Cidade de origem.

        Returns:
            tuple:
                dict: Mapeamento de cidades para suas menores distâncias desde a origem.
                dict: Mapeamento de cada cidade para seu antecessor no caminho mais curto.
        """
        distancias = {no: float('inf') for no in self.obter_nos()}
        distancias[origem] = 0
        anterior = {no: None for no in self.obter_nos()}

        fila = [(0, origem)]
        while fila:
            dist_atual, atual = heapq.heappop(fila)
            if dist_atual > distancias[atual]:
                continue
            for vizinho, peso in self.vizinhos(atual):
                nova_dist = dist_atual + peso
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    anterior[vizinho] = atual
                    heapq.heappush(fila, (nova_dist, vizinho))

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
            atual = anterior[atual]
        return caminho, distancias[destino]

    def __repr__(self):
        return f"GrafoListaArestas com {len(self.obter_nos())} nós"

