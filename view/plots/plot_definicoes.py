# Em view/plots/plot_definicoes.py
import matplotlib.pyplot as plt
import numpy as np

def plot_comparativo_desempenho(resultados_brutos: list[dict], metrica: str, titulo: str, ylabel: str, nome_arquivo_saida: str):
    if not resultados_brutos:
        print("Não há dados para plotar.")
        return

    dados_plot = {}
    estruturas_nomes = sorted(list(set(r["estrutura"] for r in resultados_brutos)))
    quantidades_unicas = sorted(list(set(r["qtd_entregas"] for r in resultados_brutos)))

    for qtd in quantidades_unicas:
        dados_plot[qtd] = {nome: np.nan for nome in estruturas_nomes}

    max_valor_metrica_dados = 0
    for res in resultados_brutos:
        if res[metrica] >= 0:
            valor = res[metrica]
            dados_plot[res["qtd_entregas"]][res["estrutura"]] = valor
            if valor > max_valor_metrica_dados:
                max_valor_metrica_dados = valor
    
    if max_valor_metrica_dados == 0 and not any(not np.isnan(v) for qtd_data in dados_plot.values() for v in qtd_data.values()):
        max_valor_metrica_dados = 1

    num_estruturas = len(estruturas_nomes)
    num_quantidades = len(quantidades_unicas)

    if num_estruturas == 0 or num_quantidades == 0:
        print("Dados insuficientes para gerar o gráfico.")
        return
        
    fig_width = 10 + num_estruturas * 0.8 + num_quantidades * 0.5
    fig_height = 8 + num_quantidades * 0.3 
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    bar_width = 0.8 / num_estruturas
    colors = plt.cm.get_cmap('tab20', num_estruturas)

    for i, nome_estrutura in enumerate(estruturas_nomes):
        valores_metrica = [dados_plot[qtd].get(nome_estrutura, np.nan) for qtd in quantidades_unicas]
        posicoes_x_estrutura = [x + i * bar_width for x in np.arange(num_quantidades)]
        
        bars = ax.bar(posicoes_x_estrutura, valores_metrica, bar_width, label=nome_estrutura, color=colors(i % colors.N))

        for bar_idx, bar in enumerate(bars):
            yval = bar.get_height()
            if not np.isnan(yval) and yval > 0.0001: 
                text_label = f'{yval:.2f}' if metrica == "memoria_pico_kb" else f'{yval:.4f}'
                if yval < 1 and yval > 0 and metrica == "tempo":
                    text_label = f'{yval:.4f}'

                # --- MODIFICAÇÃO AQUI ---
                # Calcular um pequeno offset em unidades de dados para o texto
                # Este offset precisa ser relativo à escala do eixo Y
                text_offset_y = max_valor_metrica_dados * 0.01 # Ex: 1% do valor máximo como offset
                if text_offset_y == 0: # Caso max_valor_metrica_dados seja 0
                    text_offset_y = 0.05 # Um pequeno offset absoluto

                ax.text(
                    x=bar.get_x() + bar.get_width() / 2.0,
                    y=yval + text_offset_y, # Posição y ligeiramente acima do topo da barra
                    s=text_label,
                    ha='center',          
                    va='bottom', # O texto começa a partir deste y e vai para cima         
                    fontsize=7,           
                    rotation=45
                    # Removido: xytext=(0, 2), textcoords="offset points" 
                )

    ax.set_xlabel("Quantidade de Entregas", fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(titulo, fontsize=14, pad=20) 
    ax.set_xticks([r + bar_width * (num_estruturas - 1) / 2 for r in np.arange(num_quantidades)])
    ax.set_xticklabels([str(q) for q in quantidades_unicas], fontsize=10)
    
    if max_valor_metrica_dados < 1:
        headroom_calculation_base = 1 # Use 1 se todos os valores forem muito pequenos
    else:
        headroom_calculation_base = max_valor_metrica_dados

    if headroom_calculation_base < 10:
        headroom_factor = 0.45 # Mais espaço para textos em valores pequenos
    elif headroom_calculation_base < 50 :
        headroom_factor = 0.35 
    else:
        headroom_factor = 0.25
    
    novo_ylim_superior = headroom_calculation_base * (1 + headroom_factor)
    if novo_ylim_superior <= headroom_calculation_base : # Garante que há algum aumento
        novo_ylim_superior = headroom_calculation_base + (0.5 if headroom_calculation_base < 1 else headroom_calculation_base * 0.1)


    print(f"DEBUG: Metrica '{metrica}', Max valor barra: {max_valor_metrica_dados:.2f}, Novo YLim superior: {novo_ylim_superior:.2f}")
    ax.set_ylim(0, novo_ylim_superior)
    print(f"DEBUG: YLim após set_ylim: {ax.get_ylim()}")

    if num_estruturas > 4: 
        ax.legend(title="Estruturas", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9)
    else:
        ax.legend(title="Estruturas", fontsize=9)

    plt.grid(axis='y', linestyle='--', alpha=0.6)
    fig.tight_layout(rect=[0, 0, 0.9 if num_estruturas > 4 else 1, 1]) 
    print(f"DEBUG: YLim ANTES de savefig (após tight_layout se ativo): {ax.get_ylim()}")

    try:
        plt.savefig(nome_arquivo_saida, dpi=150, bbox_inches='tight')
        print(f"Gráfico salvo em: {nome_arquivo_saida}")
    except Exception as e:
        print(f"Erro ao salvar o gráfico {nome_arquivo_saida}: {e}")
    
    print(f"DEBUG: YLim APÓS savefig: {ax.get_ylim()}")
    plt.close(fig)