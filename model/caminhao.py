class Caminhao:
    """
    Representa um caminhão disponível para entregas.

    Cada caminhão possui uma capacidade máxima de carga (em kg), uma quantidade 
    de horas disponíveis para trabalho, e uma lista de entregas alocadas.
    """
    def __init__(self, id_caminhao, capacidade_kg, horas_disponiveis, centro_origem):
        """
        Inicializa o caminhão com identificador, capacidade e tempo disponível.

        Args:
            id_caminhao (str): identificador único do caminhão.
            capacidade_kg (float): capacidade de carga em quilogramas.
            horas_disponiveis (float): número de horas disponíveis para entregas.
        """
        self.id = id_caminhao
        self.capacidade_kg_disponiveis = capacidade_kg
        self.capacidade_kg_total = capacidade_kg
        self.horas_totais = horas_disponiveis
        self.horas_disponiveis = horas_disponiveis
        self.centro_origem = centro_origem
        self.entregas = []
        self.rota = []

    def pode_entregar(self, peso, tempo_estimado):
        """
        Verifica se o caminhão pode realizar uma entrega com base no peso e tempo.

        Args:
            peso (float): peso da entrega em kg.
            tempo_estimado (float): tempo estimado da entrega em horas.

        Returns:
            bool: True se o caminhão tiver capacidade e tempo suficientes, False caso contrário.
        """
        return peso <= self.capacidade_kg_disponiveis and tempo_estimado <= self.horas_disponiveis

    def alocar_entrega(self, entrega, tempo_estimado):
        """
        Aloca uma entrega ao caminhão, atualizando capacidade e tempo disponíveis.

        Args:
            entrega (Entrega): objeto Entrega a ser adicionado.
            tempo_estimado (float): tempo estimado de duração da entrega em horas.
        """
        self.entregas.append(entrega)
        self.capacidade_kg_disponiveis -= entrega.peso
        self.horas_disponiveis -= tempo_estimado

    def __repr__(self):
        """
        Retorna uma representação legível do caminhão com informações resumidas.

        Returns:
            str: string com ID, capacidade restante e horas disponíveis.
        """
        rota_str = " → ".join(self.rota) if self.rota else "Sem rota definida"
        return (f"ID: {self.id} | Capacidade: {self.capacidade_kg_disponiveis}kg de {self.capacidade_kg_total}kg | "
            f"Horas: {self.horas_disponiveis}h de {self.horas_totais}h")
