import heapq

class GrafoListaArestas:
    def __init__(self, tipo_fila_dijkstra='heap'): # Adicionado parâmetro
        """
        Inicializa o grafo com uma lista de arestas.
        Cada aresta é uma tupla (origem, destino, peso).
        """
        self.arestas = []  # Lista de arestas
        self.nos_do_grafo = None # Cache para os nós
        self.tipo_fila_dijkstra = tipo_fila_dijkstra.lower()
        if self.tipo_fila_dijkstra not in ['heap', 'lista']:
            raise ValueError("tipo_fila_dijkstra deve ser 'heap' ou 'lista'")

    def adicionar_aresta(self, origem, destino, peso):
        """ Adiciona uma aresta bidirecional. """
        self.arestas.append((origem, destino, peso))
        self.arestas.append((destino, origem, peso))
        self.nos_do_grafo = None # Invalida o cache de nós ao adicionar aresta

    def _atualizar_nos(self):
        """ Helper interno para obter e armazenar os nós únicos do grafo. """
        if self.nos_do_grafo is None:
            nos = set()
            for o, d, _ in self.arestas:
                nos.add(o)
                nos.add(d)
            self.nos_do_grafo = list(nos)
        return self.nos_do_grafo

    def vizinhos(self, no_atual):
        """ Retorna os vizinhos de um nó. """
        # Esta operação é O(E) e será o gargalo no Dijkstra para esta estrutura.
        viz = []
        for origem_aresta, destino_aresta, peso_aresta in self.arestas:
            if origem_aresta == no_atual:
                viz.append((destino_aresta, peso_aresta))
            # Não precisa checar 'elif destino_aresta == no_atual' se as arestas
            # já são adicionadas bidirecionalmente e 'self.arestas' contém ambas.
            # Se 'adicionar_aresta' só adicionasse uma direção e você quisesse
            # que vizinhos() encontrasse ambas, aí sim. Mas com a atual 'adicionar_aresta',
            # esta forma é suficiente, embora ainda O(E).
        return viz

    def dijkstra(self, origem_str: str):
        nos = self._atualizar_nos()
        if origem_str not in nos:
            dist_vazias = {n: float('inf') for n in nos}
            ant_vazios = {n: None for n in nos}
            return dist_vazias, ant_vazios

        distancias = {n: float('inf') for n in nos}
        anterior = {n: None for n in nos}
        distancias[origem_str] = 0

        if self.tipo_fila_dijkstra == 'heap':
            pq = [(0, origem_str)]  # (distancia, vertice)
            while pq:
                dist_u, u = heapq.heappop(pq)

                if dist_u > distancias[u]:
                    continue

                for vizinho, peso in self.vizinhos(u): # self.vizinhos() é O(E)
                    if distancias[u] + peso < distancias[vizinho]:
                        distancias[vizinho] = distancias[u] + peso
                        anterior[vizinho] = u
                        heapq.heappush(pq, (distancias[vizinho], vizinho))
        
        elif self.tipo_fila_dijkstra == 'lista':
            visitados = set()
            for _ in range(len(nos)):
                min_dist_atual = float('inf')
                u = None
                for no_iter in nos:
                    if no_iter not in visitados and distancias[no_iter] < min_dist_atual:
                        min_dist_atual = distancias[no_iter]
                        u = no_iter
                
                if u is None:
                    break 
                
                visitados.add(u)

                for vizinho, peso in self.vizinhos(u): # self.vizinhos() é O(E)
                    if distancias[u] + peso < distancias[vizinho]:
                        distancias[vizinho] = distancias[u] + peso
                        anterior[vizinho] = u
        else:
            raise NotImplementedError(f"Tipo de fila {self.tipo_fila_dijkstra} não implementado.")
            
        return distancias, anterior

    def caminho_mais_curto(self, origem: str, destino: str):
        distancias, anterior = self.dijkstra(origem)

        # Verificar se o destino é alcançável
        if distancias.get(destino, float('inf')) == float('inf'):
            return None, float('inf')

        caminho = []
        atual = destino
        # Loop de segurança para evitar ciclos infinitos se 'anterior' estiver malformado
        for _ in range(len(self.nos_do_grafo) + 1 if self.nos_do_grafo else 1): 
            if atual is None:
                # Chegou ao fim da cadeia de predecessores sem encontrar a origem
                return None, float('inf') # Caminho quebrado
            
            caminho.insert(0, atual)
            if atual == origem:
                break # Caminho encontrado
            atual = anterior.get(atual) # Usar .get para segurança
        else: 
            # Se o loop for..else for completado sem break (caminho muito longo ou ciclo)
            return None, float('inf') # Caminho não encontrado ou inválido

        # Validação final
        if not caminho or caminho[0] != origem:
            return None, float('inf') 
            
        return caminho, distancias[destino]

    def __repr__(self):
        # Chama _atualizar_nos para garantir que self.nos_do_grafo esteja disponível
        num_nos_display = len(self._atualizar_nos()) if self.nos_do_grafo is not None else "N/A (chame _atualizar_nos)"
        return f"GrafoListaArestas com {num_nos_display} nós (Fila Dijkstra: {self.tipo_fila_dijkstra})"