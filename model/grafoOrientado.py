import heapq

class Aresta:
    def __init__(self, destino, peso):
        """
        Representa uma aresta no grafo.

        Args:
            destino (str): Cidade de destino.
            peso (float): Distância ou peso da aresta.
        """
        self.destino = destino
        self.peso = peso

    def __repr__(self):
        return f"Aresta(destino={self.destino}, peso={self.peso})"


class Vertice:
    def __init__(self, nome):
        """
        Representa um vértice (cidade) no grafo.

        Args:
            nome (str): Nome da cidade.
        """
        self.nome = nome
        self.arestas = []  # Lista de arestas saindo deste vértice

    def adicionar_aresta(self, destino, peso):
        """
        Adiciona uma aresta de saída deste vértice.

        Args:
            destino (str): Nome da cidade de destino.
            peso (float): Peso ou distância da aresta.
        """
        self.arestas.append(Aresta(destino, peso))

    def __repr__(self):
        return f"Vertice(nome={self.nome}, arestas={self.arestas})"


class GrafoOrientado:
    def __init__(self):
        """
        Inicializa um grafo vazio.
        """
        self.vertices = {}  # Mapeia cidade para um objeto Vertice

    def adicionar_aresta(self, origem, destino, peso):
        """
        Adiciona uma aresta orientada de uma cidade para outra.

        Args:
            origem (str): Cidade de origem.
            destino (str): Cidade de destino.
            peso (float): Peso da aresta.
        """
        if origem not in self.vertices:
            self.vertices[origem] = Vertice(origem)
        if destino not in self.vertices:
            self.vertices[destino] = Vertice(destino)
        self.vertices[origem].adicionar_aresta(destino, peso)

    def vizinhos(self, no):
        """
        Retorna os vizinhos (cidades alcançáveis) a partir de um vértice.

        Args:
            no (str): Nome da cidade.

        Returns:
            list: Lista de destinos e pesos das arestas saindo do vértice.
        """
        return [(aresta.destino, aresta.peso) for aresta in self.vertices[no].arestas] if no in self.vertices else []

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
        """
        Retorna uma representação em string do grafo.

        Returns:
            str: Quantidade de cidades no grafo.
        """
        return f"Grafo Orientado com {len(self.vertices)} cidades"

