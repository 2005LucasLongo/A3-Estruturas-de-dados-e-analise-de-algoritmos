import os, sys
from tabulate import tabulate
import time 
import tracemalloc 

raiz = os.path.abspath(os.path.join(__file__, "..", ".."))
if raiz not in sys.path:
    sys.path.append(raiz)

from model.entrega import Entrega
from model.centro_distribuicao import CentroDistribuicao
from model.grafoListaAdjacencia import GrafoListaAdjacencia
from model.grafoMatrizAdjacencia import GrafoMatrizAdjacencia
from model.grafoListaArestas import GrafoListaArestas
from model.grafoDicionario import GrafoDicionario
from model.grafoOrientado import GrafoOrientado
from model.grafoNetworkX import GrafoNetworkX
from controller.roteirizador import Roteirizador


from utils.gerador_entregas import gerar_entregas
from utils.mapa_logistico import obter_estrutura_mapa, criar_centros_distribuicao, adicionar_frota_padrao

def obter_configuracoes_teste():
    """Retorna uma lista de dicionários, cada um definindo uma configuração de teste."""
    return [
        {
            "nome_estrutura": "Lista de Adjacência (Heap)",
            "classe_grafo": GrafoListaAdjacencia,
            "tipo_fila_dijkstra": "heap"
        },
        {
            "nome_estrutura": "Lista de Adjacência (Lista Simples)",
            "classe_grafo": GrafoListaAdjacencia,
            "tipo_fila_dijkstra": "lista"
        },
        {
            "nome_estrutura": "Matriz de Adjacência (Heap)",
            "classe_grafo": GrafoMatrizAdjacencia,
            "tipo_fila_dijkstra": "heap"
        },
        {
            "nome_estrutura": "Matriz de Adjacência (Lista Simples)",
            "classe_grafo": GrafoMatrizAdjacencia,
            "tipo_fila_dijkstra": "lista"
        },
        {
            "nome_estrutura": "Lista de Arestas (Heap)",
            "classe_grafo": GrafoListaArestas,
            "tipo_fila_dijkstra": "heap",
            "requer_lista_cidades_init": False
        },
        {
            "nome_estrutura": "Lista de Arestas (Lista Simples)",
            "classe_grafo": GrafoListaArestas,
            "tipo_fila_dijkstra": "lista",
            "requer_lista_cidades_init": False
        },
        {
            "nome_estrutura": "Dicionário de Dicionários (Heap)",
            "classe_grafo": GrafoDicionario,
            "tipo_fila_dijkstra": "heap",
            "requer_lista_cidades_init": False
        },
        {
            "nome_estrutura": "Dicionário de Dicionários (Lista Simples)",
            "classe_grafo": GrafoDicionario, 
            "tipo_fila_dijkstra": "lista",
            "requer_lista_cidades_init": False
        },
        {
            "nome_estrutura": "Grafo com Objetos (Heap)",
            "classe_grafo": GrafoOrientado,
            "tipo_fila_dijkstra": "heap",
            "requer_lista_cidades_init": False
        },
        {
            "nome_estrutura": "Grafo com Objetos (Lista Simples)",
            "classe_grafo": GrafoOrientado,
            "tipo_fila_dijkstra": "lista",
            "requer_lista_cidades_init": False
        },
        {
            "nome_estrutura": "NetworkX (Nativo/Heap)",
            "classe_grafo": GrafoNetworkX, 
            "tipo_fila_dijkstra": "nativo_nx_heap",
            "requer_lista_cidades_init": False
        },
    ]

def executar_testes_em_lote(cenarios, quantidades):
    centros, arestas, destinos = obter_estrutura_mapa()
    adicionar_frota_padrao(centros, max(quantidades) * 2)
    resultados = []
    print("🔍 Comparando desempenho dos algoritmos de roteirização:\n")

    for qtd in quantidades:
        entregas = gerar_entregas(qtd, destinos)

        print(f"📦 Testando com {qtd} entregas:")
        for nome, modulo in cenarios.items():
            try:
                resultado = modulo.executar_teste(
                    centros=centros,
                    arestas=arestas,
                    entregas=entregas,
                    mostrar_erros=True,
                )
                resultados.append([
                    resultado["estrutura"],
                    resultado["qtd_entregas"],
                    resultado["tempo"],
                    resultado["memoria_pico_kb"],
                    resultado["sucessos"],
                    resultado["erros"]
                ])
            except Exception as e:
                print(f"❌ Erro ao executar {nome} com {qtd} entregas: {e}")

        # resultados.append(["---", "---", "---", "---", "---", "---"])

    return resultados

