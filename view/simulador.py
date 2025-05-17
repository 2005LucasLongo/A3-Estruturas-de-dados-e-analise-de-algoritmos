import sys, os
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

from model.entrega import Entrega
from model.caminhao import Caminhao
from model.centro_distribuicao import CentroDistribuicao
from model.grafoListaAdjacencia import GrafoListaAdjacenceia
from controller.roteirizador import Roteirizador
from utils.mapa_logistico import criar_centros_distribuicao, adicionar_frota_padrao, obter_estrutura_mapa
from utils.gerador_entregas import gerar_entregas
from time import sleep

def simular():
    """
    Função que simula o processo de roteirização de entregas a partir de centros de distribuição, caminhões e
    distâncias entre as cidades. Realiza a alocação de entregas aos centros e caminhões disponíveis e exibe os
    resultados da simulação.

    Passos realizados pela função:
    1. Criação de Centros de Distribuição e adição de caminhões a cada centro.
    2. Criação de entregas, especificando ID, destino, carga e tempo estimado de entrega.
    3. Criação de um grafo com distâncias fictícias entre as cidades.
    4. Execução do roteirizador para alocar as entregas aos caminhões disponíveis.
    5. Exibição dos resultados, incluindo o sucesso ou erro de cada entrega.

    Exibe:
        - Para cada entrega, o status (OK ou erro).
        - O centro de distribuição alocado.
        - O caminhão alocado.
        - A rota seguida.
        - O tempo estimado de entrega.
    """

    # 1. Criar Centros de Distribuição e caminhões
    centros, arestas, destinos = obter_estrutura_mapa()

    # Adiciona 2 caminhões por centro
    adicionar_frota_padrao(centros, 2)

    # 2. Criar entregas
    entregas = gerar_entregas(10, destinos)

    # 3. Criar o grafo completo com todas as cidades e conexões reais
    grafo = GrafoListaAdjacenceia()

    # Adiciona as arestas com base no mapa logístico
    for origem, destino, tempo in arestas:
        grafo.adicionar_aresta(origem, destino, tempo)

    # 4. Executar o roteirizador
    roteirizador = Roteirizador(centros, entregas, grafo)
    resultado = roteirizador.alocar_entregas()

    # 5. Exibir resultados
    print("RESULTADO DA SIMULAÇÃO:\n")
    for item in resultado:
        entrega = item["entrega"]
        if "erro" in item:
            print(f"[ERRO] {entrega.id}: {item['erro']}")
        else:
            print(f"[OK] {entrega}")
            print(f"     Centro: {item['centro']}")
            print(f"     Caminhão: {item['caminhao']}")
            print(f"     Rota: {' → '.join(item['rota'])}")
            print(f"     Tempo estimado: {item['tempo']}h\n")
    
        sleep(2)

if __name__ == "__main__":
    simular()
