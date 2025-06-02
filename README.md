#  Projeto de Otimização de Roteirização de Entregas com Análise de Estruturas de Dados 🚚💨

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/status-concluído ✅-brightgreen" alt="Status: Concluído">
  </p>

## 📝 Descrição

Este projeto apresenta o desenvolvimento de um sistema em Python focado na otimização do processo de roteirização de entregas para uma empresa de logística com múltiplos Centros de Distribuição. A solução visa não apenas encontrar rotas eficientes, mas também conduzir uma análise comparativa rigorosa do desempenho de diversas estruturas de dados e algoritmos aplicados a este contexto. O sistema considera restrições operacionais realistas, como capacidade de carga dos veículos, limites diários de horas de operação e prazos máximos para cada entrega.

## 🎯 Objetivos do Projeto

Os principais objetivos deste trabalho incluem:
-   Desenvolver um algoritmo de roteirização capaz de alocar entregas a caminhões partindo do Centro de Distribuição de referência mais próximo ao destino.
-   Minimizar os custos de transporte, primariamente o tempo total de viagem das rotas planejadas.
-   Garantir o cumprimento das restrições operacionais: capacidade dos caminhões, limite de horas de trabalho diário e prazos de entrega individuais.
-   Implementar e comparar múltiplas estruturas de dados para representação de grafos (mapa logístico), analisando seu impacto no tempo de execução e no uso de memória do algoritmo de Dijkstra (com variações de fila de prioridade).
-   Fornecer um sistema de simulação que permita a visualização dos resultados da roteirização e a coleta de dados para análise de desempenho.

## 🎓 Unidade Curricular Digital

- **Estrutura de Dados e Análise de Algoritmos**
- **Professor:** Glauber Galvão

## 👥 Integrantes do Projeto

