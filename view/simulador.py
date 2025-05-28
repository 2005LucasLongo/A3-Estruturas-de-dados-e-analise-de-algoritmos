import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))) # Corrigido para os.path.dirname(__file__)

from model.entrega import Entrega
from model.caminhao import Caminhao # Presumo que esteja usando a versão refatorada de Caminhao
from model.centro_distribuicao import CentroDistribuicao
from model.grafoListaAdjacencia import GrafoListaAdjacencia # Certifique-se que o nome está correto
from controller.roteirizador import Roteirizador
from utils.mapa_logistico import obter_estrutura_mapa, adicionar_frota_padrao
from utils.gerador_entregas import gerar_entregas
from time import sleep

def simular():
    """
    Função que simula o processo de roteirização de entregas a partir de centros de distribuição, caminhões e
    distâncias entre as cidades. Realiza a alocação de entregas aos centros e caminhões disponíveis e exibe os
    resultados da simulação.
    """

    # 1. Criar Centros de Distribuição e caminhões
    # (Você pode querer que obter_estrutura_mapa retorne os objetos CentroDistribuicao já)
    # Assumindo que obter_estrutura_mapa() retorna:
    # - uma lista de objetos CentroDistribuicao (ou dados para criá-los)
    # - uma lista de tuplas de arestas (origem_str, destino_str, tempo)
    # - uma lista de strings de destinos possíveis para entregas
    lista_obj_centros, arestas, lista_nomes_destinos = obter_estrutura_mapa()

    # Adiciona 2 caminhões por centro (esta função deve receber lista_obj_centros)
    adicionar_frota_padrao(lista_obj_centros, 2)

    # 2. Criar entregas
    entregas_geradas = gerar_entregas(10, lista_nomes_destinos)
    print(f"Total de {len(entregas_geradas)} entregas geradas para simulação.")

    # 3. Criar o grafo completo com todas as cidades e conexões reais
    grafo = GrafoListaAdjacencia() # Certifique-se que o nome da classe está correto

    # Adiciona as arestas com base no mapa logístico
    for origem_aresta, destino_aresta, tempo_aresta in arestas: # Renomeado para clareza
        grafo.adicionar_aresta(origem_aresta, destino_aresta, tempo_aresta)

    # 4. Executar o roteirizador
    roteirizador = Roteirizador(lista_obj_centros, entregas_geradas, grafo)
    resultado_alocacao = roteirizador.alocar_entregas() # Chamada única

    # 5. Exibir resultados
    exibir_resultados_detalhados(resultado_alocacao, lista_obj_centros, grafo, entregas_geradas)


