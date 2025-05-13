from model.entrega import Entrega
import random

def gerar_entregas(qtd, destinos):
    return [
        Entrega(f"E{i:03d}", random.choice(destinos), random.randint(500, 3000), random.randint(8, 24))
        for i in range(qtd)
    ]