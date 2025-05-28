import time, tracemalloc, os, sys

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

from model.entrega import Entrega
from model.centro_distribuicao import CentroDistribuicao
from model.grafoListaAdjacencia import GrafoListaAdjacencia
from controller.roteirizador import Roteirizador

def preparar_grafo(arestas_mapa: list[tuple[str, str, int]]) -> GrafoListaAdjacencia:
    """
    Recebe uma lista de arestas e as adiciona no grafo com lista de adjacência.
    """
    g = GrafoListaAdjacencia(tipo_fila_dijkstra='heap')
    for origem, destino, peso in arestas_mapa:
        g.adicionar_aresta(origem, destino, peso)
    return g

def executar_teste(centros: list[CentroDistribuicao], 
                   entregas: list[Entrega], 
                   arestas_mapa: list[tuple[str, str, int]], 
                   todas_cidades_mapa: list[str],
                   mostrar_erros: bool=False) -> dict:
    """
    Executa o teste com grafo baseado em Lista de Adjacência, medindo tempo e memória.
    """
    grafo_teste = preparar_grafo(arestas_mapa)

    tracemalloc.start()
    inicio_tempo = time.perf_counter()

    roteirizador = Roteirizador(centros, entregas, grafo_teste)
    resultado_alocacao = roteirizador.alocar_entregas()

    fim_tempo = time.perf_counter() # Renomeado
    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    erros_lista = [r for r in resultado_alocacao if "erro" in r] # Renomeado

    if mostrar_erros and erros_lista:
        print(f"\n  Erros encontrados em 'Lista de Adjacência (Heap)' com {len(entregas)} entregas:")
        for item_erro in erros_lista: # Renomeado
            # Acessar a entrega e a lista de motivos de erro
            entrega_obj = item_erro["entrega"]
            motivos = item_erro["erro"] # Que agora é uma lista de strings
            print(f"    - Entrega {entrega_obj.id} (Dest: {entrega_obj.destino}):")
            if isinstance(motivos, list):
                for m in motivos:
                    print(f"      - {m}")
            else: # Fallback se ainda for string
                print(f"      - {motivos}")


    return {
        "estrutura": "Lista de Adjacência (Heap)", # Nome descritivo
        "qtd_entregas": len(entregas),
        "tempo": fim_tempo - inicio_tempo,
        "memoria_pico_kb": memoria_pico / 1024,
        "sucessos": len(entregas) - len(erros_lista),
        "erros": len(erros_lista),
    }

