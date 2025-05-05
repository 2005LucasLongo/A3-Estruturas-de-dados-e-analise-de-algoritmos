class GrafoMatrizAdjacencia:
    """
    Representação de um grafo usando uma matriz de adjacência.
    """
    def __init__(self, cidades):
        """
        Inicializa o grafo com uma matriz de adjacência.

        Args:
            cidades (List[str]): Lista de cidades que formam os vértices do grafo.
        """
        self.cidades = cidades
        self.n = len(cidades)
        # Inicializa a matriz com infinito (distância não conhecida)
        self.matriz = [[float('inf')] * self.n for _ in range(self.n)]

    def adicionar_aresta(self, cidade1, cidade2, distancia):
        """
        Adiciona uma aresta entre as cidades com uma distância (peso).

        Args:
            cidade1 (str): Nome da primeira cidade.
            cidade2 (str): Nome da segunda cidade.
            distancia (float): Distância entre as duas cidades.
        """
        i = self.cidades.index(cidade1)
        j = self.cidades.index(cidade2)
        # A matriz é não dirigida, então adicionamos em ambos os sentidos
        self.matriz[i][j] = distancia
        self.matriz[j][i] = distancia

    def caminho_mais_curto(self, origem, destino):
        """
        Retorna o caminho mais curto e o tempo estimado usando o algoritmo de Dijkstra.

        Args:
            origem (str): Nome da cidade de origem.
            destino (str): Nome da cidade de destino.

        Returns:
            tuple (List[str], float): O caminho e o tempo estimado.
        """
        i = self.cidades.index(origem)
        j = self.cidades.index(destino)
        
        # Algoritmo de Dijkstra para matriz de adjacência
        dist = [float('inf')] * self.n
        dist[i] = 0
        visited = [False] * self.n
        prev = [None] * self.n
        
        while True:
            # Seleciona o vértice não visitado com a menor distância
            min_dist = float('inf')
            u = -1
            for v in range(self.n):
                if not visited[v] and dist[v] < min_dist:
                    min_dist = dist[v]
                    u = v
            
            if u == -1 or dist[u] == float('inf'):
                break
            
            visited[u] = True
            for v in range(self.n):
                if not visited[v] and self.matriz[u][v] < float('inf'):
                    alt = dist[u] + self.matriz[u][v]
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
        
        # Reconstruir o caminho
        caminho = []
        u = j
        while u is not None:
            caminho.append(self.cidades[u])
            u = prev[u]
        caminho.reverse()
        
        return caminho, dist[j]
