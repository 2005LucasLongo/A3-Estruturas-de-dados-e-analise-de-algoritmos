import time
import tracemalloc
import random
import os, sys

# ajusta path para encontrar o pacote
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

from model.entrega import Entrega
from model.caminhao import Caminhao
from model.centro_distribuicao import CentroDistribuicao
from controller.roteirizador import Roteirizador

# Definição de Matriz de Adjacência
class MatrizAdjacencia:
    """
    Representa um grafo não direcionado usando matriz de adjacência para modelar distâncias entre cidades.
    """
    def __init__(self, cidades):
        """
        Inicializa a matriz de adjacência com as cidades fornecidas.

        Args:
            cidades (list[str]): Lista de nomes das cidades.
        """
        self.indices = {cidade: i for i, cidade in enumerate(cidades)}
        n = len(cidades)
        self.matriz = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            self.matriz[i][i] = 0

    def adicionar_aresta(self, origem, destino, distancia):
        """
        Adiciona uma aresta bidirecional entre duas cidades com a distância especificada.

        Args:
            origem (str): Cidade de origem.
            destino (str): Cidade de destino.
            distancia (float): Distância entre origem e destino.
        """
        i, j = self.indices[origem], self.indices[destino]
        self.matriz[i][j] = distancia
        self.matriz[j][i] = distancia

    def dijkstra(self, origem):
        """
        Executa o algoritmo de Dijkstra a partir de uma cidade de origem.

        Args:
            origem (str): Cidade de origem.

        Returns:
            tuple: Dois dicionários, o primeiro com as distâncias mínimas e o segundo com os predecessores.
        """
        n = len(self.matriz)
        dist = [float('inf')] * n
        prev = [None] * n
        start = self.indices[origem]
        dist[start] = 0
        visited = [False] * n

        for _ in range(n):
            # seleciona não visitado com menor dist
            u = min((d, idx) for idx, d in enumerate(dist) if not visited[idx])[1]
            visited[u] = True
            for v in range(n):
                if self.matriz[u][v] < float('inf'):
                    alt = dist[u] + self.matriz[u][v]
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
        # converte para dict
        cidades = list(self.indices.keys())
        dist_map = {cidade: dist[idx] for cidade, idx in self.indices.items()}
        prev_map = {cidade: (list(self.indices.keys())[prev[idx]] if prev[idx] is not None else None) for cidade, idx in self.indices.items()}
        return dist_map, prev_map

    def caminho_mais_curto(self, origem, destino):
        """
        Retorna o caminho mais curto entre duas cidades.

        Args:
            origem (str): Cidade de origem.
            destino (str): Cidade de destino.

        Returns:
            tuple: Lista do caminho e distância total.
        """
        dist, prev = self.dijkstra(origem)
        path = []
        u = destino
        while u is not None:
            path.insert(0, u)
            u = prev[u]
        return path, dist[destino]


def gerar_entregas(qtd):
    """
    Gera uma lista de entregas com destinos e atributos aleatórios.

    Args:
        qtd (int): Quantidade de entregas a gerar.

    Returns:
        list[Entrega]: Lista de objetos Entrega.
    """
    destinos = [
        "Salvador", "Fortaleza", "Manaus", "Porto Alegre", "Curitiba",
        "Rio de Janeiro", "Vitória", "Goiânia", "Campo Grande", "Natal"
    ]
    return [Entrega(f"E{i:03d}", random.choice(destinos), random.randint(500,3000), random.randint(8,24)) for i in range(qtd)]


def preparar_centros():
    """
    Cria os centros de distribuição e adiciona caminhões a cada um.

    Returns:
        tuple: Lista de centros de distribuição e lista de nomes das cidades dos centros.
    """
    cidades = ["Belém", "Recife", "Brasília", "São Paulo", "Florianópolis"]
    centros = []
    for cidade in cidades:
        centro = CentroDistribuicao(cidade)
        for j in range(4):
            centro.adicionar_caminhao(Caminhao(f"{cidade[:2]}-{j+1}", 6000, 22))
        centros.append(centro)
    return centros, cidades


def preparar_grafo(cidades):
    """
    Cria o grafo de rotas baseado em matriz de adjacência.

    Args:
        cidades (list[str]): Lista de cidades dos centros de distribuição.

    Returns:
        MatrizAdjacencia: Grafo com as conexões configuradas.
    """
    m = MatrizAdjacencia(cidades + [
        "Salvador","Fortaleza","Manaus","Porto Alegre","Curitiba",
        "Rio de Janeiro","Vitória","Goiânia","Campo Grande","Natal"
    ])
    conexoes = [
        ("Belém","Manaus",10),("Recife","Fortaleza",5),("Recife","Salvador",6),
        ("Brasília","Salvador",7),("São Paulo","Curitiba",4),("Florianópolis","Curitiba",3),
        ("Florianópolis","Porto Alegre",5),("São Paulo","Porto Alegre",7),("Brasília","Goiânia",4),
        ("Brasília","Campo Grande",9),("São Paulo","Rio de Janeiro",6),("São Paulo","Vitória",8),
        ("Recife","Natal",4),("Belém","Brasília",12),("Recife","Brasília",10),
        ("Brasília","São Paulo",8),("São Paulo","Florianópolis",6)
    ]
    for o,d,dist in conexoes:
        m.adicionar_aresta(o,d,dist)
    return m


def testar_desempenho():
    """
    Executa um teste de desempenho da roteirização usando 100 entregas e matriz de adjacência,
    medindo tempo de execução e uso de memória.
    """
    centros, cidades_centros = preparar_centros()
    entregas = gerar_entregas(100)
    grafo = preparar_grafo(cidades_centros)

    tracemalloc.start()
    inicio = time.perf_counter()

    roteirizador = Roteirizador(centros, entregas, grafo)
    resultado = roteirizador.alocar_entregas()

    fim = time.perf_counter()
    mem_atual, mem_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n✅ Roteirização (matriz) concluída para 100 entregas.")
    print(f"⏱️ Tempo de execução: {fim - inicio:.4f} segundos")
    print(f"💾 Uso de memória atual: {mem_atual/1024:.2f} KB")
    print(f"📈 Pico de memória: {mem_pico/1024:.2f} KB")
    print(f"Entregas com sucesso: {sum(1 for r in resultado if 'erro' not in r)}")
    print(f"Entregas com erro: {sum(1 for r in resultado if 'erro' in r)}\n")

if __name__ == "__main__":
    import tracemalloc
    testar_desempenho()
