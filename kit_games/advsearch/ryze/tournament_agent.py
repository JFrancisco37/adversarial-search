import random
import time
import math
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board

# ---------------------------------------------------------------- #
#  1. FUNÇÕES AUXILIARES                                           #
# ---------------------------------------------------------------- #

def evaluate_custom(state: GameState, player:str) -> float:
    """
    Heurística customizada que primeiro trata estados terminais.
    """
    # CORREÇÃO CRÍTICA: Lidar com estados terminais primeiro para evitar crashes.
    if state.is_terminal():
        winner = state.winner()
        if winner == player:
            return math.inf  # Vitória é infinitamente bom
        elif winner is None:
            return 0.0       # Empate é neutro
        else:
            return -math.inf # Derrota é infinitamente ruim

    # Se não for terminal, calcula a heurística.
    board = state.board
    opponent = 'W' if player == 'B' else 'B'
    
    # --- Métrica 1: Controle de Cantos ---
    player_corners = 0
    opponent_corners = 0
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for r, c in corners:
        if board.tiles[r][c] == player:
            player_corners += 1
        elif board.tiles[r][c] == opponent:
            opponent_corners += 1
    score_corners = 200.0 * (player_corners - opponent_corners)

    # --- Métrica 2: Mobilidade Relativa ---
    player_moves = len(board.legal_moves(player))
    opponent_moves = len(board.legal_moves(opponent))
    score_mobility = 20.0 * (player_moves - opponent_moves)
    
    # --- Métrica 3: Contagem de Peças ---
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


def minimax_search(state: GameState, max_depth:int, eval_func:callable) -> Tuple[int, int]:
    """
    Implementação do Minimax com poda Alfa-Beta.
    """
    initial_player = state.player

    def max_value(current_state, alpha, beta, depth):
        if depth == 0 or current_state.is_terminal():
            return eval_func(current_state, initial_player), None
        v = -math.inf
        best_action = None
        successors = [(move, current_state.next_state(move)) for move in current_state.legal_moves()]
        if not successors: return eval_func(current_state, initial_player), None
        best_action = successors[0][0]
        for action, next_state in successors:
            v_prime, _ = min_value(next_state, alpha, beta, depth - 1) if next_state.player != initial_player else max_value(next_state, alpha, beta, depth - 1)
            if v_prime > v: v, best_action = v_prime, action
            alpha = max(alpha, v)
            if alpha >= beta: break
        return v, best_action

    def min_value(current_state, alpha, beta, depth):
        if depth == 0 or current_state.is_terminal():
            return eval_func(current_state, initial_player), None
        v = math.inf
        best_action = None
        successors = [(move, current_state.next_state(move)) for move in current_state.legal_moves()]
        if not successors: return eval_func(current_state, initial_player), None
        best_action = successors[0][0]
        for action, next_state in successors:
            v_prime, _ = max_value(next_state, alpha, beta, depth - 1) if next_state.player == initial_player else min_value(next_state, alpha, beta, depth - 1)
            if v_prime < v: v, best_action = v_prime, action
            beta = min(beta, v)
            if beta <= alpha: break
        return v, best_action

    _, move = max_value(state, -math.inf, math.inf, max_depth)
    return move


# ---------------------------------------------------------------- #
#  2. FUNÇÃO PRINCIPAL (make_move com PROFUNDIDADE LIMITADA)        #
# ---------------------------------------------------------------- #

def make_move(state: GameState) -> Tuple[int, int]:
    """
    Versão final com limite de profundidade para evitar timeout.
    """
    TIME_LIMIT = 4.8 
    start_time = time.time()

    legal_moves = state.legal_moves()
    if not legal_moves:
        return None 
    
    best_move = list(legal_moves)[0]

    # profundidade 4 foi o máximo que conseguimos fazer ser consistente (não tomar timeout com frequência)
    for depth in range(1, 5):
        if time.time() - start_time >= TIME_LIMIT:
            break
        
        current_move = minimax_search(state, depth, evaluate_custom)
        
        if time.time() - start_time < TIME_LIMIT:
            if current_move is not None:
                best_move = current_move
        else:
            break

    return best_move