import sys, os
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

from model.entrega import Entrega
from model.caminhao import Caminhao
from model.centro_distribuicao import CentroDistribuicao
from model.grafoListaAdjacencia import GrafoListaAdjacenceia
from controller.roteirizador import Roteirizador
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

    # Região Norte
    g.adicionar_aresta("Rio Branco", "Porto Velho", 5)
    g.adicionar_aresta("Porto Velho", "Manaus", 8)
    g.adicionar_aresta("Manaus", "Boa Vista", 6)
    g.adicionar_aresta("Manaus", "Macapá", 10)
    g.adicionar_aresta("Macapá", "Belém", 6)

    # Região Nordeste
    g.adicionar_aresta("São Luís", "Teresina", 4)
    g.adicionar_aresta("Teresina", "Fortaleza", 6)
    g.adicionar_aresta("Fortaleza", "Natal", 4)
    g.adicionar_aresta("Natal", "João Pessoa", 2)
    g.adicionar_aresta("João Pessoa", "Recife", 2)
    g.adicionar_aresta("Recife", "Maceió", 3)
    g.adicionar_aresta("Maceió", "Aracaju", 3)
    g.adicionar_aresta("Aracaju", "Salvador", 4)

    # Conexões Norte/Nordeste/Centro-Oeste
    g.adicionar_aresta("Belém", "Palmas", 10)
    g.adicionar_aresta("Palmas", "Brasília", 6)
    g.adicionar_aresta("São Luís", "Palmas", 8)
    g.adicionar_aresta("Salvador", "Brasília", 7)
    g.adicionar_aresta("Fortaleza", "Brasília", 12)

    # Região Centro-Oeste
    g.adicionar_aresta("Brasília", "Goiânia", 2)
    g.adicionar_aresta("Goiânia", "Cuiabá", 7)
    g.adicionar_aresta("Cuiabá", "Campo Grande", 5)
    g.adicionar_aresta("Campo Grande", "Brasília", 8)

    # Região Sudeste
    g.adicionar_aresta("Brasília", "Belo Horizonte", 5)
    g.adicionar_aresta("Belo Horizonte", "Rio de Janeiro", 5)
    g.adicionar_aresta("Belo Horizonte", "Vitória", 4)
    g.adicionar_aresta("Rio de Janeiro", "Vitória", 6)
    g.adicionar_aresta("Rio de Janeiro", "São Paulo", 4)

    # Região Sul
    g.adicionar_aresta("São Paulo", "Curitiba", 4)
    g.adicionar_aresta("Curitiba", "Florianópolis", 3)
    g.adicionar_aresta("Florianópolis", "Porto Alegre", 5)

    # Conexões Sudeste/Centro-Oeste/Sul
    g.adicionar_aresta("São Paulo", "Campo Grande", 6)
    g.adicionar_aresta("São Paulo", "Goiânia", 5)

    # Extras para garantir múltiplos caminhos
    g.adicionar_aresta("Manaus", "Belém", 10)
    g.adicionar_aresta("Boa Vista", "Macapá", 10)
    g.adicionar_aresta("Cuiabá", "Porto Velho", 6)
    g.adicionar_aresta("Porto Alegre", "Campo Grande", 7)
    g.adicionar_aresta("Palmas", "Cuiabá", 9)
    g.adicionar_aresta("Vitória", "Salvador", 7)
    g.adicionar_aresta("São Luís", "Belém", 6)
    g.adicionar_aresta("Aracaju", "Recife", 5)

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
            print(f"[OK] {entrega}")
            print(f"     Centro: {item['centro']}")
            print(f"     Caminhão: {item['caminhao']}")
            print(f"     Rota: {' → '.join(item['rota'])}")
            print(f"     Tempo estimado: {item['tempo']}h\n")
    
        sleep(2)

if __name__ == "__main__":
    simular()
