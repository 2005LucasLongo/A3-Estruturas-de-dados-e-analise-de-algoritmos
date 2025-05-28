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
            caminhao = Caminhao(placa, capacidade_kg=randint(1000, 10000), horas_disponiveis_dia=randint(8, 24), centro_origem=centro)
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

    arestas  = [
        # Região Norte
        ("Rio Branco", "Porto Velho", 11.5),
        ("Porto Velho", "Manaus", 48),   
        ("Manaus", "Boa Vista", 17.5),
        ("Manaus", "Macapá", 72),       
        ("Macapá", "Belém", 36),      

        # Região Nordeste
        ("São Luís", "Teresina", 9.5),
        ("Teresina", "Fortaleza", 15),
        ("Fortaleza", "Natal", 11.5),
        ("Natal", "João Pessoa", 4),
        ("João Pessoa", "Recife", 2.5),
        ("Recife", "Maceió", 5),
        ("Maceió", "Aracaju", 5.5),
        ("Aracaju", "Salvador", 7),

        # Conexões Norte/Nordeste/Centro-Oeste
        ("Belém", "Palmas", 28),
        ("Palmas", "Brasília", 19),
        ("São Luís", "Palmas", 24.5),
        ("Salvador", "Brasília", 34),
        ("Fortaleza", "Brasília", 51.5),

        # Região Centro-Oeste
        ("Brasília", "Goiânia", 4),
        ("Goiânia", "Cuiabá", 21),
        ("Cuiabá", "Campo Grande", 16.5),
        ("Campo Grande", "Brasília", 24.5),

        # Região Sudeste
        ("Brasília", "Belo Horizonte", 17.5),
        ("Belo Horizonte", "Rio de Janeiro", 9.5),
        ("Belo Horizonte", "Vitória", 11.5),
        ("Rio de Janeiro", "Vitória", 11.5),
        ("Rio de Janeiro", "São Paulo", 9.5),

        # Região Sul
        ("São Paulo", "Curitiba", 9),
        ("Curitiba", "Florianópolis", 6),
        ("Florianópolis", "Porto Alegre", 10.5),

        # Conexões Sudeste/Centro-Oeste/Sul
        ("São Paulo", "Campo Grande", 23.5),
        ("São Paulo", "Goiânia", 21),

        # Extras para garantir múltiplos caminhos
        ("Manaus", "Belém", 96),         
        ("Boa Vista", "Macapá", 120),    
        ("Cuiabá", "Porto Velho", 34),
        ("Porto Alegre", "Campo Grande", 33),
        ("Palmas", "Cuiabá", 41),
        ("Vitória", "Salvador", 28),
        ("São Luís", "Belém", 19),
        ("Aracaju", "Recife", 11.5)
    ]

    destinos = [
        "Aracaju", "Belém", "Belo Horizonte", "Boa Vista", "Brasília",
        "Campo Grande", "Cuiabá", "Curitiba", "Florianópolis", "Fortaleza",
        "Goiânia", "João Pessoa", "Macapá", "Maceió", "Manaus",
        "Natal", "Palmas", "Porto Alegre", "Porto Velho", "Recife",
        "Rio Branco", "Rio de Janeiro", "Salvador", "São Luís", "São Paulo",
        "Teresina", "Vitória"
    ]


    return centros, arestas, destinos
