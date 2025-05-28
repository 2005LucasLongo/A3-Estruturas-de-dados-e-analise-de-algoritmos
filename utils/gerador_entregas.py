from model.entrega import Entrega
from random import choice, randint

def gerar_entregas(qtd, destinos):
    return [
        Entrega(f"E{i:03d}", choice(destinos), randint(500, 3000), randint(8, 200))
        for i in range(qtd)
    ]