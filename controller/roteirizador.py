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
        Realiza a alocação de cada entrega a um caminhão disponível.

        Para cada entrega:
          1. Identifica o centro mais próximo e obtém rota e tempo estimado.
          2. Percorre a frota do centro checando `caminhao.pode_entregar`.
          3. Se possível, chama `caminhao.alocar_entrega` e registra a alocação.
          4. Caso contrário, registra erro de falta de veículo viável.

        Returns:
            List[Dict]: lista de dicionários, cada um contendo:
                - 'entrega': objeto Entrega
                - 'caminhao': objeto Caminhao (se alocado)
                - 'centro': nome da cidade do centro
                - 'rota': list[str] da sequência de cidades
                - 'tempo': float do tempo estimado
                - 'erro': str, presente apenas se falhou a alocação
        """
        relatorio = []

        for entrega in self.entregas:
            centro, dist = self.centro_mais_proximo(entrega.destino)
            caminho, tempo_estimado = self.grafo.caminho_mais_curto(centro.cidade, entrega.destino)

            # Procurar um caminhão viável no centro
            caminhao_alocado = None
            for caminhao in centro.caminhoes:
                if caminhao.pode_entregar(entrega.peso, tempo_estimado):
                    caminhao_alocado = caminhao
                    break

            if caminhao_alocado:
                caminhao_alocado.alocar_entrega(entrega, tempo_estimado)
                relatorio.append({
                    "entrega": entrega,
                    "caminhao": caminhao_alocado,
                    "centro": centro.cidade,
                    "rota": caminho,
                    "tempo": tempo_estimado
                })
            else:
                relatorio.append({
                    "entrega": entrega,
                    "erro": f"Nenhum caminhão disponível em {centro.cidade} para a entrega"
                })

        return relatorio
