from model.entrega import Entrega

class Caminhao:
    """
    Representa um caminhão disponível para entregas.

    Cada caminhão possui uma capacidade máxima de carga (em kg), uma quantidade 
    de horas disponíveis para trabalho, e uma lista de entregas alocadas.
    """
    def __init__(self, id_caminhao, capacidade_kg, horas_disponiveis_dia, centro_origem):
        """
        Inicializa o caminhão com identificador, capacidade e tempo disponível.

        Args:
            id_caminhao (str): identificador único do caminhão.
            capacidade_kg (float): capacidade de carga em quilogramas.
            horas_disponiveis (float): número de horas disponíveis para entregas.
        """
        self.id = id_caminhao
        self.capacidade_kg_total = capacidade_kg
        self.capacidade_kg_usada = 0  # Acompanha o peso usado
        self.horas_operacao_maximas_dia = horas_disponiveis_dia # Total que pode operar no dia
        self.tempo_rota_atual = 0 # Tempo da rota atualmente alocada
        self.centro_origem = centro_origem
        self.entregas = []
        self.rota = [] # Lista de cidades da rota atual

    @property
    def capacidade_kg_disponivel(self):
        return self.capacidade_kg_total - self.capacidade_kg_usada

    @property
    def horas_disponiveis_para_rota(self):
        # Quanto tempo ainda pode adicionar à rota atual sem exceder o limite diário
        return self.horas_operacao_maximas_dia - self.tempo_rota_atual

    def adicionar_entrega_a_lista(self, entrega: 'Entrega'):
        """ Apenas adiciona a entrega à lista e atualiza o peso usado. """
        if entrega not in self.entregas: # Evitar duplicatas se chamado incorretamente
            self.entregas.append(entrega)
            self.capacidade_kg_usada += entrega.peso

    def remover_entrega_da_lista(self, entrega: 'Entrega'):
        """ Remove uma entrega e libera capacidade (útil se o roteirizador tentar e falhar). """
        if entrega in self.entregas:
            self.entregas.remove(entrega)
            self.capacidade_kg_usada -= entrega.peso

    def atualizar_rota_e_tempo(self, nova_rota: list, tempo_total_nova_rota: float):
        """ Atualiza a rota planejada e o tempo total de operação para essa rota. """
        self.rota = nova_rota
        self.tempo_rota_atual = tempo_total_nova_rota

    def pode_adicionar_carga(self, peso_adicional: float) -> bool:
        """ Verifica se uma carga adicional cabe na capacidade restante. """
        return (self.capacidade_kg_usada + peso_adicional) <= self.capacidade_kg_total


    def __repr__(self):
        # Calcula dinamicamente a capacidade disponível para o repr
        cap_disponivel = self.capacidade_kg_total - self.capacidade_kg_usada
        # Calcula dinamicamente as horas restantes do dia se a rota atual for executada
        horas_restantes_dia = self.horas_operacao_maximas_dia - self.tempo_rota_atual

        return (f"ID: {self.id} | Capacidade Usada: {self.capacidade_kg_usada:.2f}/{self.capacidade_kg_total:.2f}kg "
                f"(Disponível: {cap_disponivel:.2f}kg) | Tempo Rota: {self.tempo_rota_atual:.2f}h "
                f"(Restante Dia: {horas_restantes_dia:.2f}h / {self.horas_operacao_maximas_dia:.2f}h)")

