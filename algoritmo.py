from random import randint

CIDADES = ['Belém', 'Recife', 'Brasília', 'São Paulo', 'Florianópolis']

class cliente:
    def __init__ (self, cidade):
        self.cidade = cidade

DISTANCIAS = [ # em km
    # Belém
    [
        0, # Belém-Belém
        2039, # Belém-Recife
        1889, # Belém-Brasília
        2804, # Belém-SP
        3478 # Belém-Florianópolis
    ],
    
    # Recife
    [
        2039, # Recife-Belém
        0, # Recife-Recife
        2120, # Recife-Brasília
        2662, # Recife-SP
        3350 # Recife-Florianópolis
    ],
    
    # Brasília
    [
        1889, # Brasília-Belém
        2120, # Brasília-Recife
        0, # Brasília-Brasília
        1008, # Brasília-SP
        1682 # Brasília-Florianópolis
    ],
    
    # SP
    [
        2804, # SP-Belém
        2662, # SP-Recife
        1008, # SP-Brasília
        0, # SP-SP
        697 # SP-Florianópolis
    ],
    
    # Florianópolis
    [
        3478, # Florianópolis-Belém
        3350, # Florianópolis-Recife
        1682, # Florianópolis-Brasília
        697, # Florianópolis-SP
        0 # Florianópolis-Florianópolis
    ]
]

def gerarListaDeClientes(quantidadeClientes):
    clientes = []
    for i in range(quantidadeClientes):
        clientes.append(cliente(CIDADES[randint(0, 4)]))
    return clientes

def listarCidadesComClientes(lista_clientes):
    cidades = []
    for cliente in lista_clientes:
        cidades.append(cliente.cidade)
    cidades = list(dict.fromkeys(cidades))
    return cidades

def obterCidadeComClientesMaisProximaDaAtual (cidade_atual, cidades_com_clientes):
    try:
        cidades_com_clientes.remove(cidade_atual)
    except:
        pass
    index_cidade_mais_proxima = CIDADES.index(cidades_com_clientes[0])
    index_cidade_atual = CIDADES.index(cidade_atual)
    
    # obtem os indexes das cidades com clientes
    cidades_com_clientes_indexes = []
    for cidade in cidades_com_clientes:
        cidades_com_clientes_indexes.append(CIDADES.index(cidade))
    
    # calcula qual a cidade mais próxima
    for index_cidade in cidades_com_clientes_indexes:
        if DISTANCIAS[index_cidade_atual][index_cidade] < DISTANCIAS[index_cidade_atual][index_cidade_mais_proxima]:
            index_cidade_mais_proxima = index_cidade
    
    return CIDADES[index_cidade_mais_proxima]
    

# sample

LISTA_CLIENTES = gerarListaDeClientes(10)
cidades_com_clientes = listarCidadesComClientes(LISTA_CLIENTES)
QUANTIA_CIDADES = len(cidades_com_clientes)
CIDADE_INICIAL = CIDADES[randint(0, 4)]
cidade_atual = CIDADE_INICIAL

print(f'Cidades: {cidades_com_clientes}')
print(f'Partida: {CIDADE_INICIAL}')

for c in range(0, QUANTIA_CIDADES):
    try:
        try:
            cidades_com_clientes.remove(cidade_atual)
        except:
            pass
        cidade_atual = obterCidadeComClientesMaisProximaDaAtual(cidade_atual, cidades_com_clientes)

        print(f'Cidades: {cidades_com_clientes}')
        print(f'Atualmente: {cidade_atual}')
    except:
        print('Fim da rota.')
