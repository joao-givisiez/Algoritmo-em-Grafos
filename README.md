# Heurística Híbrida para o Problema de Roteamento de Arcos Capacitado (CARP)

Este projeto implementa uma solução heurística para o Problema de Roteamento de Arcos Capacitado (CARP), um desafio clássico em otimização e logística. A abordagem combina uma fase construtiva para gerar uma solução inicial viável e uma fase de melhoria baseada em Variable Neighborhood Search (VNS) para refinar essa solução.

## Estrutura do Projeto

- `rodar_todas.py`: O script principal que orquestra todo o processo. Ele lê todas as instâncias da pasta `Ins/`, aplica as heurísticas e salva os resultados na pasta `SolucoesFinais/`.
- `leitura.py`: Responsável por ler e interpretar os arquivos de instância `.dat`, extraindo informações como capacidade dos veículos, depósito, e a lista de serviços obrigatórios (nós, arestas e arcos).
- `grafo.py`: Contém a modelagem do grafo. Utiliza uma lista de adjacência para representar as conexões e implementa o algoritmo de Dijkstra para calcular os caminhos mais curtos entre os nós, com um sistema de cache para otimizar o desempenho.
- `construtivo.py`: Implementa a heurística construtiva que gera uma solução inicial viável, garantindo que todas as demandas sejam atendidas e que as restrições de capacidade dos veículos sejam respeitadas.
- `melhoria.py`: Implementa a heurística de melhoria VNS para otimizar a solução inicial.

## Modelagem do Grafo

O grafo é representado por uma **lista de adjacência**, implementada com um dicionário em Python, onde cada chave é um nó e o valor é uma lista de tuplas `(vizinho, custo)`.

- O grafo é não direcionado para arestas e direcionado para arcos, conforme especificado nos arquivos de instância.
- Para calcular o custo de deslocamento entre dois pontos quaisquer, utilizamos o **algoritmo de Dijkstra**. Para evitar recálculos e acelerar o processo, os resultados de Dijkstra para cada nó de origem são armazenados em um **cache**.

## Metodologia de Solução

A solução é obtida em duas fases principais:

### 1. Fase Construtiva

Uma solução inicial é gerada de forma gulosa. O algoritmo constrói rotas uma a uma, adicionando os serviços obrigatórios mais próximos até que a capacidade do veículo seja atingida. O processo se repete até que todos os serviços tenham sido alocados a uma rota.

### 2. Fase de Melhoria (VNS)

Após a fase construtiva, a solução é refinada usando uma heurística baseada em **Variable Neighborhood Search (VNS)**. O VNS explora sistematicamente diferentes estruturas de vizinhança para encontrar uma solução de melhor qualidade. Os movimentos utilizados são:

- **Relocate**: Move um serviço de uma rota para outra.
- **Swap**: Troca dois serviços entre duas rotas distintas.
- **2-Opt (Intra-rota)**: Inverte um segmento de uma rota para tentar reduzir seu custo total, removendo cruzamentos.

O VNS opera em um laço: ele tenta aplicar o primeiro movimento que resulta em uma melhoria no custo total. Quando uma melhoria é encontrada, o processo é reiniciado a partir da nova solução.

## Critérios de Parada

O processo de otimização para cada instância possui dois critérios de parada:

1.  **Limite de Tempo**: A fase de melhoria (VNS) para cada instância é limitada a um tempo máximo de **200 segundos**. A verificação é feita em pontos-chave do algoritmo para garantir que o processo seja interrompido de forma responsiva.
2.  **Ótimo Local**: Se o VNS completar um ciclo inteiro através de todas as estruturas de vizinhança (Relocate, Swap, 2-Opt) sem encontrar nenhuma melhoria, o algoritmo para, pois considera que um ótimo local foi atingido.

## Formato do Arquivo de Saída

As soluções são salvas em arquivos `sol-{nome_da_instancia}.dat` com o seguinte formato:

- **Linha 1**: Custo total da solução (soma dos custos de todas as rotas).
- **Linha 2**: Número total de rotas na solução.
- **Linha 3**: Tempo de execução da heurística em microssegundos.
- **Linha 4**: Tempo de referência (atualmente, idêntico à linha 3).
- **Linhas seguintes**: Descrição de cada rota, uma por linha, no formato:
  `0 1 {ID_da_Rota} {Demanda_Total} {Custo_da_Rota} {Visitas_Totais} (D 0,1,1) {Serviços} (D 0,1,1)`
  - `{Serviços}`: Uma sequência de serviços no formato `(S id,p1,p2)`, separados por espaços.

**Importante**: Rotas que se tornam vazias durante o processo de melhoria são removidas e não são incluídas no arquivo de solução final.

## Como Executar

1.  Certifique-se de que o Python está instalado.
2.  Coloque os arquivos de instância (`.dat`) na pasta `Ins/`.
3.  Execute o script principal:
    ```bash
    python rodar_todas.py
    ```
4.  Os arquivos de solução serão gerados na pasta `SolucoesFinais/`.
