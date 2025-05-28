import os
import sys
from itertools import permutations

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from model.entrega import Entrega
# Importe suas outras classes de modelo se precisar de type hinting ou acesso direto
# from model.centro_distribuicao import CentroDistribuicao
# from model.caminhao import Caminhao
# from model.grafoListaAdjacencia import GrafoListaAdjacenceia

class Roteirizador:
    """
    Orquestra a roteirização de entregas a partir de múltiplos centros de distribuição.

    A cada entrega, identifica o centro mais próximo, calcula a rota mais curta
    (via Grafo.caminho_mais_curto) e tenta alocar a carga em um caminhão disponível,
    respeitando as restrições de capacidade, tempo de operação e prazos de entrega.
    """

    def __init__(self, centros, entregas, grafo):
        """
        Inicializa o roteirizador.
        Args:
            centros (List[CentroDistribuicao]): lista de centros de distribuição.
            entregas (List[Entrega]): lista de entregas a serem roteirizadas.
            grafo (Grafo): instância de Grafo para cálculo de rotas.
        """
        self.centros = centros
        self.entregas = entregas
        self.grafo = grafo

    def centro_mais_proximo(self, destino_entrega: str):
        # ... (código existente do centro_mais_proximo - sem alterações aqui) ...
        menor_dist = float('inf')
        centro_selecionado = None

        if not self.centros:
            return None, menor_dist

        for cd_origem in self.centros:
            _, dist_calculada = self.grafo.caminho_mais_curto(cd_origem.cidade, destino_entrega)
            if dist_calculada < menor_dist:
                menor_dist = dist_calculada
                centro_selecionado = cd_origem
        
        if centro_selecionado is None:
            return None, float('inf')
        return centro_selecionado, menor_dist

    def _calcular_melhor_rota_para_destinos(self, origem_rota: str, destinos_visitar: list, entrega_atual_para_prazo: 'Entrega' = None):
        # ... (código existente do _calcular_melhor_rota_para_destinos - sem alterações aqui) ...
        if not destinos_visitar:
            return [origem_rota], 0, True

        melhor_rota_final = None
        menor_tempo_final = float('inf')
        prazo_atendido_pela_melhor_rota = False # Renomeado para clareza

        for ordem_visita in permutations(destinos_visitar):
            rota_candidata_atual = [origem_rota]
            tempo_total_candidato = 0
            cidade_atual_na_rota = origem_rota
            rota_valida_nesta_permutacao = True
            prazo_entrega_atual_ok_nesta_permutacao = True

            for proximo_destino_na_ordem in ordem_visita:
                segmento_rota, tempo_segmento = self.grafo.caminho_mais_curto(cidade_atual_na_rota, proximo_destino_na_ordem)

                if not segmento_rota or tempo_segmento == float('inf'): # Adicionado verificação de tempo_segmento
                    rota_valida_nesta_permutacao = False
                    break

                rota_candidata_atual.extend(segmento_rota[1:])
                tempo_total_candidato += tempo_segmento
                cidade_atual_na_rota = proximo_destino_na_ordem

                if entrega_atual_para_prazo and proximo_destino_na_ordem == entrega_atual_para_prazo.destino:
                    if tempo_total_candidato > entrega_atual_para_prazo.prazo:
                        prazo_entrega_atual_ok_nesta_permutacao = False
            
            if rota_valida_nesta_permutacao:
                if tempo_total_candidato < menor_tempo_final:
                    # Se é mais curta E atende ao prazo da entrega atual
                    if prazo_entrega_atual_ok_nesta_permutacao:
                        menor_tempo_final = tempo_total_candidato
                        melhor_rota_final = rota_candidata_atual
                        prazo_atendido_pela_melhor_rota = True
                    # Se é mais curta, mas NÃO atende ao prazo, e ainda não temos uma que atenda
                    elif not prazo_atendido_pela_melhor_rota:
                        # Ainda atualizamos para ter a rota mais curta possível, mesmo que fora do prazo
                        # A decisão de usar essa rota será do chamador
                        menor_tempo_final = tempo_total_candidato
                        melhor_rota_final = rota_candidata_atual
                        # prazo_atendido_pela_melhor_rota continua False
                # Caso especial: tempo igual, mas esta atende ao prazo e a anterior não
                elif tempo_total_candidato == menor_tempo_final and prazo_entrega_atual_ok_nesta_permutacao and not prazo_atendido_pela_melhor_rota:
                    melhor_rota_final = rota_candidata_atual
                    prazo_atendido_pela_melhor_rota = True


        if melhor_rota_final is None:
             return None, float('inf'), False
        
        return melhor_rota_final, menor_tempo_final, prazo_atendido_pela_melhor_rota


    def alocar_entregas(self):
        relatorio_final = []

        for entrega_obj in self.entregas:
            cd_origem_da_entrega, _ = self.centro_mais_proximo(entrega_obj.destino)

            if cd_origem_da_entrega is None:
                relatorio_final.append({
                    "entrega": entrega_obj,
                    # MODIFICAÇÃO: Erro agora é uma lista de strings
                    "erro": [f"Destino '{entrega_obj.destino}' inalcançável por qualquer Centro de Distribuição."]
                })
                continue
            
            entrega_obj.origem = cd_origem_da_entrega.cidade

            melhor_opcao_para_entrega = {
                "caminhao": None, "centro_alocado": None, "rota": None,
                "tempo_total_rota": float('inf'), "alocada": False
            }
            
            falhas_agregadas = {
                "capacidade_peso": 0,
                "rota_invalida_ou_inalcancavel": 0,
                "prazo_entrega_excedido": 0,
                "horas_caminhao_excedidas": 0,
                "prazo_outras_entregas_violado": 0,
                "total_caminhoes_verificados_para_entrega": 0,
                "caminhoes_sem_cd_origem_definido": 0
            }
            caminhoes_considerados_validos_inicialmente = 0

            for cd_caminhao_iter in self.centros:
                for caminhao_candidato in cd_caminhao_iter.caminhoes:
                    falhas_agregadas["total_caminhoes_verificados_para_entrega"] += 1
                    
                    if not hasattr(caminhao_candidato, 'centro_origem') or not hasattr(caminhao_candidato.centro_origem, 'cidade'):
                        falhas_agregadas["caminhoes_sem_cd_origem_definido"] +=1
                        continue 
                    
                    origem_da_rota_do_caminhao_str = caminhao_candidato.centro_origem.cidade
                    
                    peso_total_com_nova_entrega = sum(e.peso for e in caminhao_candidato.entregas) + entrega_obj.peso
                    if peso_total_com_nova_entrega > caminhao_candidato.capacidade_kg_total:
                        falhas_agregadas["capacidade_peso"] += 1
                        continue 

                    caminhoes_considerados_validos_inicialmente += 1
                    destinos_para_o_caminhao = [e.destino for e in caminhao_candidato.entregas] + [entrega_obj.destino]
                    
                    nova_rota_calculada, tempo_total_calculado, prazo_entrega_atual_atendido = \
                        self._calcular_melhor_rota_para_destinos(
                            origem_da_rota_do_caminhao_str,
                            destinos_para_o_caminhao,
                            entrega_obj
                        )

                    if not nova_rota_calculada:
                        falhas_agregadas["rota_invalida_ou_inalcancavel"] += 1
                        continue 

                    if not prazo_entrega_atual_atendido:
                        falhas_agregadas["prazo_entrega_excedido"] += 1
                    if tempo_total_calculado > caminhao_candidato.horas_operacao_maximas_dia:
                        falhas_agregadas["horas_caminhao_excedidas"] += 1
                    
                    entregas_ja_no_caminhao = caminhao_candidato.entregas 
                    todas_entregas_para_verificacao_prazo = list(entregas_ja_no_caminhao) + [entrega_obj]
                    prazos_todos_ok = self.verificar_prazos_para_rota(
                        nova_rota_calculada, 
                        tempo_total_calculado,
                        todas_entregas_para_verificacao_prazo, 
                        origem_da_rota_do_caminhao_str
                    )
                    if not prazos_todos_ok:
                        falhas_agregadas["prazo_outras_entregas_violado"] += 1

                    if prazo_entrega_atual_atendido and \
                       tempo_total_calculado <= caminhao_candidato.horas_operacao_maximas_dia and \
                       prazos_todos_ok:
                        if tempo_total_calculado < melhor_opcao_para_entrega["tempo_total_rota"]:
                            melhor_opcao_para_entrega.update({
                                "caminhao": caminhao_candidato,
                                "centro_alocado": caminhao_candidato.centro_origem,
                                "rota": nova_rota_calculada,
                                "tempo_total_rota": tempo_total_calculado,
                                "alocada": True
                            })
            
            if melhor_opcao_para_entrega["alocada"]:
                caminhao_escolhido = melhor_opcao_para_entrega["caminhao"]
                caminhao_escolhido.adicionar_entrega_a_lista(entrega_obj)
                caminhao_escolhido.atualizar_rota_e_tempo(
                    melhor_opcao_para_entrega["rota"],
                    melhor_opcao_para_entrega["tempo_total_rota"]
                )
                relatorio_final.append({
                    "entrega": entrega_obj,
                    "caminhao": caminhao_escolhido,
                    "centro": melhor_opcao_para_entrega["centro_alocado"],
                    "rota": melhor_opcao_para_entrega["rota"],
                    "tempo": melhor_opcao_para_entrega["tempo_total_rota"]
                })
            else:
                # MODIFICAÇÃO: Construir lista de strings para os erros
                lista_erros_detalhados = []
                if falhas_agregadas["caminhoes_sem_cd_origem_definido"] == falhas_agregadas["total_caminhoes_verificados_para_entrega"] and falhas_agregadas["total_caminhoes_verificados_para_entrega"] > 0 :
                     lista_erros_detalhados.append(f"AVISO INTERNO: Todos os {falhas_agregadas['total_caminhoes_verificados_para_entrega']} caminhões verificados foram ignorados por não terem Centro de Distribuição de origem definido corretamente.")
                elif falhas_agregadas["caminhoes_sem_cd_origem_definido"] > 0:
                    lista_erros_detalhados.append(f"AVISO INTERNO: {falhas_agregadas['caminhoes_sem_cd_origem_definido']} caminhões ignorados por não terem Centro de Distribuição de origem definido corretamente.")

                if falhas_agregadas["capacidade_peso"] == caminhoes_considerados_validos_inicialmente and caminhoes_considerados_validos_inicialmente > 0:
                    lista_erros_detalhados.append(f"Todos os {caminhoes_considerados_validos_inicialmente} caminhões (com Centro de Distribuição definido e capacidade inicial verificável) não possuem capacidade de peso suficiente.")
                elif falhas_agregadas["capacidade_peso"] > 0:
                     lista_erros_detalhados.append(f"{falhas_agregadas['capacidade_peso']}/{caminhoes_considerados_validos_inicialmente} caminhões (com Centro de Distribuição definido) sem capacidade de peso.")
                
                if falhas_agregadas["rota_invalida_ou_inalcancavel"] == (caminhoes_considerados_validos_inicialmente - falhas_agregadas["capacidade_peso"]) and (caminhoes_considerados_validos_inicialmente - falhas_agregadas["capacidade_peso"]) > 0 :
                     lista_erros_detalhados.append("Todos os caminhões com capacidade tiveram rotas inválidas/inalcançáveis.")
                elif falhas_agregadas["rota_invalida_ou_inalcancavel"] > 0:
                    lista_erros_detalhados.append(f"{falhas_agregadas['rota_invalida_ou_inalcancavel']} tentativas de rota falharam (rota inválida/inalcançável).")
                
                if falhas_agregadas["prazo_entrega_excedido"] > 0:
                    lista_erros_detalhados.append(f"{falhas_agregadas['prazo_entrega_excedido']} tentativas excederiam o prazo da entrega ({entrega_obj.prazo}h).")
                if falhas_agregadas["horas_caminhao_excedidas"] > 0:
                    lista_erros_detalhados.append(f"{falhas_agregadas['horas_caminhao_excedidas']} tentativas excederiam as horas de operação do caminhão.")
                if falhas_agregadas["prazo_outras_entregas_violado"] > 0:
                    lista_erros_detalhados.append(f"{falhas_agregadas['prazo_outras_entregas_violado']} tentativas violariam prazos de entregas pré-existentes no caminhão.")
                
                if not lista_erros_detalhados:
                    if falhas_agregadas["total_caminhoes_verificados_para_entrega"] > 0:
                        lista_erros_detalhados.append(f"Nenhum caminhão atendeu a todos os critérios (verificados: {falhas_agregadas['total_caminhoes_verificados_para_entrega']}).")
                    else:
                        lista_erros_detalhados.append("Nenhum caminhão disponível nos Centros de Distribuiçãos para verificação.")
                
                relatorio_final.append({"entrega": entrega_obj, "erro": lista_erros_detalhados}) # "erro" agora contém a lista
        
        return relatorio_final

    def verificar_prazos_para_rota(self, rota_calculada: list, tempo_total_rota_nao_usado: float, entregas_na_rota: list, origem_rota_str: str):
        # ... (código existente do verificar_prazos_para_rota - renomeei um arg não usado para clareza) ...
        if not rota_calculada or not entregas_na_rota :
            return True 

        map_destino_para_entrega = {entrega.destino: entrega for entrega in entregas_na_rota}
        tempo_acumulado_na_rota = 0
        cidade_atual = origem_rota_str

        for i in range(len(rota_calculada) - 1):
            proxima_cidade_na_rota = rota_calculada[i+1]
            _, tempo_segmento = self.grafo.caminho_mais_curto(cidade_atual, proxima_cidade_na_rota)

            if tempo_segmento == float('inf'):
                return False 

            tempo_acumulado_na_rota += tempo_segmento
            cidade_atual = proxima_cidade_na_rota
            
            if cidade_atual in map_destino_para_entrega:
                entrega_correspondente = map_destino_para_entrega[cidade_atual]
                if tempo_acumulado_na_rota > entrega_correspondente.prazo:
                    return False 
        return True