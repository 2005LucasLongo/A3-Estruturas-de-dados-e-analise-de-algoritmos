# Projeto de Roteirização de Entregas

## Descrição

Este projeto tem como objetivo implementar um sistema de roteirização de entregas, utilizando dados simulados para representar centros de distribuição, caminhões, entregas e destinos. O sistema é projetado para alocar entregas a caminhões de forma otimizada, levando em consideração o tempo de transporte entre centros de distribuição e destinos.

## Unidade Curricular Digital

- **Estrutura de Dados e Análise de Algoritmos**
- **Professor:** Glauber Galvão

## Integrantes do Projeto

- **Anderson Corrêa** - UNISOCIESC - [Função no Projeto]
- **Elison Walter Ronchi** - UNISOCIESC - [Função no Projeto]
- **Erick de Jesus Santana** - UNIFACS - [Função no Projeto]
- **Felipe Magalhães de Araújo Carneiro** - USJT - [Função no Projeto]
- **Kéure Passos Soares** - UNISOCIESC - [Função no Projeto]
- **Lucas Longo** - UNISOCIESC - [Função no Projeto]

## Como Executar os Testes

Para executar os testes, siga as etapas abaixo:

### Pré-requisitos

Certifique-se de ter o **Python** instalado em seu computador. Você pode verificar isso executando o seguinte comando no terminal:

```bash
python --version
```

Além disso, recomendamos o uso do **VS Code** como ambiente de desenvolvimento, embora qualquer editor de texto de sua preferência funcione.

## Passo 1: Baixar o Projeto

Clone o repositório ou baixe o código fonte para o seu computador.

```bash
git clone 'https://github.com/2005LucasLongo/A3-Estruturas-de-dados-e-analise-de-algoritmos'
```

## Passo 2: Executar os Testes

### Teste de Grande Volume

Para testar a performance do sistema com um grande volume de entregas, execute o seguinte comando:

```bash
python -m testes.teste_grande_volume
```

### Testes da Matriz de Volume

Execute os testes utilizando o comando abaixo para validar o sistema com uma matriz de adjacência de distâncias:

```bash
python -m testes.teste_matriz_volume
```

### Teste de Simulação Pequena

Para simular a roteirização com dados de centros de distribuição e entregas:

```bash
python -m view.simulador
```

## Considerações Finais

O projeto utiliza conceitos de **Estrutura de Dados e Análise de Algoritmos** para otimizar a alocação de entregas, simulando um ambiente logístico com caminhões, centros de distribuição e destinos. A otimização da alocação é feita levando em consideração o tempo estimado de viagem entre os pontos, representados através de gráficos e matrizes de adjacência.
