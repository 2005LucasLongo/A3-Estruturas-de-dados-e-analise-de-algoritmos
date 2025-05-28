import heapq

class GrafoListaAdjacencia:
    """
    Representa um grafo não direcionado onde os vértices são cidades e as arestas representam estradas com distâncias associadas.
    """
    def __init__(self, tipo_fila_dijkstra='heap'):
        """
        Inicializa um grafo vazio com um dicionário de adjacência.
        """
        self.vertices = {}  # {cidade: [(vizinho, distancia)]}
        self.tipo_fila_dijkstra = tipo_fila_dijkstra.lower()
        if self.tipo_fila_dijkstra not in ['heap', 'lista']:
            raise ValueError("tipo_fila_dijkstra deve ser 'heap' ou 'lista'")

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
        
        # Evitar adicionar arestas duplicadas na lista de adjacência
        # (Se o mapa_logistico já garante arestas únicas, esta checagem é opcional mas segura)
        if not any(v == destino for v, d in self.vertices[origem]):
            self.vertices[origem].append((destino, distancia))
        if not any(v == origem for v, d in self.vertices[destino]):
            self.vertices[destino].append((origem, distancia))

    def dijkstra(self, origem_str: str):
        """
        Executa o algoritmo de Dijkstra para encontrar o menor caminho de uma cidade origem até todas as outras.

        Args:
            origem (str): Cidade de origem.

        Returns:
            tuple:
                dict: Mapeamento de cidades para suas menores distâncias desde a origem.
                dict: Mapeamento de cada cidade para seu antecessor no caminho mais curto.
        """

        if origem_str not in self.vertices:
            # Retornar um formato que caminho_mais_curto possa interpretar como falha
            # Por exemplo, um dicionário de distâncias onde todas são infinitas
            dist_vazias = {v: float('inf') for v in self.vertices}
            ant_vazios = {v: None for v in self.vertices}
            if self.vertices: # Se o grafo não está totalmente vazio
                 if origem_str in dist_vazias: dist_vazias[origem_str] = float('inf') # Garante que é inf se não for um nó válido
            return dist_vazias, ant_vazios


        distancias = {v: float('inf') for v in self.vertices}
        anterior = {v: None for v in self.vertices}
        distancias[origem_str] = 0

        if self.tipo_fila_dijkstra == 'heap':
            pq = [(0, origem_str)]  # (distancia, vertice)
            while pq:
                dist_u, u = heapq.heappop(pq)

                if dist_u > distancias[u]:
                    continue

                for vizinho, peso in self.vertices.get(u, []):
                    if distancias[u] + peso < distancias[vizinho]:
                        distancias[vizinho] = distancias[u] + peso
                        anterior[vizinho] = u
                        heapq.heappush(pq, (distancias[vizinho], vizinho))
        
        elif self.tipo_fila_dijkstra == 'lista':
            visitados = set()
            num_total_vertices = len(self.vertices)
            for _ in range(num_total_vertices):
                min_dist_atual = float('inf')
                u = None
                # Encontrar o nó não visitado com menor distância
                for vertice_iter in self.vertices:
                    if vertice_iter not in visitados and distancias[vertice_iter] < min_dist_atual:
                        min_dist_atual = distancias[vertice_iter]
                        u = vertice_iter
                
                if u is None: # Nenhum nó alcançável restante ou todos visitados
                    break 
                
                visitados.add(u)

                for vizinho, peso in self.vertices.get(u, []):
                    if distancias[u] + peso < distancias[vizinho]:
                        distancias[vizinho] = distancias[u] + peso
                        anterior[vizinho] = u
        else: # Deveria ter sido pego no __init__
            raise ValueError(f"Tipo de fila Dijkstra desconhecido: {self.tipo_fila_dijkstra}")
            
        return distancias, anterior

    def caminho_mais_curto(self, origem: str, destino: str):
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
        if origem not in self.vertices or destino not in self.vertices:
            return None, float('inf') # Cidades não existem no grafo

        distancias, anterior = self.dijkstra(origem)

        if distancias.get(destino, float('inf')) == float('inf'):
            return None, float('inf')

        caminho = []
        atual = destino
        while atual is not None:
            caminho.insert(0, atual)
            if atual == origem:
                break
            atual = anterior.get(atual) # Usar .get para segurança
            if atual is None and (not caminho or caminho[0] != origem): # Interrompeu antes de chegar na origem
                 return None, float('inf') # Caminho quebrado
        
        if not caminho or caminho[0] != origem:
             # Caso especial: origem == destino já tratado por distancias[origem]=0
            return None, float('inf') # Caminho não pôde ser reconstruído corretamente

        return caminho, distancias[destino]

    def __repr__(self):
        """
        Retorna uma representação em string do grafo.

        Returns:
            str: Quantidade de cidades no grafo.
        """
        return f"GrafoListaAdjacencia com {len(self.vertices)} cidades (Fila Dijkstra: {self.tipo_fila_dijkstra})"
