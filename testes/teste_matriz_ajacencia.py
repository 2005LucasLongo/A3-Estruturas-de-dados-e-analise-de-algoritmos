import time, tracemalloc, os, sys

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

from model.entrega import Entrega
from model.centro_distribuicao import CentroDistribuicao
from model.grafoMatrizAdjacencia import GrafoMatrizAdjacencia
from controller.roteirizador import Roteirizador

def preparar_grafo(arestas: list[tuple[str, str, int]]) -> GrafoMatrizAdjacencia:
    """
    Cria um grafo com matriz de adjacência usando as arestas fornecidas.
    """
    cidades = set()
    for origem, destino, _ in arestas:
        cidades.add(origem)
        cidades.add(destino)

    g = GrafoMatrizAdjacencia(sorted(cidades))
    for origem, destino, peso in arestas:
        g.adicionar_aresta(origem, destino, peso)
    return g


def executar_teste(centros: list[CentroDistribuicao], entregas: list[Entrega], arestas: list[tuple[str, str, int]], mostrar_erros: bool=False) -> dict:
    """
    Executa o teste com grafo baseado em matriz de adjacência, medindo tempo e memória.
    """
    grafo = preparar_grafo(arestas)

    tracemalloc.start()
    inicio = time.perf_counter()

    roteirizador = Roteirizador(centros, entregas, grafo)
    resultado = roteirizador.alocar_entregas()

    fim = time.perf_counter()
    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    erros = [r for r in resultado if "erro" in r]

    if mostrar_erros:
        for item in erros:
            print(f"{item['erro']} {item['entrega'].id}")
    
    return {
        "estrutura": "Matriz de Adjacência",
        "qtd_entregas": len(entregas),
        "tempo": fim - inicio,
        "memoria_atual_kb": memoria_atual / 1024,
        "memoria_pico_kb": memoria_pico / 1024,
        "sucessos": len(entregas) - len(erros),
        "erros": len(erros),
    }
