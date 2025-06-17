import random
import math
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

def make_move(state: GameState) -> Tuple[int, int]:
    """
    Retorna uma jogada para o estado de jogo fornecido.
    """
    max_depth = 3
    return minimax_move(state, max_depth, evaluate_count)


def evaluate_count(state: GameState, player:str) -> float:
    """
    Avalia um estado de Othello com base na diferença de peças,
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
    
    player_pieces = 0
    opponent_pieces = 0
    opponent = 'W' if player == 'B' else 'B'

    for row in board:
        for tile in row:
            if tile == player:
                player_pieces += 1
            elif tile == opponent:
                opponent_pieces += 1
    
    return float(player_pieces - opponent_pieces)