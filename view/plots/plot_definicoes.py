import matplotlib.pyplot as plt

def plot_sucesso_falhas(quantidades, sucessos, falhas):
    """
    Gera um gráfico de barras comparando o número de entregas bem-sucedidas vs. falhas
    para diferentes quantidades de entregas.

    Args:
    quantidades (list[int]): quantidade total de entregas por cenário.
    sucessos (list[int]): número de entregas bem-sucedidas.
    falhas (list[int]): número de entregas com erro.
    """
    bar_width = 0.35
    x = range(len(quantidades))

    plt.figure(figsize=(10, 6))
    plt.bar(x, sucessos, width=bar_width, label='Sucesso', color='green')
    plt.bar([i + bar_width for i in x], falhas, width=bar_width, label='Falhas', color='red')

    plt.xlabel("Quantidade de Entregas")
    plt.ylabel("Número de Entregas")
    plt.title("Comparação de Entregas Sucesso vs. Falhas")
    plt.xticks([i + bar_width / 2 for i in x], quantidades)
    plt.legend()
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()