import os, sys

raiz = os.path.abspath(os.path.join(__file__, "..", ".."))
if raiz not in sys.path:
    sys.path.append(raiz)

from model.centro_distribuicao import CentroDistribuicao
from model.caminhao import Caminhao

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
            caminhao = Caminhao(placa, capacidade_kg=6000, horas_disponiveis=22)
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

    arestas = [
        ("Belém", "Manaus", 10),
        ("Recife", "Fortaleza", 5),
        ("Recife", "Salvador", 6),
        ("Brasília", "Salvador", 7),
        ("São Paulo", "Curitiba", 4),
        ("Florianópolis", "Curitiba", 3),
        ("Florianópolis", "Porto Alegre", 5),
        ("São Paulo", "Porto Alegre", 7),
        ("Brasília", "Goiânia", 4),
        ("Brasília", "Campo Grande", 9),
        ("São Paulo", "Rio de Janeiro", 6),
        ("São Paulo", "Vitória", 8),
        ("Recife", "Natal", 4),

        # Ligações entre centros
        ("Belém", "Brasília", 12),
        ("Recife", "Brasília", 10),
        ("Brasília", "São Paulo", 8),
        ("São Paulo", "Florianópolis", 6)
    ]

    destinos = [
        "Manaus", "Fortaleza", "Salvador", "Curitiba", "Porto Alegre",
        "Goiânia", "Campo Grande", "Rio de Janeiro", "Vitória", "Natal"
    ]

    return centros, arestas, destinos