def executar_teste_configurado(config: dict,
                               centros_teste: list[CentroDistribuicao],
                               entregas_teste: list[Entrega],
                               arestas_mapa: list[tuple[str, str, int]],
                               todas_cidades_mapa: list[str], # Necessário para GrafoMatrizAdjacencia
                               mostrar_erros: bool = False) -> dict:
    """
    Executa um teste de roteirização para uma configuração específica de grafo,
    medindo tempo e memória.
    """
    ClasseGrafo = config["classe_grafo"]
    tipo_fila = config["tipo_fila_dijkstra"]
    nome_estrutura_teste = config["nome_estrutura"]

    # Preparar o grafo conforme a configuração
    if ClasseGrafo == GrafoMatrizAdjacencia:
        # Matriz de Adjacência precisa da lista de todas as cidades no construtor
        grafo_teste = ClasseGrafo(cidades=todas_cidades_mapa, tipo_fila_dijkstra=tipo_fila)
    else: # Lista de Adjacência
        grafo_teste = ClasseGrafo(tipo_fila_dijkstra=tipo_fila)

    for origem, destino, peso in arestas_mapa:
        grafo_teste.adicionar_aresta(origem, destino, peso)

    # Medição
    tracemalloc.start()
    inicio_tempo = time.perf_counter()

    roteirizador = Roteirizador(centros_teste, entregas_teste, grafo_teste)
    resultado_alocacao = roteirizador.alocar_entregas()

    fim_tempo = time.perf_counter()
    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    erros_lista = [r for r in resultado_alocacao if "erro" in r]

    if mostrar_erros and erros_lista:
        print(f"\n  Erros encontrados em '{nome_estrutura_teste}' com {len(entregas_teste)} entregas:")
        for item_erro in erros_lista:
            entrega_obj = item_erro["entrega"]
            motivos = item_erro["erro"]
            print(f"    - Entrega {entrega_obj.id} (Dest: {entrega_obj.destino}):")
            if isinstance(motivos, list):
                for m in motivos: print(f"      - {m}")
            else: print(f"      - {motivos}")
    
    return {
        "estrutura": nome_estrutura_teste,
        "qtd_entregas": len(entregas_teste),
        "tempo": fim_tempo - inicio_tempo,
        "memoria_pico_kb": memoria_pico / 1024,
        "sucessos": len(entregas_teste) - len(erros_lista),
        "erros": len(erros_lista),
    }

# 3. Função Principal de Execução dos Lotes de Teste (Modificada)
def executar_testes_em_lote(configuracoes_para_teste: list,
                              quantidades_entregas: list,
                              num_caminhoes_por_cd_fixo: int):
    
    _, arestas_mapa, lista_nomes_destinos_entregas = obter_estrutura_mapa()
    
    set_cidades_mapa = set()
    for o, d, _ in arestas_mapa:
        set_cidades_mapa.add(o)
        set_cidades_mapa.add(d)
    temp_centros_obj_mapa, _, _ = obter_estrutura_mapa() # Para pegar nomes de cidades dos centros
    for centro_obj_mapa in temp_centros_obj_mapa:
        set_cidades_mapa.add(centro_obj_mapa.cidade)
    for dest_entrega_mapa in lista_nomes_destinos_entregas:
        set_cidades_mapa.add(dest_entrega_mapa)
    todas_cidades_mapa_lista = sorted(list(set_cidades_mapa))

    resultados_gerais = []
    print("🔍 Comparando desempenho dos algoritmos de roteirização:\n")

    for qtd_entregas_teste in quantidades_entregas:
        print(f"--- CENÁRIO: {qtd_entregas_teste} Entregas, {num_caminhoes_por_cd_fixo} Caminhões por Centro de Distribuição ---\n")
        
        entregas_teste_cenario = gerar_entregas(qtd_entregas_teste, lista_nomes_destinos_entregas)

        for config_atual in configuracoes_para_teste: # Agora itera sobre as configurações
            print(f"  Testando Estrutura: {config_atual['nome_estrutura']}...")
            
            # Recriar centros e caminhões para cada configuração de teste para estado limpo
            centros_para_teste_config = criar_centros_distribuicao()
            adicionar_frota_padrao(centros_para_teste_config, num_caminhoes_por_cd_fixo)

            try:
                # Chama a função generalizada de teste
                resultado_individual = executar_teste_configurado(
                    config=config_atual,
                    centros_teste=centros_para_teste_config,
                    entregas_teste=entregas_teste_cenario,
                    arestas_mapa=arestas_mapa,
                    todas_cidades_mapa=todas_cidades_mapa_lista,
                    mostrar_erros=False # Mantenha False para medição de desempenho
                )
                resultados_gerais.append([
                    resultado_individual["estrutura"],
                    resultado_individual["qtd_entregas"],
                    f"{resultado_individual['tempo']:.4f}",
                    f"{resultado_individual['memoria_pico_kb']:.2f}",
                    resultado_individual["sucessos"],
                    resultado_individual["erros"]
                ])
                print(f"    Tempo: {resultado_individual['tempo']:.4f}s, Memória Pico: {resultado_individual['memoria_pico_kb']:.2f}KB")
            except Exception as e:
                print(f"❌ Erro ao executar {config_atual['nome_estrutura']} com {qtd_entregas_teste} entregas: {e}")
                import traceback
                traceback.print_exc()
                resultados_gerais.append([config_atual['nome_estrutura'], qtd_entregas_teste, "ERRO", "ERRO", "ERRO", "ERRO"])
            print()
    return resultados_gerais

# 4. Função para Exibir Resultados (Pode permanecer a mesma)
def exibir_resultados_tabulados(resultados_lista_de_listas):
    headers = ["Estrutura", "Nº Entregas", "Tempo (s)", "Memória Pico (KB)", "Sucessos", "Erros"]
    print("\n📊 Resultados Comparativos Consolidados:")
    print(tabulate(resultados_lista_de_listas, headers=headers, tablefmt="fancy_grid"))
    # O sleep(2) foi removido da sua versão anterior, pode ser omitido ou adicionado se desejado.

# 5. Função Principal para Orquestrar a Comparação (Modificada)
def comparar_algoritmos_estruturas():
    configs_de_teste = obter_configuracoes_teste() # Obtém as novas configurações
    
    quantidades_entregas_cenarios = [
        10, 
        50, 
        # 100,
    ]
    numero_caminhoes_por_cd_teste = max(quantidades_entregas_cenarios) # Número fixo de caminhões para isolar o teste de estrutura

    import random
    random.seed(42) # Seed para reprodutibilidade da geração de dados

    resultados_compilados = executar_testes_em_lote(
        configs_de_teste, 
        quantidades_entregas_cenarios,
        numero_caminhoes_por_cd_teste
    )
    
    if resultados_compilados:
        exibir_resultados_tabulados(resultados_compilados)

if __name__ == "__main__":
    comparar_algoritmos_estruturas()