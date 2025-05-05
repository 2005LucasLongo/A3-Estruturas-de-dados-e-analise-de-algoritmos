class CentroDistribuicao:
    """
    Representa um centro de distribuição localizado em uma cidade.

    Cada centro gerencia uma frota de caminhões disponíveis para entregas.
    """
    def __init__(self, cidade):
        """
        Inicializa um centro de distribuição com sua respectiva cidade.

        Args:
            cidade (str): nome da cidade onde o centro está localizado.
        """
        self.cidade = cidade
        self.caminhoes = []

    def adicionar_caminhao(self, caminhao):
        """
        Adiciona um caminhão à frota do centro de distribuição.

        Args:
            caminhao (Caminhao): objeto Caminhao a ser adicionado.
        """
        self.caminhoes.append(caminhao)

    def __repr__(self):
        """
        Retorna uma representação em string do centro e quantidade de caminhões.

        Returns:
            str: nome da cidade e número de caminhões cadastrados.
        """
        return f"Centro: {self.cidade} | Caminhões: {len(self.caminhoes)}"
