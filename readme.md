# Relatório do Trabalho 4 - Busca com Adversário

## 1. Identificação do Grupo


*    João Francisco Hirtenkauf Munhoz – 00275634
*    Luís Antônio Mikhail Dawa – 00313853
*    Mario Augusto Brum da Silveira – 00322868


***

## 2. Bibliotecas Adicionais

Nenhuma biblioteca adicional precisa ser instalada para executar a implementação. O projeto utiliza apenas as bibliotecas padrão do Python e as especificadas no enunciado.

***

## 3. Avaliação do Tic-Tac-Toe Misere

* **O minimax sempre ganha ou empata jogando contra o `randomplayer`?** 
    Sim. Após diversos testes, nosso agente demonstrou ser ótimo, vencendo ou empatando em todas as partidas contra um oponente que realiza jogadas aleatórias.

* **O minimax sempre empata consigo mesmo?** 
    Sim. Quando o agente joga contra si mesmo, o resultado é consistentemente um empate. Isso indica que a estratégia é determinística e ótima, pois nenhum dos jogadores consegue forçar uma vitória contra uma estratégia idêntica.

* **O minimax não perde para você quando você usa a sua melhor estratégia?** 
    Sim. O agente se mostrou invencível contra um jogador humano

***

## 4. Avaliação do Othello

### 4.1. Heurística Customizada

A heurística customizada, implementada no arquivo `othello_minimax_custom.py`, foi projetada para ser superior às heurísticas de contagem de peças e valor posicional. Ela avalia um estado do jogo combinando três métricas estratégicas com pesos diferentes:

1.  **Controle de Cantos (Peso 200.0)**: Atribui um valor muito alto às peças localizadas nos quatro cantos do tabuleiro. Cantos são as posições mais estáveis do jogo, pois não podem ser capturadas.
2.  **Mobilidade Relativa (Peso 20.0)**: Calcula a diferença entre o número de jogadas legais disponíveis para o jogador e para o oponente. Limitar a mobilidade do adversário é uma tática chave em Othello.
3.  **Contagem de Peças (Peso 1.0)**: Utiliza a diferença simples no número de peças. Esta métrica tem o menor peso, pois a quantidade de peças só se torna o fator decisivo no final do jogo.

A função combina esses fatores em um único valor: `score = (200 * score_corners) + (20 * score_mobility) + (1 * score_pieces)`.

**Fonte**: A concepção desta heurística foi desenvolvida com o auxílio de uma LLM (Gemini), baseada em princípios e estratégias conhecidas para o jogo de Othello.

### 4.2. Resultados do Mini-Torneio

Abaixo estão os resultados das partidas entre as três implementações de heurísticas, conforme solicitado na seção 2.2-b do enunciado.

| Partida (Pretas vs. Brancas) | Vencedor | Placar Final (Pretas - Brancas) |
| :--- | :---: | :---: |
| Contagem de Peças **vs** Valor Posicional | **Valor Posicional (W)** | `B 18 - W 46` |
| Valor Posicional **vs** Contagem de Peças | **Valor Posicional (B)** | `B 46 - W 18` |
| Contagem de Peças **vs** Heurística Customizada | **Customizada (W)** | `B 13 - W 51` |
| Heurística Customizada **vs** Contagem de Peças | **Customizada (B)** | `B 47 - W 17` |
| Valor Posicional **vs** Heurística Customizada | **Customizada (W)** | `B 17 - W 47` |
| Heurística Customizada **vs** Valor Posicional | **Customizada (B)** | `B 34 - W 30` |

**Conclusão do Torneio**: A **Heurística Customizada** foi a implementação mais bem-sucedida de todas, vencendo as 4 partidas que disputou contra as outras duas heurísticas. A heurística de Valor Posicional ficou em segundo lugar, com 2 vitórias, e a de Contagem de Peças não venceu nenhuma partida, confirmando ser a estratégia mais fraca.

### 4.3. Implementação para o Torneio

A implementação escolhida para o arquivo `tournament_agent.py`  utiliza o **Minimax com poda alfa-beta em conjunto com a heurística customizada**  e o critério de parada de aprofundamento iterativo, porém com profundidade limitada em 4 (pois foi a maior profundidade alcançada sem que desse timeout durante a execução).

Esta escolha é justificada pelos resultados do mini-torneio, onde a heurística customizada demonstrou clara superioridade. A combinação de uma função de avaliação robusta com uma gestão de tempo eficiente cria um agente competitivo e que respeita as regras do torneio.

### 4.4. Critério de Parada: Iterative Deepening

O algoritmo executa a busca Minimax em um loop, começando com `profundidade = 1` e incrementando a cada iteração, até um máximo de `profundidade = 4`. Antes de iniciar uma nova busca em uma profundidade maior, o tempo decorrido é verificado. Se o tempo estiver próximo do limite de 5 segundos  (definido como 4.8s no código para segurança), o loop é interrompido e a melhor jogada encontrada na maior profundidade concluída com sucesso é retornada.

***

## 5. Extras

Não foram implementados itens opcionais, como o algoritmo MCTS ou outras melhorias não vistas em aula.