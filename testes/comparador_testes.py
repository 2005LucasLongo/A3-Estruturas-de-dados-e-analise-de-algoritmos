import os
import sys
import importlib
from tabulate import tabulate

# Adiciona raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))

# Define os módulos de teste que você quer comparar
cenarios = {
    "Lista de Adjacência": "testes.teste_lista_adjacencia",
    "Matriz de Adjacência": "testes.teste_matriz_ajacencia"
}

quantidades = [10, 50, 100, 200]
resultados = []

print("🔍 Comparando desempenho dos algoritmos de roteirização:\n")

for qtd in quantidades:
    print(f"\n📦 Testando com {qtd} entregas:\n")
    for nome, modulo_path in cenarios.items():
        try:
            modulo = importlib.import_module(modulo_path)
            print(f"Executando {nome}...")
            resultado = modulo.executar_teste(qtd)
            resultados.append(
                [
                    resultado["estrutura"], 
                    resultado["qtd_entregas"], 
                    resultado["tempo"], 
                    resultado["memoria_pico_kb"], 
                    resultado["sucessos"], 
                    resultado["erros"]
                ]
            )
        except Exception as e:
            print(f"Erro ao executar {nome} com {qtd} entregas: {e}")

# Apresentar os resultados
print("\n📊 Resultados Comparativos:")
headers = ["Estrutura", "Entregas", "Tempo (s)", "Memória Pico (KB)", "Sucesso", "Erros"]
print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
