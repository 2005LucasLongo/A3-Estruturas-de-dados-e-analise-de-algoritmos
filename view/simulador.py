import sys, os
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

from model.entrega import Entrega
from model.caminhao import Caminhao
from model.centro_distribuicao import CentroDistribuicao
from model.grafoListaAdjacencia import GrafoListaAdjacenceia
from controller.roteirizador import Roteirizador



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
    centros = [
        CentroDistribuicao("Belém"),
        CentroDistribuicao("Recife"),
        CentroDistribuicao("Brasília"),
        CentroDistribuicao("São Paulo"),
        CentroDistribuicao("Florianópolis")
    ]

    # Adiciona 2 caminhões por centro
    for i, centro in enumerate(centros):
        centro.adicionar_caminhao(Caminhao(f"{centro.cidade[:2]}-01", 5000, 20))
        centro.adicionar_caminhao(Caminhao(f"{centro.cidade[:2]}-02", 4000, 18))

    # 2. Criar entregas
    entregas = [
        Entrega("E01", "Salvador", 1200, 12),
        Entrega("E02", "Curitiba", 2000, 14),
        Entrega("E03", "Manaus", 800, 20),
        Entrega("E04", "Porto Alegre", 2500, 16),
        Entrega("E05", "Fortaleza", 1500, 10)
    ]

    # 3. Criar o grafo com distâncias fictícias (em horas)
    g = GrafoListaAdjacenceia()
    # Conexões entre centros e destinos
    g.adicionar_aresta("Belém", "Manaus", 10)
    g.adicionar_aresta("Recife", "Fortaleza", 5)
    g.adicionar_aresta("Recife", "Salvador", 6)
    g.adicionar_aresta("Brasília", "Salvador", 7)
    g.adicionar_aresta("São Paulo", "Curitiba", 4)
    g.adicionar_aresta("Florianópolis", "Curitiba", 3)
    g.adicionar_aresta("Florianópolis", "Porto Alegre", 5)
    g.adicionar_aresta("São Paulo", "Porto Alegre", 7)

    # Conexões entre centros (para rotas compostas)
    g.adicionar_aresta("Belém", "Brasília", 12)
    g.adicionar_aresta("Recife", "Brasília", 10)
    g.adicionar_aresta("Brasília", "São Paulo", 8)
    g.adicionar_aresta("São Paulo", "Florianópolis", 6)

    # 4. Executar o roteirizador
    roteirizador = Roteirizador(centros, entregas, g)
    resultado = roteirizador.alocar_entregas()

    # 5. Exibir resultados
    print("RESULTADO DA SIMULAÇÃO:\n")
    for item in resultado:
        entrega = item["entrega"]
        if "erro" in item:
            print(f"[ERRO] {entrega.id}: {item['erro']}")
        else:
            print(f"[OK] {entrega.id} - {entrega.destino}")
            print(f"     Centro: {item['centro']}")
            print(f"     Caminhão: {item['caminhao'].id}")
            print(f"     Rota: {' → '.join(item['rota'])}")
            print(f"     Tempo estimado: {item['tempo']}h\n")

if __name__ == "__main__":
    simular()
