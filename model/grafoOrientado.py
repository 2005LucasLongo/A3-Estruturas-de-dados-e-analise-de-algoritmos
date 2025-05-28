import heapq

class Aresta:
    def __init__(self, destino_nome: str, peso: float):
        self.destino_nome = destino_nome
        self.peso = peso

    def __repr__(self):
        return f"Aresta(destino_nome='{self.destino_nome}', peso={self.peso})"


class Vertice:
    def __init__(self, nome: str):
        self.nome = nome
        self.arestas = [] 

    def adicionar_aresta(self, destino_nome: str, peso: float):
        # Poderia checar se a aresta para este destino já existe se necessário
        self.arestas.append(Aresta(destino_nome, peso))

    def __repr__(self):
        return f"Vertice(nome='{self.nome}', num_arestas={len(self.arestas)})"


class GrafoOrientado: # Vamos chamá-la de GrafoComObjetos para o teste
    def __init__(self, tipo_fila_dijkstra='heap'): # Adicionado parâmetro
        self.vertices = {}  # Mapeia nome_cidade para objeto Vertice
        self.tipo_fila_dijkstra = tipo_fila_dijkstra.lower()
        if self.tipo_fila_dijkstra not in ['heap', 'lista']:
            raise ValueError("tipo_fila_dijkstra deve ser 'heap' ou 'lista'")

    def _obter_ou_criar_vertice(self, nome_cidade: str) -> Vertice:
        if nome_cidade not in self.vertices:
            self.vertices[nome_cidade] = Vertice(nome_cidade)
        return self.vertices[nome_cidade]

    def adicionar_aresta(self, origem_str: str, destino_str: str, peso: float):
        vertice_origem = self._obter_ou_criar_vertice(origem_str)
        self._obter_ou_criar_vertice(destino_str) # Garante que o vértice de destino exista no dicionário self.vertices

        vertice_origem.adicionar_aresta(destino_str, peso)
        
        # Para comportamento NÃO-DIRECIONADO (tornando comparável com outros grafos no problema):
        vertice_destino_obj = self.vertices[destino_str]
        vertice_destino_obj.adicionar_aresta(origem_str, peso)


    def vizinhos(self, nome_no_atual: str) -> list:
        """ Retorna vizinhos como lista de tuplas (nome_vizinho, peso_aresta). """
        if nome_no_atual in self.vertices:
            vertice_atual_obj = self.vertices[nome_no_atual]
            return [(aresta.destino_nome, aresta.peso) for aresta in vertice_atual_obj.arestas]
        return []

    def obter_nomes_dos_nos(self) -> list: # Renomeado para clareza
        return list(self.vertices.keys())

    def dijkstra(self, origem_str: str):
        if origem_str not in self.vertices:
            dist_vazias = {nome_v: float('inf') for nome_v in self.obter_nomes_dos_nos()}
            ant_vazios = {nome_v: None for nome_v in self.obter_nomes_dos_nos()}
            return dist_vazias, ant_vazios

        todos_os_nomes_nos = self.obter_nomes_dos_nos()
        distancias = {nome_v: float('inf') for nome_v in todos_os_nomes_nos}
        anterior = {nome_v: None for nome_v in todos_os_nomes_nos}
        
        # Assegurar que a origem está em distancias antes de tentar acessá-la
        if origem_str in distancias:
            distancias[origem_str] = 0
        else: # Deve ser coberto pela primeira checagem, mas como segurança
            return distancias, anterior

        if self.tipo_fila_dijkstra == 'heap':
            pq = [(0, origem_str)]  # (distancia, nome_vertice)
            while pq:
                dist_u, u_nome = heapq.heappop(pq)

                if dist_u > distancias.get(u_nome, float('inf')):
                    continue

                for vizinho_nome, peso_aresta in self.vizinhos(u_nome):
                    if distancias.get(u_nome, float('inf')) + peso_aresta < distancias.get(vizinho_nome, float('inf')):
                        distancias[vizinho_nome] = distancias[u_nome] + peso_aresta
                        anterior[vizinho_nome] = u_nome
                        heapq.heappush(pq, (distancias[vizinho_nome], vizinho_nome))
        
        elif self.tipo_fila_dijkstra == 'lista':
            visitados = set()
            for _ in range(len(todos_os_nomes_nos)):
                min_dist_atual = float('inf')
                u_nome = None
                for nome_no_iter in todos_os_nomes_nos:
                    if nome_no_iter not in visitados and distancias.get(nome_no_iter, float('inf')) < min_dist_atual:
                        min_dist_atual = distancias[nome_no_iter]
                        u_nome = nome_no_iter
                
                if u_nome is None:
                    break 
                
                visitados.add(u_nome)

                for vizinho_nome, peso_aresta in self.vizinhos(u_nome):
                    if distancias.get(u_nome, float('inf')) + peso_aresta < distancias.get(vizinho_nome, float('inf')):
                        distancias[vizinho_nome] = distancias[u_nome] + peso_aresta
                        anterior[vizinho_nome] = u_nome
        else:
            raise NotImplementedError(f"Tipo de fila {self.tipo_fila_dijkstra} não implementado.")
            
        return distancias, anterior

    def caminho_mais_curto(self, origem_str: str, destino_str: str):
        if origem_str not in self.vertices or destino_str not in self.vertices:
            return None, float('inf')

        distancias, anterior = self.dijkstra(origem_str)

        if distancias.get(destino_str, float('inf')) == float('inf'):
            return None, float('inf')

        caminho = []
        atual_str = destino_str
        num_nos = len(self.vertices)
        for _ in range(num_nos + 2): # Loop de segurança um pouco maior
            if atual_str is None:
                return None, float('inf') 
            
            caminho.insert(0, atual_str)
            if atual_str == origem_str:
                break 
            atual_str = anterior.get(atual_str)
        else: 
            return None, float('inf') 

        if not caminho or caminho[0] != origem_str:
            return None, float('inf') 
            
        return caminho, distancias[destino_str]

    def __repr__(self):
        return f"GrafoComObjetos com {len(self.vertices)} cidades (Fila Dijkstra: {self.tipo_fila_dijkstra})"