def exibir_resultados_detalhados(resultado_alocacao, todos_os_centros, grafo, todas_as_entregas_geradas):
    print("\n--- RELATÓRIO DETALHADO DA SIMULAÇÃO DE ENTREGAS ---")

    caminhoes_ativos = {}
    entregas_alocadas_ids = set()
    entregas_nao_alocadas_info = []

    for item_resultado in resultado_alocacao:
        entrega_processada = item_resultado["entrega"]
        # MODIFICAÇÃO: Verifica se a chave "erro" existe. Se não, é sucesso.
        if "erro" not in item_resultado: # Sucesso na alocação
            entregas_alocadas_ids.add(entrega_processada.id)
            caminhao = item_resultado["caminhao"]
            centro_do_caminhao = item_resultado["centro"] 
            rota_planejada = item_resultado["rota"]
            tempo_total_planejado = item_resultado["tempo"]

            if caminhao.id not in caminhoes_ativos:
                caminhoes_ativos[caminhao.id] = {
                    "caminhao_obj": caminhao,
                    "entregas_nesta_rota": [],
                    "rota_parcial_entregas": rota_planejada,
                    "tempo_parcial_entregas": tempo_total_planejado,
                    "cd_origem_obj": centro_do_caminhao
                }
            caminhoes_ativos[caminhao.id]["entregas_nesta_rota"].append(entrega_processada)
        else: # Falha na alocação
            entregas_nao_alocadas_info.append({
                "entrega": entrega_processada,
                "lista_de_motivos": item_resultado["erro"] # "erro" agora contém a lista de motivos
            })
    
    # ... (o restante da lógica para exibir caminhões ativos permanece o mesmo) ...
    print("\nVISUALIZAÇÃO DA OPERAÇÃO POR CAMINHÃO:\n")
    if not caminhoes_ativos:
        print("Nenhum caminhão realizou entregas.")
    else:
        for i, (caminhao_id, dados_caminhao) in enumerate(caminhoes_ativos.items()):
            if i > 0: 
                # Removido o input para não travar a execução completa para o exemplo
                # input(f"\nPressione Enter para ver a análise do próximo caminhão...\n")
                print("-" * 50 + "\n") # Apenas uma separação visual

            caminhao = dados_caminhao["caminhao_obj"]
            cd_origem_obj = dados_caminhao["cd_origem_obj"] 
            rota_ate_ultima_entrega = dados_caminhao["rota_parcial_entregas"]
            tempo_ate_ultima_entrega = dados_caminhao["tempo_parcial_entregas"]
            entregas_nesta_rota = dados_caminhao["entregas_nesta_rota"]

            print(f"--- Caminhão: {caminhao.id} (CD: {cd_origem_obj.cidade}) ---")
            print(f"  Capacidade Total: {caminhao.capacidade_kg_total}kg, Horas Máximas/Dia: {caminhao.horas_operacao_maximas_dia}h")
            
            if not rota_ate_ultima_entrega :
                print("  Sem rota definida (possivelmente entrega no próprio CD ou erro na rota).")
                if tempo_ate_ultima_entrega == 0 and len(entregas_nesta_rota) == 1 and entregas_nesta_rota[0].destino == cd_origem_obj.cidade:
                    print(f"  Entrega realizada no próprio CD: {entregas_nesta_rota[0]}")
                print(f"  Caminhão permanece no CD: {cd_origem_obj.cidade}\n")
                continue

            print(f"  Rota Planejada (Entregas): {' → '.join(rota_ate_ultima_entrega)}")
            print(f"  Tempo Estimado (Entregas): {tempo_ate_ultima_entrega}h")
            peso_inicial_carregado = sum(e.peso for e in entregas_nesta_rota)
            print(f"  Peso Inicial Carregado: {peso_inicial_carregado:.2f}kg")
            print("\n  Detalhes da Rota e Entregas:")
            cidade_anterior_rota = rota_ate_ultima_entrega[0]
            tempo_acumulado_simulado = 0
            peso_simulado_no_caminhao = peso_inicial_carregado

            if len(rota_ate_ultima_entrega) == 1 and rota_ate_ultima_entrega[0] == cd_origem_obj.cidade:
                print(f"    PARTIDA: {cd_origem_obj.cidade} (próprio CD)")
                for entrega_obj_sim in entregas_nesta_rota:
                    if entrega_obj_sim.destino == cd_origem_obj.cidade:
                        print(f"    => CHEGADA: {cd_origem_obj.cidade} (Próprio CD, Tempo: 0h)")
                        print(f"       ENTREGA REALIZADA: {entrega_obj_sim}")
                        peso_simulado_no_caminhao -= entrega_obj_sim.peso
                        print(f"       Peso restante no caminhão: {peso_simulado_no_caminhao:.2f}kg")
                print(f"    RETORNO: Caminhão já está no CD de origem ({cd_origem_obj.cidade}).")
                print(f"  Tempo Total da Viagem (com retorno implícito): {tempo_ate_ultima_entrega}h")
                horas_restantes_dia = caminhao.horas_operacao_maximas_dia - caminhao.tempo_rota_atual
                print(f"  Horas restantes do caminhão no dia: {horas_restantes_dia:.2f}h\n")
                input("Aperte enter para continuar para a próxima entrega.")
                continue
                

            for idx_cidade, cidade_atual_rota in enumerate(rota_ate_ultima_entrega):
                if idx_cidade == 0:
                    print(f"    PARTIDA: {cidade_atual_rota}")
                else:
                    _, tempo_trecho_simulado = grafo.caminho_mais_curto(cidade_anterior_rota, cidade_atual_rota)
                    if tempo_trecho_simulado == float('inf'):
                        print(f"    ERRO: Não foi possível calcular trecho de {cidade_anterior_rota} para {cidade_atual_rota}")
                        break 
                    tempo_acumulado_simulado += tempo_trecho_simulado
                    print(f"    TRECHO: {cidade_anterior_rota} → {cidade_atual_rota} (Tempo: {tempo_trecho_simulado}h)")
                    print(f"    => CHEGADA: {cidade_atual_rota} (Tempo acumulado na rota: {tempo_acumulado_simulado}h)")
                entregas_nesta_cidade_sim = [e for e in entregas_nesta_rota if e.destino == cidade_atual_rota]
                for entrega_obj_sim in entregas_nesta_cidade_sim:
                    print(f"       ENTREGA REALIZADA: {entrega_obj_sim}")
                    peso_simulado_no_caminhao -= entrega_obj_sim.peso
                    print(f"       Peso restante no caminhão: {peso_simulado_no_caminhao:.2f}kg")
                cidade_anterior_rota = cidade_atual_rota
            
            ultima_parada_rota = rota_ate_ultima_entrega[-1]
            tempo_total_com_retorno_simulado = tempo_ate_ultima_entrega
            rota_completa_com_retorno_simulada = list(rota_ate_ultima_entrega)

            if ultima_parada_rota != cd_origem_obj.cidade:
                caminho_retorno_sim, tempo_retorno_sim = grafo.caminho_mais_curto(ultima_parada_rota, cd_origem_obj.cidade)
                if caminho_retorno_sim:
                    print(f"\n    TRECHO RETORNO: {ultima_parada_rota} → {cd_origem_obj.cidade} (Tempo: {tempo_retorno_sim}h)")
                    rota_completa_com_retorno_simulada.extend(caminho_retorno_sim[1:])
                    tempo_total_com_retorno_simulado += tempo_retorno_sim
                    print(f"    => CHEGADA AO CD DE ORIGEM: {cd_origem_obj.cidade}")
                else:
                    print(f"\n    AVISO: Não foi possível calcular rota de retorno de {ultima_parada_rota} para {cd_origem_obj.cidade}.")
            else:
                print(f"\n    RETORNO: Caminhão já está no CD de origem ({cd_origem_obj.cidade}) ou a última entrega foi no CD.")

            print(f"\n  Rota Completa Simulada (com retorno): {' → '.join(rota_completa_com_retorno_simulada)}")
            print(f"  Tempo Total da Viagem Simulado (com retorno): {tempo_total_com_retorno_simulado:.2f}h")
            if tempo_total_com_retorno_simulado > caminhao.horas_operacao_maximas_dia:
                print(f"  ATENÇÃO: Tempo total simulado com retorno ({tempo_total_com_retorno_simulado:.2f}h) excede as horas máximas do caminhão ({caminhao.horas_operacao_maximas_dia:.2f}h)!")
            horas_restantes_dia_apos_entregas = caminhao.horas_operacao_maximas_dia - caminhao.tempo_rota_atual 
            print(f"  Horas restantes do caminhão no dia (após rota de entregas): {horas_restantes_dia_apos_entregas:.2f}h")
            # Removi a separação com input para não travar a execução
            if i < len(caminhoes_ativos) -1 : # Adiciona separador visual entre caminhões
                 print("-" * 50 + "\n")
            else: # Após o último caminhão
                 print("-" * 50 + "\n")
            input("Aperte enter para continuar para a próxima entrega.")


    # 3. Exibir Entregas Não Alocadas
    print("\n--- ENTREGAS NÃO ALOCADAS ---\n")
    if not entregas_nao_alocadas_info:
        print("Todas as entregas foram alocadas com sucesso.")
    else:
        print(f"Total de {len(entregas_nao_alocadas_info)} entregas não puderam ser alocadas:")
        for info_nao_alocada in entregas_nao_alocadas_info:
            entrega_na = info_nao_alocada["entrega"]
            lista_de_motivos_erro = info_nao_alocada["lista_de_motivos"] # Agora é uma lista

            print(f"  - Entrega: {entrega_na}") # Usa o __repr__ da Entrega
            print(f"    Motivos:")
            if isinstance(lista_de_motivos_erro, list) and lista_de_motivos_erro:
                for motivo_individual in lista_de_motivos_erro:
                    print(f"      - {motivo_individual.strip()}") # .strip() para remover espaços extras se houver
            elif isinstance(lista_de_motivos_erro, str): # Fallback se ainda for uma string
                 print(f"      - {lista_de_motivos_erro.strip()}")
            else:
                print(f"      - Informação de erro não disponível ou em formato inesperado.")
            print("-" * 50) # Separador para a próxima entrega não alocada
        print() # Linha extra no final da seção

if __name__ == "__main__":
    simular()