import heapq

class Grafo:
    """
    Representa um grafo não direcionado onde os vértices são cidades e as arestas representam estradas com distâncias associadas.
    """
    def __init__(self):
        """
        Inicializa um grafo vazio com um dicionário de adjacência.
        """
        self.vertices = {}  # {cidade: [(vizinho, distancia)]}

    def adicionar_aresta(self, origem, destino, distancia):
        """
        Adiciona uma aresta bidirecional entre duas cidades com uma distância específica.

        Args:
            origem (str): Cidade de origem.
            destino (str): Cidade de destino.
            distancia (float): Distância entre origem e destino.
        """
        if origem not in self.vertices:
            self.vertices[origem] = []
        if destino not in self.vertices:
            self.vertices[destino] = []
        self.vertices[origem].append((destino, distancia))
        self.vertices[destino].append((origem, distancia))  # Se for bidirecional

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
        distancias = {v: float('inf') for v in self.vertices}
        distancias[origem] = 0
        anterior = {v: None for v in self.vertices}

        fila = [(0, origem)]
        while fila:
            dist_atual, atual = heapq.heappop(fila)
            if dist_atual > distancias[atual]:
                continue
            for vizinho, peso in self.vertices[atual]:
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
        """
        Retorna uma representação em string do grafo.

        Returns:
            str: Quantidade de cidades no grafo.
        """
        return f"Grafo com {len(self.vertices)} cidades"
