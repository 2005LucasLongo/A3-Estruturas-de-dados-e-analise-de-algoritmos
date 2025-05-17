from model.entrega import Entrega
from random import choice, randint, seed

seed = 42

def gerar_entregas(qtd, destinos):
    return [
        Entrega(f"E{i:03d}", choice(destinos), randint(500, 3000), randint(8, 24))
        for i in range(qtd)
    ]