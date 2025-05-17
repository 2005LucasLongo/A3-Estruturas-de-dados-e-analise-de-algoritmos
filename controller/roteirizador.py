import os, sys
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))

class Roteirizador:
    """
    Orquestra a roteirização de entregas a partir de múltiplos centros de distribuição.

    A cada entrega, identifica o centro mais próximo, calcula a rota mais curta 
    (via Grafo.caminho_mais_curto) e tenta alocar a carga em um caminhão disponível.
    """
    def __init__(self, centros, entregas, grafo):
        """
        Inicializa o roteirizador.

        Args:
            centros (List[CentroDistribuicao]): lista de centros de distribuição,
                cada um com sua frota de caminhões.
            entregas (List[Entrega]): lista de entregas a serem roteirizadas.
            grafo (Grafo): instância de Grafo ou compatível, para cálculo de rotas.
        """
        self.centros = centros  # Lista de CentroDistribuicao
        self.entregas = entregas  # Lista de Entrega
        self.grafo = grafo  # Instância de Grafo

    def centro_mais_proximo(self, destino):
        """
        Encontra o centro de distribuição mais próximo de um dado destino.

        Para cada centro, executa Grafo.caminho_mais_curto(origem, destino)
        e retorna aquele que tiver menor distância.

        Args:
            destino (str): nome da cidade de destino da entrega.

        Returns:
            Tuple[CentroDistribuicao, float]:
                - O objeto CentroDistribuicao selecionado.
                - A distância (ou custo) mínima até o destino.
        """
        menor_dist = float('inf')
        centro_mais_prox = None

        for centro in self.centros:
            _, dist = self.grafo.caminho_mais_curto(centro.cidade, destino)
            if dist < menor_dist:
                menor_dist = dist
                centro_mais_prox = centro

        return centro_mais_prox, menor_dist

    def alocar_entregas(self):
        """
        Realiza a alocação de cada entrega a um caminhão disponível, preferencialmente em caminhões
        já alocados com rotas ativas, otimizando a nova rota para incluir o destino adicional.
        """
        relatorio = []

        for entrega in self.entregas:
            centro, _ = self.centro_mais_proximo(entrega.destino)
            if centro is None:
                relatorio.append({
                    "entrega": entrega,
                    "erro": f"Nenhum centro de distribuição pode alcançar '{entrega.destino}'"
                })
                continue


            entrega.origem = centro.cidade

            melhor_caminhao = None
            melhor_rota = None
            melhor_tempo = float('inf')

            for centro in self.centros:
                for caminhao in centro.caminhoes:
                    # Cidades de todas as entregas + nova entrega
                    destinos = [e.destino for e in caminhao.entregas] + [entrega.destino]

                    # Evita recalcular rota se já passou da capacidade
                    peso_total = sum(e.peso for e in caminhao.entregas) + entrega.peso

                    if peso_total > caminhao.capacidade_kg_total:
                        continue

                    # Tenta encontrar a melhor ordem para visitar os destinos
                    from itertools import permutations

                    melhor_caminho_candidato = None
                    melhor_tempo_candidato = float('inf')

                    for ordem in permutations(destinos):
                        origem = centro.cidade if not caminhao.entregas else caminhao.entregas[0].origem
                        tempo_total = 0
                        rota_total = [origem]

                        atual = origem
                        for destino in ordem:
                            caminho, tempo = self.grafo.caminho_mais_curto(atual, destino)
                            if not caminho:
                                break
                            tempo_total += tempo
                            rota_total.extend(caminho[1:])  # Evita duplicar cidades
                            atual = destino

                        if tempo_total <= caminhao.horas_disponiveis and tempo_total < melhor_tempo_candidato:
                            melhor_tempo_candidato = tempo_total
                            melhor_caminho_candidato = rota_total

                    if melhor_caminho_candidato and melhor_tempo_candidato < melhor_tempo:
                        melhor_tempo = melhor_tempo_candidato
                        melhor_rota = melhor_caminho_candidato
                        melhor_caminhao = caminhao

            if melhor_caminhao:
                melhor_caminhao.alocar_entrega(entrega, melhor_tempo)
                melhor_caminhao.rota = melhor_rota
                relatorio.append({
                    "entrega": entrega,
                    "caminhao": melhor_caminhao,
                    "centro": melhor_caminhao.centro_origem,
                    "rota": melhor_rota,
                    "tempo": melhor_tempo
                })
            else:
                relatorio.append({
                    "entrega": entrega,
                    "erro": f"Nenhum caminhão viável para a entrega {entrega.id}"
                })


        return relatorio

    def _melhor_rota_com_destinos(self, origem, destinos):
        """
        Gera a melhor rota passando por múltiplos destinos, retornando o caminho e o tempo total.
        Usa permutação simples pois o número de destinos por caminhão é pequeno.

        Args:
            origem (str): cidade de origem
            destinos (List[str]): lista de destinos a serem cobertos

        Returns:
            Tuple[List[str], float]: caminho total e tempo total
        """
        from itertools import permutations

        menor_tempo = float('inf')
        melhor_rota = []

        for ordem in permutations(destinos):
            rota_total = []
            tempo_total = 0
            atual = origem

            for destino in ordem:
                sub_rota, tempo = self.grafo.caminho_mais_curto(atual, destino)
                if rota_total:
                    sub_rota = sub_rota[1:]  # evita duplicação da cidade atual
                rota_total += sub_rota
                tempo_total += tempo
                atual = destino

            if tempo_total < menor_tempo:
                menor_tempo = tempo_total
                melhor_rota = rota_total

        return melhor_rota, menor_tempo
