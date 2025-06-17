import random
from typing import Tuple
from ..tttm.gamestate import GameState
from ..tttm.board import Board
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.

def make_move(state: GameState) -> Tuple[int, int]:
    """
    Retorna uma jogada calculada pelo algoritmo minimax para o estado de jogo fornecido.
    :param state: estado para fazer a jogada
    :return: tupla (int, int) com as coordenadas x, y da jogada (lembre-se: 0 é a primeira linha/coluna)
    """
    # Chama a implementação do minimax com poda alfa-beta.
    # A profundidade é ilimitada (-1), pois o jogo é pequeno. 
    # A função 'utility' é passada para avaliar os estados terminais. 
    move = minimax_move(state, max_depth=-1, eval_func=utility)
    return move

def utility(state: GameState, player: str) -> float:
    """
    Retorna a utilidade de um estado terminal para um determinado jogador.
    No Jogo da Velha Invertido, alinhar 3 peças resulta em derrota. 
    A função GameState.winner() já retorna o vencedor de acordo com esta regra.
    """
    # Obtém o vencedor do estado do jogo.
    winner = state.winner()

    # Se não há vencedor (empate), a utilidade é 0.
    if winner is None:
        return 0.0
    # Se o vencedor é o jogador para o qual estamos otimizando, a utilidade é máxima (1).
    elif winner == player:
        return 1.0
    # Se o vencedor é o oponente, a utilidade é mínima (-1).
    else:
        return -1.0