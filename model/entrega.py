class Entrega:
    """
    Representa uma entrega a ser realizada para uma cidade específica.

    Contém informações sobre destino, peso e prazo máximo de entrega.
    """
    def __init__(self, id_entrega, destino, peso, prazo, origem=None):
        """
        Inicializa uma nova entrega com seus atributos básicos.

        Args:
            id_entrega (str): Identificador único da entrega.
            destino (str): Nome da cidade destino da entrega.
            peso (float): Peso da carga da entrega em kg.
            prazo (float): Prazo máximo para a entrega em horas.
        """
        self.id = id_entrega
        self.destino = destino
        self.peso = peso
        self.prazo = prazo
        self.origem = origem

    def __repr__(self):
        """
        Retorna uma representação em string da entrega.

        Returns:
            str: Informações resumidas da entrega.
        """
        return f"Entrega {self.id} -> {self.destino} | Peso: {self.peso}kg | Prazo Máximo: {self.prazo}h"
