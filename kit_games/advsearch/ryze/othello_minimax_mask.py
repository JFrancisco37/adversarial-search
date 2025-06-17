import random
import math
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]

def make_move(state: GameState) -> Tuple[int, int]:
    """
    Retorna uma jogada para o estado de jogo fornecido.
    """
    max_depth = 3
    return minimax_move(state, max_depth, evaluate_mask)


def evaluate_mask(state: GameState, player:str) -> float:
    """
    Avalia um estado de Othello com base no valor posicional,
    tratando estados terminais primeiro.
    """
    # ETAPA 1: VERIFICAR SE O ESTADO É TERMINAL
    if state.is_terminal():
        winner = state.winner()
        if winner == player:
            return math.inf  # Vitória
        elif winner is None:
            return 0.0       # Empate
        else:
            return -math.inf # Derrota

    # ETAPA 2: SE NÃO FOR TERMINAL, CALCULAR A HEURÍSTICA
    board = state.board.tiles
    player_score = 0
    opponent_score = 0
    opponent = 'W' if player == 'B' else 'B'

    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                player_score += EVAL_TEMPLATE[r][c]
            elif board[r][c] == opponent:
                opponent_score += EVAL_TEMPLATE[r][c]
    
    return float(player_score - opponent_score)