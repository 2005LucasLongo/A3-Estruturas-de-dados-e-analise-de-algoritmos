from itertools import permutations
from random import randint

CIDADES = ['Belém', 'Recife', 'Brasília', 'São Paulo', 'Florianópolis']

class Cliente:
    def __init__(self, cidade):
        self.cidade = cidade

# Matriz de distâncias (em km)
DISTANCIAS = [
    # Belém
    [0, 2039, 1889, 2804, 3478],
    # Recife
    [2039,  0, 2120, 2662, 3350],
    # Brasília
    [1889,  2120, 0, 1008, 1682],
    # São Paulo
    [2804,  2662, 1008, 0, 697],
    # Florianópolis
    [3478,  3350, 1682, 697, 0]
]

def gerarListaDeClientes(quantidadeClientes):
    """Gera uma lista aleatória de clientes, cada um com uma cidade."""
    clientes = []
    for _ in range(quantidadeClientes):
        clientes.append(Cliente(CIDADES[randint(0, len(CIDADES)-1)]))
    return clientes

def listarCidadesComClientes(lista_clientes):
    """Retorna uma lista de cidades com clientes (sem repetições)."""
    cidades = []
    for cliente in lista_clientes:
        cidades.append(cliente.cidade)
    # Remove duplicatas mantendo a ordem
    return list(dict.fromkeys(cidades))

def calcular_distancia(rota):
    """Calcula a distância total percorrida numa rota (lista de cidades)."""
    total = 0
    for i in range(len(rota)-1):
        origem = CIDADES.index(rota[i])
        destino = CIDADES.index(rota[i+1])
        total += DISTANCIAS[origem][destino]
    return total

def encontrar_rota_otima(cidade_inicial, cidades_com_clientes):
    """
    Encontra a rota ótima (com menor distância total) que parte da cidade_inicial
    e passa por todas as cidades com clientes.
    """
    # Se a cidade de partida estiver na lista, remova-a
    cidades_disponiveis = [cidade for cidade in cidades_com_clientes if cidade != cidade_inicial]
    
    melhor_rota = None
    melhor_distancia = float('inf')
    
    # Gera todas as permutações possíveis das cidades restantes
    for perm in permutations(cidades_disponiveis):
        rota = [cidade_inicial] + list(perm)
        dist = calcular_distancia(rota)
        if dist < melhor_distancia:
            melhor_distancia = dist
            melhor_rota = rota
            
    return melhor_rota, melhor_distancia

# Exemplo de uso

# Gera um lista de clientes aleatórios e extrai as cidades onde há clientes
LISTA_CLIENTES = gerarListaDeClientes(randint(1,10))
cidades_com_clientes = listarCidadesComClientes(LISTA_CLIENTES)

# Define a cidade de partida aleatoriamente
CIDADE_INICIAL = CIDADES[randint(0, len(CIDADES)-1)]

print(f'Cidades com clientes: {cidades_com_clientes}')
print(f'Cidade de partida: {CIDADE_INICIAL}')

rota_otima, distancia_otima = encontrar_rota_otima(CIDADE_INICIAL, cidades_com_clientes)
print(f'Rota ótima: {rota_otima}')
print(f'Distância total: {distancia_otima} km')