import time
import tracemalloc
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

from model.entrega import Entrega
from model.caminhao import Caminhao
from model.centro_distribuicao import CentroDistribuicao
from model.grafoDicionario import GrafoDicionario
from controller.roteirizador import Roteirizador

def gerar_entregas(qtd: int) -> list:
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
    cidades = ["Belém", "Recife", "Brasília", "São Paulo", "Florianópolis"]
    centros = []
    for cidade in cidades:
        centro = CentroDistribuicao(cidade)
        for j in range(10):
            cam = Caminhao(f"{cidade[:2]}-{j+1}", 6000, 22)
            centro.adicionar_caminhao(cam)
        centros.append(centro)
    return centros

def preparar_grafo() -> GrafoDicionario:
    g = GrafoDicionario()
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
    g.adicionar_aresta("Belém", "Brasília", 12)
    g.adicionar_aresta("Recife", "Brasília", 10)
    g.adicionar_aresta("Brasília", "São Paulo", 8)
    g.adicionar_aresta("São Paulo", "Florianópolis", 6)
    return g

def executar_teste(qtd_entregas: int) -> dict:
    centros = preparar_centros()
    entregas = gerar_entregas(qtd_entregas)
    grafo = preparar_grafo()

    tracemalloc.start()
    inicio = time.perf_counter()

    roteirizador = Roteirizador(centros, entregas, grafo)
    resultado = roteirizador.alocar_entregas()

    fim = time.perf_counter()
    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    erros = [rota["erro"] for rota in resultado if "erro" in rota]
    tot_erros = len(erros)
    tot_sucessos = qtd_entregas - tot_erros

    return {
        "estrutura": "Dicionário de Dicionários",
        "qtd_entregas": qtd_entregas,
        "tempo": fim - inicio,
        "memoria_atual_kb": memoria_atual / 1024,
        "memoria_pico_kb": memoria_pico / 1024,
        "sucessos": tot_sucessos,
        "erros": tot_erros
    }

if __name__ == "__main__":
    for qtd in [10, 50, 100, 200]:
        resultado = executar_teste(qtd)
        print(f"\n🔹 {resultado['estrutura']} com {qtd} entregas:")
        print(f"   ⏱️ Tempo: {resultado['tempo']:.4f}s")
        print(f"   💾 Memória atual: {resultado['memoria_atual_kb']:.2f} KB")
        print(f"   📈 Pico de memória: {resultado['memoria_pico_kb']:.2f} KB")
        print(f"   ✅ Sucesso: {resultado['sucessos']} | ❌ Erros: {resultado['erros']}")
