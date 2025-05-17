import os, sys
from random import randint, seed

raiz = os.path.abspath(os.path.join(__file__, "..", ".."))
if raiz not in sys.path:
    sys.path.append(raiz)

from model.centro_distribuicao import CentroDistribuicao
from model.caminhao import Caminhao

seed(42)

def criar_centros_distribuicao() -> list:
    """
    Cria e retorna os centros de distribuição (sem caminhões).
    """
    cidades = ["Belém", "Recife", "Brasília", "São Paulo", "Florianópolis"]
    return [CentroDistribuicao(cidade) for cidade in cidades]

def adicionar_frota_padrao(centros: list, qtd_caminhoes: int = 10):
    """
    Adiciona uma frota padrão de caminhões a cada centro.

    Args:
        centros (list): lista de CentroDistribuicao.
        qtd_caminhoes (int): número de caminhões por centro.
    """
    for centro in centros:
        for j in range(qtd_caminhoes):
            placa = f"{centro.cidade[:2]}-{j+1}"
            caminhao = Caminhao(placa, capacidade_kg=randint(1000, 10000), horas_disponiveis=randint(8, 20), centro_origem=centro.cidade)
            centro.adicionar_caminhao(caminhao)

def preparar_centros_com_frota(qtd_caminhoes_por_centro=10) -> list:
    """
    Cria centros e adiciona automaticamente uma frota padrão.

    Útil para testes e simulações.
    """
    centros = criar_centros_distribuicao()
    adicionar_frota_padrao(centros, qtd_caminhoes_por_centro)
    return centros

def obter_estrutura_mapa():
    """
    Retorna os dados básicos do mapa logístico:
    - centros: nomes dos centros de distribuição
    - arestas: conexões entre cidades com seus respectivos tempos
    - destinos: cidades que receberão entregas
    """

    centros = criar_centros_distribuicao()

    arestas_base  = [
        # Região Norte
        ("Rio Branco", "Porto Velho", 5),
        ("Porto Velho", "Manaus", 8),
        ("Manaus", "Boa Vista", 6),
        ("Manaus", "Macapá", 10),
        ("Macapá", "Belém", 6),

        # Região Nordeste
        ("São Luís", "Teresina", 4),
        ("Teresina", "Fortaleza", 6),
        ("Fortaleza", "Natal", 4),
        ("Natal", "João Pessoa", 2),
        ("João Pessoa", "Recife", 2),
        ("Recife", "Maceió", 3),
        ("Maceió", "Aracaju", 3),
        ("Aracaju", "Salvador", 4),

        # Conexões Norte/Nordeste/Centro-Oeste
        ("Belém", "Palmas", 10),
        ("Palmas", "Brasília", 6),
        ("São Luís", "Palmas", 8),
        ("Salvador", "Brasília", 7),
        ("Fortaleza", "Brasília", 12),

        # Região Centro-Oeste
        ("Brasília", "Goiânia", 2),
        ("Goiânia", "Cuiabá", 7),
        ("Cuiabá", "Campo Grande", 5),
        ("Campo Grande", "Brasília", 8),

        # Região Sudeste
        ("Brasília", "Belo Horizonte", 5),
        ("Belo Horizonte", "Rio de Janeiro", 5),
        ("Belo Horizonte", "Vitória", 4),
        ("Rio de Janeiro", "Vitória", 6),
        ("Rio de Janeiro", "São Paulo", 4),

        # Região Sul
        ("São Paulo", "Curitiba", 4),
        ("Curitiba", "Florianópolis", 3),
        ("Florianópolis", "Porto Alegre", 5),

        # Conexões Sudeste/Centro-Oeste/Sul
        ("São Paulo", "Campo Grande", 6),
        ("São Paulo", "Goiânia", 5),

        # Extras para garantir múltiplos caminhos
        ("Manaus", "Belém", 10),
        ("Boa Vista", "Macapá", 10),
        ("Cuiabá", "Porto Velho", 6),
        ("Porto Alegre", "Campo Grande", 7),
        ("Palmas", "Cuiabá", 9),
        ("Vitória", "Salvador", 7),
        ("São Luís", "Belém", 6),
        ("Aracaju", "Recife", 5)
    ]

     # Garante bidirecionalidade (duas vias)
    arestas = []
    for origem, destino, peso in arestas_base:
        arestas.append((origem, destino, peso))
        arestas.append((destino, origem, peso))


    destinos = [
        "Aracaju", "Belém", "Belo Horizonte", "Boa Vista", "Brasília",
        "Campo Grande", "Cuiabá", "Curitiba", "Florianópolis", "Fortaleza",
        "Goiânia", "João Pessoa", "Macapá", "Maceió", "Manaus",
        "Natal", "Palmas", "Porto Alegre", "Porto Velho", "Recife",
        "Rio Branco", "Rio de Janeiro", "Salvador", "São Luís", "São Paulo",
        "Teresina", "Vitória"
    ]


    return centros, arestas, destinos
