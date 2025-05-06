import heapq

class GrafoDicionario:
    def __init__(self):
        self.grafo = {}

    def adicionar_aresta(self, origem, destino, peso):
        if origem not in self.grafo:
            self.grafo[origem] = {}
        if destino not in self.grafo:
            self.grafo[destino] = {}
        self.grafo[origem][destino] = peso
        self.grafo[destino][origem] = peso  # Grafo não-direcionado

    def vizinhos(self, no):
        return self.grafo.get(no, {}).items()

    def obter_nos(self):
        return list(self.grafo.keys())

    def dijkstra(self, origem):
        distancias = {no: float('inf') for no in self.grafo}
        distancias[origem] = 0
        anterior = {no: None for no in self.grafo}

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
        distancias, anterior = self.dijkstra(origem)
        caminho = []
        atual = destino
        while atual is not None:
            caminho.insert(0, atual)
            atual = anterior[atual]
        return caminho, distancias[destino]

    def __repr__(self):
        return f"GrafoDicionario com {len(self.grafo)} nós"
