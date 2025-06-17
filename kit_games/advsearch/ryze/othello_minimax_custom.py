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
    return minimax_move(state, max_depth, evaluate_custom)


def evaluate_custom(state: GameState, player:str) -> float:
    """
    Heurística customizada que trata estados terminais primeiro.
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
    board = state.board
    opponent = 'W' if player == 'B' else 'B'
    
    # --- Métrica 1: Controle de Cantos (Peso Alto) ---
    player_corners = 0
    opponent_corners = 0
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for r, c in corners:
        if board.tiles[r][c] == player:
            player_corners += 1
        elif board.tiles[r][c] == opponent:
            opponent_corners += 1
    score_corners = 200.0 * (player_corners - opponent_corners)

    # --- Métrica 2: Mobilidade Relativa (Peso Médio) ---
    player_moves = len(board.legal_moves(player))
    opponent_moves = len(board.legal_moves(opponent))
    score_mobility = 20.0 * (player_moves - opponent_moves)
    
    # --- Métrica 3: Contagem de Peças (Peso Baixo) ---
    player_pieces = 0
    opponent_pieces = 0
    for r in range(8):
        for c in range(8):
            if board.tiles[r][c] == player:
                player_pieces += 1
            elif board.tiles[r][c] == opponent:
                opponent_pieces += 1
    score_pieces = 1.0 * (player_pieces - opponent_pieces)

    return score_corners + score_mobility + score_pieces