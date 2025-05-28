import heapq

class GrafoDicionario:
    def __init__(self, tipo_fila_dijkstra='heap'): # Adicionado parâmetro
        """
        Inicializa o grafo usando um dicionário de dicionários.
        self.grafo = {origem: {destino1: peso1, destino2: peso2}, ...}
        """
        self.grafo = {}
        self.tipo_fila_dijkstra = tipo_fila_dijkstra.lower()
        if self.tipo_fila_dijkstra not in ['heap', 'lista']:
            raise ValueError("tipo_fila_dijkstra deve ser 'heap' ou 'lista'")

    def adicionar_aresta(self, origem, destino, peso):
        """ Adiciona uma aresta bidirecional. """
        # Garante que as chaves de origem e destino existam
        self.grafo.setdefault(origem, {})[destino] = peso
        self.grafo.setdefault(destino, {})[origem] = peso

    def vizinhos(self, no_atual):
        """ Retorna os vizinhos de um nó e os pesos das arestas. """
        return self.grafo.get(no_atual, {}).items() # Eficiente

    def obter_nos(self):
        """ Retorna uma lista de todos os nós (cidades) no grafo. """
        return list(self.grafo.keys())

    def dijkstra(self, origem_str: str):
        if origem_str not in self.grafo: # Verifica se a origem existe
            # Retorna estruturas vazias/infinitas se a origem não for válida
            dist_vazias = {n: float('inf') for n in self.obter_nos()}
            ant_vazios = {n: None for n in self.obter_nos()}

            return dist_vazias, ant_vazios

        todos_os_nos = self.obter_nos() # Obtém todos os nós para inicialização
        distancias = {no: float('inf') for no in todos_os_nos}
        anterior = {no: None for no in todos_os_nos}
        
        if origem_str in distancias: # Garante que a origem é um nó conhecido
            distancias[origem_str] = 0
        else: 
              return distancias, anterior


        if self.tipo_fila_dijkstra == 'heap':
            pq = [(0, origem_str)]  # (distancia, vertice)
            while pq:
                dist_u, u = heapq.heappop(pq)

                if dist_u > distancias.get(u, float('inf')): # Usar .get para segurança
                    continue

                for vizinho, peso in self.vizinhos(u): # self.vizinhos() é eficiente aqui
                    if distancias.get(u, float('inf')) + peso < distancias.get(vizinho, float('inf')):
                        distancias[vizinho] = distancias[u] + peso
                        anterior[vizinho] = u
                        heapq.heappush(pq, (distancias[vizinho], vizinho))
        
        elif self.tipo_fila_dijkstra == 'lista':
            visitados = set()
            for _ in range(len(todos_os_nos)):
                min_dist_atual = float('inf')
                u = None
                # Encontra o nó não visitado com menor distância
                for no_iter in todos_os_nos: # Itera sobre todos os nós conhecidos
                    if no_iter not in visitados and distancias.get(no_iter, float('inf')) < min_dist_atual:
                        min_dist_atual = distancias[no_iter]
                        u = no_iter
                
                if u is None: # Nenhum nó alcançável restante ou todos visitados
                    break 
                
                visitados.add(u)

                for vizinho, peso in self.vizinhos(u): # Eficiente
                    if distancias.get(u, float('inf')) + peso < distancias.get(vizinho, float('inf')):
                        distancias[vizinho] = distancias[u] + peso
                        anterior[vizinho] = u
        else:
            raise NotImplementedError(f"Tipo de fila {self.tipo_fila_dijkstra} não implementado.")
            
        return distancias, anterior

    def caminho_mais_curto(self, origem: str, destino: str):
        if origem not in self.grafo or destino not in self.grafo: # Verifica se origem e destino existem
            return None, float('inf')

        distancias, anterior = self.dijkstra(origem)

        if distancias.get(destino, float('inf')) == float('inf'): # Destino inalcançável
            return None, float('inf')

        caminho = []
        atual = destino
        # Loop de segurança para evitar ciclos infinitos
        num_nos = len(self.obter_nos())
        for _ in range(num_nos + 1): 
            if atual is None:
                # Caso estranho: predecessores quebrados, mas distância não era inf
                return None, float('inf') # Caminho quebrado
            
            caminho.insert(0, atual)
            if atual == origem:
                break # Caminho encontrado e completo
            atual = anterior.get(atual)
        else: 
            # Se o loop for..else for completado sem break (caminho muito longo ou ciclo)
            return None, float('inf') # Caminho não encontrado ou inválido

        # Validação final do caminho
        if not caminho or caminho[0] != origem:
            return None, float('inf') 
            
        return caminho, distancias[destino]

    def __repr__(self):
        return f"GrafoDicionario com {len(self.grafo)} nós (Fila Dijkstra: {self.tipo_fila_dijkstra})"