- [**Anderson Corrêa**](https://github.com/Anderson-Andy-Correa) - UNISOCIESC - Definição do problema, modelagem de dados, desenvolvimento do código principal
- **Elison Walter Ronchi** - UNISOCIESC - Produção textual do relatório
- **Erick de Jesus Santana** - UNIFACS - Produção textual do relatório
- **Felipe Magalhães de Araújo Carneiro** - USJT - Desenvolvimento dos testes e documentação in-code, slides e edição do vídeo do pitch
- [**Kéure Passos Soares**](https://github.com/KeurePassos) - UNISOCIESC - Definição do problema, levantamento de requisitos
- [**Lucas Longo**](https://github.com/2005LucasLongo) - UNISOCIESC - Definição do problema, organização dos arquivos, integração dos membros do grupo, gerenciamento de processos e diagramação do relatório conforme as normas ABNT

## 🛠️ Tecnologias Utilizadas

-   **Linguagem Principal:** Python (versão 3.10+)
-   **Bibliotecas Principais:**
    -   `matplotlib`: Para a geração de gráficos comparativos de desempenho.
    -   `networkx`: Utilizada como uma das implementações de grafo para benchmark e comparação.
    -   `tabulate`: Para a formatação e exibição de tabelas de resultados no console.
-   **Ambiente de Desenvolvimento Sugerido:** VS Code com a extensão Python.
-   **Controle de Versão:** Git e GitHub.


## 📂 Estrutura do Projeto

O projeto está organizado na seguinte estrutura de pastas principal:

-   **`/model`**: Contém as classes que representam os dados e a lógica de negócio (Ex: `Entrega`, `Caminhao`, `CentroDistribuicao` e as diversas implementações de Grafo).
-   **`/controller`**: Contém a lógica de controle e orquestração (Ex: `Roteirizador`).
-   **`/view`**: Responsável pela apresentação e visualização (Ex: `simulador.py` para saída no console, e a subpasta `plots` para geração de gráficos).
-   **`/utils`**: Módulos utilitários para geração de dados e configuração do mapa (Ex: `gerador_entregas.py`, `mapa_logistico.py`).
-   **`/testes`**: Scripts para a execução de testes, principalmente o framework de comparação de desempenho (`comparador_testes.py`).
-   **`main.py`**: Ponto de entrada principal da aplicação, gerenciador de ambiente virtual e dependências.

## ✨ Principais Funcionalidades Implementadas

-   Modelagem de entidades logísticas: Entregas, Caminhões e Centros de Distribuição.
-   Implementação de múltiplas estruturas de dados para representação de grafos:
    -   Lista de Adjacência (com variações de fila Heap/Lista no Dijkstra)
    -   Matriz de Adjacência (com variações de fila Heap/Lista no Dijkstra)
    -   Lista de Arestas (com variações de fila Heap/Lista no Dijkstra)
    -   Dicionário de Dicionários (com variações de fila Heap/Lista no Dijkstra)
    -   Grafo com Objetos (com variações de fila Heap/Lista no Dijkstra)
    -   Wrapper para NetworkX (utilizando Dijkstra nativo).
-   Algoritmo de roteirização (`Roteirizador`) que:
    -   Identifica o Centro de Distribuição de referência mais próximo ao destino da entrega.
    -   Aloca entregas a caminhões considerando capacidade de carga, horas de operação e prazos individuais das entregas.
    -   Otimiza a sequência de paradas para rotas com múltiplas entregas (via permutação para um número pequeno de paradas).
    -   Utiliza o algoritmo de Dijkstra para cálculo de caminhos mínimos entre pontos.
-   Simulação de roteirização com exibição de resultados detalhados no console.
-   Framework de testes comparativos para analisar tempo de execução e uso de memória das diferentes estruturas de grafo.
-   Geração automática de gráficos de desempenho (tempo vs. volume, memória vs. volume) para as estruturas testadas.


## 🚀 Como Configurar e Executar

Siga as etapas abaixo para configurar o ambiente e executar o projeto:

### Pré-requisitos

-   **Python:** Certifique-se de ter o Python instalado (recomendado Python 3.10 ou superior). Verifique com `python --version`.
-   **Git:** Necessário para clonar o repositório.
-   (Opcional) **VS Code** ou outro editor de sua preferência.

### Passo 1: Clonar o Repositório

Abra um terminal ou prompt de comando e clone o repositório:

```bash
git clone https://github.com/2005LucasLongo/A3-Estruturas-de-dados-e-analise-de-algoritmos.git
```

### Passo 2: Execução Principal via main.py

O método recomendado para executar o projeto é através do script main.py. Ele foi projetado para verificar e tentar configurar automaticamente um ambiente virtual (venv) e instalar as dependências listadas no arquivo requirements.txt na primeira execução. Isso ajuda a evitar problemas de compatibilidade e garante que todas as bibliotecas necessárias estejam disponíveis.

**Para executar:**

Navegue até a pasta raiz do projeto no seu terminal e execute:

```bash
python main.py
```

Ou, em alguns sistemas Windows, você pode conseguir executar dando um duplo clique no arquivo main.py.

**Comportamento Padrão do main.py:**
Por padrão, ao executar main.py, o sistema realizará uma simulação básica de roteirização (chamando a função simular()) e exibirá os resultados no console.

### Passo 3: Executando a Análise Comparativa de Desempenho
Para realizar a análise comparativa completa das estruturas de dados (Parte 3 do trabalho), que inclui a execução de múltiplos cenários de teste, a coleta de dados de tempo e memória, a exibição de uma tabela consolidada e a geração dos gráficos comparativos (salvos em view/plots/imagens_graficos/), você precisará fazer uma pequena modificação no arquivo main.py:

1. Abra o arquivo main.py em um editor de texto.

2. Localize o seguinte trecho de código (geralmente próximo ao final do bloco if __name__ == "__main__":):

```python
# ... (outros códigos como time.sleep(1), simular()) ...
# comparar_algoritmos_estruturas() # <--- LINHA COMENTADA
input("\n✅ Execução concluída. Pressione Enter para sair...")
```

3. **Descomente** a linha # comparar_algoritmos_estruturas() removendo o **#** do início:

```python
# ... (outros códigos como time.sleep(1), simular()) ...
comparar_algoritmos_estruturas() # <--- LINHA DESCOMENTADA
input("\n✅ Execução concluída. Pressione Enter para sair...")
```

(Certifique-se de que a função comparar_algoritmos_estruturas importada no main.py seja a que efetivamente executa os testes do testes/comparador_testes.py E também aciona a lógica de geração de gráficos, possivelmente chamando a função principal do view/plots/gerar_graficos_finais.py ou tendo essa funcionalidade integrada).
    
4. Salve o arquivo main.py.

5. Execute novamente o main.py como no Passo 2:

```bash
python main.py
```

Agora, além da simulação básica (se ainda estiver sendo chamada antes no main.py), a suíte completa de testes de desempenho será executada, e os gráficos serão gerados. Este processo pode levar alguns minutos, dependendo do número de cenários e da complexidade dos testes.

6. **(Opcional) Executar Apenas a Simulação Básica Diretamente**

Se desejar rodar apenas a simulação básica de roteirização (sem a análise comparativa de desempenho e sem as verificações de ambiente do main.py, assumindo que as dependências já estão instaladas no seu ambiente ativo), você pode executar:

```bash
python -m view.simulador
```

## 📊 Como Interpretar os Resultados dos Testes

Ao executar a análise comparativa de desempenho (Passo 3 acima), o sistema gerará uma tabela de resultados no console e gráficos de imagem. Aqui estão algumas dicas para interpretá-los:

* Objetivo Principal dos Testes: Comparar a eficiência (tempo de execução e uso de memória) de diferentes estruturas de dados para representar o mapa logístico e o impacto do tipo de fila de prioridade (Heap vs. Lista Simples) no algoritmo de Dijkstra.

* Métricas Chave:
    * Tempo de Execução (s): Medido para a função roteirizador.alocar_entregas(). Valores menores indicam maior rapidez no processamento da roteirização para um dado cenário.

    * Pico de Memória (KB): Indica o máximo de memória que o processo utilizou durante a roteirização. Valores menores são preferíveis, especialmente para cenários com grande volume de dados.
    
    * Sucessos/Erros na Alocação: Para este projeto, espera-se que o número de entregas alocadas com sucesso (ou não) seja consistente entre as diferentes estruturas de grafo, pois a lógica de negócio para alocação é a mesma. Diferenças aqui podem indicar particularidades, mas o foco principal da comparação está no tempo e na memória.

* Observando os Gráficos:

    * Gráfico de Tempo de Execução: Verifique como as barras (ou linhas) de cada estrutura se comportam à medida que o número de entregas aumenta. Estruturas mais escaláveis apresentarão um crescimento de tempo menos acentuado. Compare as alturas das barras para um mesmo volume de entregas para ver qual foi mais rápida. Observe a diferença entre as versões "Heap" e "Lista Simples" para cada tipo de grafo.
    
    * Gráfico de Pico de Memória: Analise quais estruturas consomem mais ou menos memória e como esse consumo evolui com o aumento do número de entregas.

* Exemplo de Análise Esperada: Teoricamente, para grafos esparsos como mapas rodoviários, representações como Lista de Adjacência ou Dicionário de Dicionários, quando combinadas com uma fila de prioridade baseada em Heap para o Dijkstra, devem apresentar melhor desempenho em tempo do que uma Matriz de Adjacência ou uma Lista de Arestas pura. Os testes visam confirmar ou identificar nuances dessa expectativa.

* Relatório Completo: A análise detalhada, conclusões e justificativas para a escolha da estrutura de dados mais eficiente para este projeto estão contidas no [relatório técnico completo](https://docs.google.com/document/d/1LmGRJYOzFCzpiWqjJLpmuO9awjAzF2ca90UNLVBxbrU/edit?tab=t.0).

## 💡 Considerações sobre a Implementação

O projeto aplica conceitos de Estrutura de Dados e Análise de Algoritmos para desenvolver uma solução para o problema de roteirização de veículos. A otimização da alocação de entregas considera múltiplas restrições e utiliza o algoritmo de Dijkstra (com diferentes implementações de fila de prioridade) para o cálculo de caminhos mínimos. A análise comparativa de diferentes representações de grafos (listas de adjacência, matrizes de adjacência, lista de arestas, dicionários, objetos e NetworkX) visa identificar as abordagens mais eficientes em termos de tempo de processamento e uso de memória para o contexto do problema.