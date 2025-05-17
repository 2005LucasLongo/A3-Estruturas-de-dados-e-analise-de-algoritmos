import os, sys
from tabulate import tabulate
from time import sleep

raiz = os.path.abspath(os.path.join(__file__, "..", ".."))
if raiz not in sys.path:
    sys.path.append(raiz)

from testes import teste_dicionario, teste_lista_adjacencia, teste_lista_arestas, teste_matriz_ajacencia, teste_networkx, teste_oo
from utils.gerador_entregas import gerar_entregas
from utils.mapa_logistico import obter_estrutura_mapa, criar_centros_distribuicao, adicionar_frota_padrao

def obter_modulos_teste():
    return {
        "Lista de Adjacência": teste_lista_adjacencia,
        "Matriz de Adjacência": teste_matriz_ajacencia,
        "Lista de Arestas": teste_lista_arestas,
        "Dicionário de Dicionários": teste_dicionario,
        "Grafo com Objetos": teste_oo,
        "NetworkX": teste_networkx,
    }


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

def exibir_resultados(resultados):
    headers = ["Estrutura", "Entregas", "Tempo (s)", "Memória Pico (KB)", "Sucesso", "Erros"]
    print("\n📊 Resultados Comparativos:")
    for resutlado in range(0, len(resultados), len(resultados[0])):
        print(tabulate(resultados[resutlado:resutlado + len(resultados[0])], headers=headers, tablefmt="fancy_grid"))
        sleep(2)

def comparar_algoritmos():
    cenarios = obter_modulos_teste()
    quantidades = [ 
        10, 
        100,
        # 1000
    ]
    resultados = executar_testes_em_lote(cenarios, quantidades)
    if resultados:
        exibir_resultados(resultados)

if __name__ == "__main__":
    comparar_algoritmos()
