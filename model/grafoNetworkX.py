# Em model/grafoNetworkX.py
import networkx as nx
# heapq não é mais necessário aqui se usarmos as funções diretas do NetworkX

class GrafoNetworkX:
    def __init__(self, tipo_fila_dijkstra='nativo_nx_heap'): # Parâmetro informativo
        """
        Inicializa um grafo utilizando a biblioteca NetworkX.
        O tipo_fila_dijkstra é principalmente para fins de nomenclatura no relatório,
        pois usaremos as implementações otimizadas do NetworkX.
        """
        self.grafo = nx.Graph()  # Grafo não direcionado
        self.tipo_fila_dijkstra = tipo_fila_dijkstra # Armazena para o __repr__ ou relatórios

    def adicionar_aresta(self, origem: str, destino: str, distancia: float):
        """
        Adiciona uma aresta bidirecional ao grafo NetworkX.
        O atributo 'weight' é o padrão usado por muitas funções do NetworkX.
        """
        self.grafo.add_edge(origem, destino, weight=distancia)

    def caminho_mais_curto(self, origem: str, destino: str):
        """
        Encontra o caminho mais curto e a distância usando as funções do NetworkX.
        Retorna (lista_caminho, custo_total) ou (None, float('inf')).
        """
        try:
            if origem not in self.grafo or destino not in self.grafo:
                return None, float('inf')

            custo = nx.dijkstra_path_length(self.grafo, source=origem, target=destino, weight='weight')
            caminho = nx.dijkstra_path(self.grafo, source=origem, target=destino, weight='weight')
            return caminho, custo
        except nx.NetworkXNoPath: # Exceção específica se não houver caminho
            return None, float('inf')
        except nx.NodeNotFound: # Exceção se origem ou destino não estiverem no grafo (já checado acima, mas como fallback)
            return None, float('inf')
        except Exception as e: # Captura genérica para outros possíveis erros do NetworkX
            return None, float('inf')


    def __repr__(self):
        return f"GrafoNetworkX com {self.grafo.number_of_nodes()} cidades e {self.grafo.number_of_edges()} estradas (Dijkstra: {self.tipo_fila_dijkstra})"
    