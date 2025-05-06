import os
import sys
import importlib
from tabulate import tabulate

def adicionar_raiz_ao_path():
    raiz = os.path.abspath(os.path.join(__file__, "..", ".."))
    if raiz not in sys.path:
        sys.path.append(raiz)

def obter_modulos_teste():
    return {
        "Lista de Adjacência": "testes.teste_lista_adjacencia",
        "Matriz de Adjacência": "testes.teste_matriz_ajacencia"
    }

def executar_testes_em_lote(cenarios, quantidades):
    resultados = []
    print("🔍 Comparando desempenho dos algoritmos de roteirização:\n")

    for qtd in quantidades:
        print(f"📦 Testando com {qtd} entregas:\n")
        for nome, modulo_path in cenarios.items():
            try:
                modulo = importlib.import_module(modulo_path)
                print(f"Executando {nome}...")
                resultado = modulo.executar_teste(qtd)
                resultados.append([
                    resultado["estrutura"],
                    resultado["qtd_entregas"],
                    resultado["tempo"],
                    resultado["memoria_pico_kb"],
                    resultado["sucessos"],
                    resultado["erros"]
                ])
            except Exception as e:
                print(f"Erro ao executar {nome} com {qtd} entregas: {e}")
    return resultados

def exibir_resultados(resultados):
    headers = ["Estrutura", "Entregas", "Tempo (s)", "Memória Pico (KB)", "Sucesso", "Erros"]
    print("📊 Resultados Comparativos:")
    print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))

def comparar_algoritmos():
    adicionar_raiz_ao_path()
    cenarios = obter_modulos_teste()
    quantidades = [10, 50, 100, 200]
    resultados = executar_testes_em_lote(cenarios, quantidades)
    exibir_resultados(resultados)

if __name__ == "__main__":
    comparar_algoritmos()
