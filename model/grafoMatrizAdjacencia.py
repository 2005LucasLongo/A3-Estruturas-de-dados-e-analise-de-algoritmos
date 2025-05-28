import heapq

class GrafoMatrizAdjacencia:
    """
    Representação de um grafo usando uma matriz de adjacência.
    """
    def __init__(self, cidades, tipo_fila_dijkstra='lista'):
        """
        Inicializa o grafo com uma matriz de adjacência.

        Args:
            cidades (List[str]): Lista de cidades que formam os vértices do grafo.
        """
        self.cidades = list(set(cidades)) # Garante cidades únicas e cria uma cópia
        self.n = len(self.cidades)
        self.map_cidade_para_idx = {cidade: i for i, cidade in enumerate(self.cidades)}
        
        self.matriz = [[float('inf')] * self.n for _ in range(self.n)]
        for i in range(self.n):
            self.matriz[i][i] = 0
        
        self.tipo_fila_dijkstra = tipo_fila_dijkstra.lower()
        if self.tipo_fila_dijkstra not in ['heap', 'lista']:
            raise ValueError("tipo_fila_dijkstra deve ser 'heap' ou 'lista'")

    def adicionar_aresta(self, cidade1_str: str, cidade2_str: str, distancia: float):
        """
        Adiciona uma aresta entre as cidades com uma distância (peso).

        Args:
            cidade1 (str): Nome da primeira cidade.
            cidade2 (str): Nome da segunda cidade.
            distancia (float): Distância entre as duas cidades.
        """
        idx1 = self.map_cidade_para_idx.get(cidade1_str)
        idx2 = self.map_cidade_para_idx.get(cidade2_str)

        if idx1 is not None and idx2 is not None:
            self.matriz[idx1][idx2] = distancia
            self.matriz[idx2][idx1] = distancia

    def dijkstra(self, origem_str: int):
        idx_origem = self.map_cidade_para_idx.get(origem_str)
        if idx_origem is None:
            # Retornar arrays/listas vazias ou com inf para consistência
            dist_vazias_map = {c: float('inf') for c in self.cidades}
            ant_vazios_map = {c: None for c in self.cidades}
            return dist_vazias_map, ant_vazios_map

        dist = [float('inf')] * self.n
        prev = [None] * self.n # Armazena índices dos predecessores
        dist[idx_origem] = 0
        
        if self.tipo_fila_dijkstra == 'heap':
            pq = [(0, idx_origem)]  # (distancia, vertice_idx)
            visitados_heap = [False] * self.n # Para otimizar no heap com matriz

            while pq:
                d, u_idx = heapq.heappop(pq)

                if d > dist[u_idx]: # Se já encontramos um caminho menor
                    continue
                
                # if visitados_heap[u_idx]: # Opcional: se um nó pode ser adicionado múltiplas vezes com distâncias diferentes
                #     continue
                # visitados_heap[u_idx] = True


                for v_idx in range(self.n):
                    peso_aresta = self.matriz[u_idx][v_idx]
                    if peso_aresta != float('inf'): # Existe aresta u_idx -> v_idx
                        if dist[u_idx] + peso_aresta < dist[v_idx]:
                            dist[v_idx] = dist[u_idx] + peso_aresta
                            prev[v_idx] = u_idx
                            heapq.heappush(pq, (dist[v_idx], v_idx))
        
        elif self.tipo_fila_dijkstra == 'lista':
            visitados_lista = [False] * self.n
            for _ in range(self.n):
                min_dist_atual = float('inf')
                u_idx = -1
                for i_vert in range(self.n):
                    if not visitados_lista[i_vert] and dist[i_vert] < min_dist_atual:
                        min_dist_atual = dist[i_vert]
                        u_idx = i_vert
                
                if u_idx == -1: # Nenhum nó alcançável restante
                    break
                
                visitados_lista[u_idx] = True
                for v_idx in range(self.n):
                    # A condição 'not visitados_lista[v_idx]' não é estritamente necessária aqui para relaxamento,
                    # mas sim para a escolha do próximo 'u'.
                    peso_aresta = self.matriz[u_idx][v_idx] # Já checamos se u_idx é válido
                    if peso_aresta != float('inf'): # Existe aresta
                        if dist[u_idx] + peso_aresta < dist[v_idx]:
                            dist[v_idx] = dist[u_idx] + peso_aresta
                            prev[v_idx] = u_idx
        else:
            raise ValueError(f"Tipo de fila Dijkstra desconhecido: {self.tipo_fila_dijkstra}")

        # Converter distancias e prev (que usam índices) de volta para nomes de cidades
        dist_final_map = {self.cidades[i]: dist[i] for i in range(self.n)}
        # Cuidado: prev[i] é um ÍNDICE. Se for None, continua None.
        ant_final_map = {
            self.cidades[i]: (self.cidades[prev[i]] if prev[i] is not None else None)
            for i in range(self.n)
        }
        return dist_final_map, ant_final_map
    
    def caminho_mais_curto(self, origem_str: str, destino_str: str):
        """
        Retorna o caminho mais curto e o tempo estimado usando o algoritmo de Dijkstra.

        Args:
            origem (str): Nome da cidade de origem.
            destino (str): Nome da cidade de destino.

        Returns:
            tuple (List[str], float): O caminho e o tempo estimado.
        """
        if origem_str not in self.map_cidade_para_idx or destino_str not in self.map_cidade_para_idx:
            return None, float('inf')

        distancias_map, anterior_map = self.dijkstra(origem_str)

        dist_destino = distancias_map.get(destino_str, float('inf'))
        if dist_destino == float('inf'):
            return None, float('inf')

        caminho = []
        atual_str = destino_str
        # Loop de segurança para evitar ciclos infinitos se 'anterior_map' estiver malformado
        for _ in range(self.n + 1): 
            if atual_str is None: # Chegou ao fim da cadeia de predecessores sem encontrar a origem
                # Isso não deveria acontecer se dist_destino não for inf e origem != destino
                # A menos que a origem não seja um nó válido no 'anterior_map' do dijkstra.
                return None, float('inf') # Caminho quebrado
            
            caminho.insert(0, atual_str)
            if atual_str == origem_str:
                break # Caminho encontrado
            atual_str = anterior_map.get(atual_str)
        else: # Se o loop for..else for completado sem break (caminho muito longo ou ciclo)
            return None, float('inf') # Caminho não encontrado ou inválido

        if not caminho or caminho[0] != origem_str:
            # Redundante se o loop acima funcionou, mas como segurança
            return None, float('inf') 
            
        return caminho, dist_destino

    def __repr__(self):
        return f"GrafoMatrizAdjacencia com {self.n} cidades (Fila Dijkstra: {self.tipo_fila_dijkstra})"
    