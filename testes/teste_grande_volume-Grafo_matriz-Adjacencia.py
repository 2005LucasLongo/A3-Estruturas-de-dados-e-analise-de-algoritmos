import time
import tracemalloc
import random
import os, sys

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

from model.entrega import Entrega
from model.caminhao import Caminhao
from model.centro_distribuicao import CentroDistribuicao
from model.grafoMatrizAdjacencia import GrafoMatrizAdjacencia
from controller.roteirizador import Roteirizador

def gerar_entregas(qtd: int) -> list:
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


def preparar_centros() -> list:
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
        for j in range(10):
            cam = Caminhao(f"{cidade[:2]}-{j+1}", 6000, 22)
            centro.adicionar_caminhao(cam)
        centros.append(centro)
    return centros


def preparar_grafo_matriz() -> GrafoMatrizAdjacencia:
    """
    Cria um grafo com a representação de matriz de adjacência para as conexões.
    """
    cidades = [
        "Belém", "Recife", "Brasília", "São Paulo", "Florianópolis",
        "Manaus", "Fortaleza", "Porto Alegre", "Curitiba", "Rio de Janeiro", 
        "Vitória", "Goiânia", "Campo Grande", "Natal", "Salvador"
    ]
    grafo = GrafoMatrizAdjacencia(cidades)
    # Adiciona as arestas ao grafo
    grafo.adicionar_aresta("Belém", "Manaus", 10)
    grafo.adicionar_aresta("Recife", "Fortaleza", 5)
    grafo.adicionar_aresta("Recife", "Salvador", 6)
    grafo.adicionar_aresta("Brasília", "Salvador", 7)
    grafo.adicionar_aresta("São Paulo", "Curitiba", 4)
    grafo.adicionar_aresta("Florianópolis", "Curitiba", 3)
    grafo.adicionar_aresta("Florianópolis", "Porto Alegre", 5)
    grafo.adicionar_aresta("São Paulo", "Porto Alegre", 7)
    grafo.adicionar_aresta("Brasília", "Goiânia", 4)
    grafo.adicionar_aresta("Brasília", "Campo Grande", 9)
    grafo.adicionar_aresta("São Paulo", "Rio de Janeiro", 6)
    grafo.adicionar_aresta("São Paulo", "Vitória", 8)
    grafo.adicionar_aresta("Recife", "Natal", 4)
    grafo.adicionar_aresta("Belém", "Brasília", 12)
    grafo.adicionar_aresta("Recife", "Brasília", 10)
    grafo.adicionar_aresta("Brasília", "São Paulo", 8)
    grafo.adicionar_aresta("São Paulo", "Florianópolis", 6)

    return grafo


def testar_desempenho(qtd_entregas: int, mostrar_erros: bool=False) -> tuple[int, int]:
    """
    Executa um teste de desempenho com 100 entregas, medindo tempo e uso de memória.

    O teste simula centros, entregas, e o grafo de conexões. Roda o algoritmo de roteirização
    e imprime os resultados de desempenho e alocação de entregas.
    """
    centros = preparar_centros()
    entregas = gerar_entregas(qtd_entregas)
    grafo = preparar_grafo_matriz()

    tracemalloc.start()
    inicio = time.perf_counter()

    roteirizador = Roteirizador(centros, entregas, grafo)
    resultado = roteirizador.alocar_entregas()

    fim = time.perf_counter()
    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    erros = [rota["erro"] for rota in resultado if "erro" in rota]
    tot_erros = len(erros)
    tot_sucessos = qtd_entregas - len(erros)

    print(f"\n📝 Roteirização concluída para {qtd_entregas} entregas.")
    print(f"⏱️ Tempo de execução: {fim - inicio:.4f} segundos")
    print(f"💾 Uso de memória atual: {memoria_atual / 1024:.2f} KB")
    print(f"📈 Pico de memória: {memoria_pico / 1024:.2f} KB")
    print(f"✅ Entregas com sucesso: {tot_sucessos} | ({tot_sucessos/qtd_entregas:.2%})")
    print(f"❌ Entregas com erro: {tot_erros} | ({tot_erros/qtd_entregas:.2%}\n")

    if mostrar_erros and erros:
        print(*[rota["erro"] + " com ID " + rota["entrega"].id for rota in resultado if "erro" in rota], sep="\n")

    return tot_sucessos, tot_erros


if __name__ == "__main__":
    for qtd in [10, 50, 100, 200]:
        testar_desempenho(qtd)
