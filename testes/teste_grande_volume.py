import time
import tracemalloc
import random

from model.entrega import Entrega
from model.caminhao import Caminhao
from model.centro_distribuicao import CentroDistribuicao
from model.grafo import Grafo
from controller.roteirizador import Roteirizador


def gerar_entregas(qtd):
    """
    Gera uma lista de objetos Entrega com dados aleatórios.

    Args:
        qtd (int): Quantidade de entregas a serem geradas.

    Returns:
        list: Lista de objetos Entrega.
    """
    destinos = [
        "Salvador", "Fortaleza", "Manaus", "Porto Alegre", "Curitiba",
        "Rio de Janeiro", "Vitória", "Goiânia", "Campo Grande", "Natal"
    ]
    entregas = []
    for i in range(qtd):
        destino = random.choice(destinos)
        peso = random.randint(500, 3000)
        prazo = random.randint(8, 24)
        entregas.append(Entrega(f"E{i:03d}", destino, peso, prazo))
    return entregas


def preparar_centros():
    """
    Cria centros de distribuição com caminhões alocados.

    Returns:
        list: Lista de objetos CentroDistribuicao com caminhões.
    """
    cidades = ["Belém", "Recife", "Brasília", "São Paulo", "Florianópolis"]
    centros = []
    for cidade in cidades:
        centro = CentroDistribuicao(cidade)
        # Adiciona 4 caminhões por centro
        for j in range(4):
            cam = Caminhao(f"{cidade[:2]}-{j+1}", 6000, 22)
            centro.adicionar_caminhao(cam)
        centros.append(centro)
    return centros


def preparar_grafo():
    """
    Cria um grafo com as conexões entre centros e destinos, simulando distâncias (em horas).

    Returns:
        Grafo: Objeto grafo com as arestas definidas.
    """
    g = Grafo()
    # Ligações principais entre centros e destinos (tempo em horas)
    g.adicionar_aresta("Belém", "Manaus", 10)
    g.adicionar_aresta("Recife", "Fortaleza", 5)
    g.adicionar_aresta("Recife", "Salvador", 6)
    g.adicionar_aresta("Brasília", "Salvador", 7)
    g.adicionar_aresta("São Paulo", "Curitiba", 4)
    g.adicionar_aresta("Florianópolis", "Curitiba", 3)
    g.adicionar_aresta("Florianópolis", "Porto Alegre", 5)
    g.adicionar_aresta("São Paulo", "Porto Alegre", 7)
    g.adicionar_aresta("Brasília", "Goiânia", 4)
    g.adicionar_aresta("Brasília", "Campo Grande", 9)
    g.adicionar_aresta("São Paulo", "Rio de Janeiro", 6)
    g.adicionar_aresta("São Paulo", "Vitória", 8)
    g.adicionar_aresta("Recife", "Natal", 4)

    # Ligações entre centros
    g.adicionar_aresta("Belém", "Brasília", 12)
    g.adicionar_aresta("Recife", "Brasília", 10)
    g.adicionar_aresta("Brasília", "São Paulo", 8)
    g.adicionar_aresta("São Paulo", "Florianópolis", 6)

    return g


def testar_desempenho():
    """
    Executa um teste de desempenho com 100 entregas, medindo tempo e uso de memória.

    O teste simula centros, entregas, e o grafo de conexões. Roda o algoritmo de roteirização
    e imprime os resultados de desempenho e alocação de entregas.
    """
    centros = preparar_centros()
    entregas = gerar_entregas(100)
    grafo = preparar_grafo()

    tracemalloc.start()
    inicio = time.perf_counter()

    roteirizador = Roteirizador(centros, entregas, grafo)
    resultado = roteirizador.alocar_entregas()

    fim = time.perf_counter()
    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n✅ Roteirização concluída para 100 entregas.")
    print(f"⏱️ Tempo de execução: {fim - inicio:.4f} segundos")
    print(f"💾 Uso de memória atual: {memoria_atual / 1024:.2f} KB")
    print(f"📈 Pico de memória: {memoria_pico / 1024:.2f} KB")
    print(f"Entregas com sucesso: {sum(1 for r in resultado if 'erro' not in r)}")
    print(f"Entregas com erro: {sum(1 for r in resultado if 'erro' in r)}\n")


if __name__ == "__main__":
    testar_desempenho()
