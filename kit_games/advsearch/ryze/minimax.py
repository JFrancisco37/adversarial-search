import random
from typing import Tuple, Callable
import math



def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Retorna uma jogada calculada pelo algoritmo minimax com poda alfa-beta para o estado de jogo fornecido.
    Esta versão foi ajustada para lidar com turnos não alternados.
    :param state: estado para fazer a jogada (instância de GameState)
    :param max_depth: profundidade máxima de busca (-1 = ilimitada)
    :param eval_func: a função para avaliar um estado terminal ou folha.
                      Deve receber um objeto GameState e uma string identificando o jogador,
                      e retornar um valor float representando a utilidade do estado para esse jogador.
    :return: tupla (int, int) com as coordenadas x, y da jogada.
    """
    
    initial_player = state.player

    def max_value(current_state, alpha, beta, depth):
        if depth == 0 or current_state.is_terminal():
            return eval_func(current_state, initial_player), None

        v = -math.inf
        best_action = None
        
        successors = [(move, current_state.next_state(move)) for move in current_state.legal_moves()]
        if not successors:
             return eval_func(current_state, initial_player), None
        
        best_action = successors[0][0]

        for action, next_state in successors:
            # AJUSTE: Verifica quem joga no próximo estado.
            # Se o jogador for o mesmo, ele continua maximizando (chama max_value).
            if next_state.player == initial_player:
                v_prime, _ = max_value(next_state, alpha, beta, depth - 1 if depth != -1 else -1)
            # Se for o oponente, ele irá minimizar (chama min_value).
            else:
                v_prime, _ = min_value(next_state, alpha, beta, depth - 1 if depth != -1 else -1)
            
            if v_prime > v:
                v = v_prime
                best_action = action
            
            alpha = max(alpha, v)
            
            if alpha >= beta:
                break
                
        return v, best_action

    def min_value(current_state, alpha, beta, depth):
        if depth == 0 or current_state.is_terminal():
            return eval_func(current_state, initial_player), None
            
        v = math.inf
        best_action = None
        
        successors = [(move, current_state.next_state(move)) for move in current_state.legal_moves()]
        if not successors:
            return eval_func(current_state, initial_player), None
        
        best_action = successors[0][0]

        for action, next_state in successors:
            # AJUSTE: Verifica quem joga no próximo estado.
            # Se for o jogador inicial, ele tentará maximizar (chama max_value).
            if next_state.player == initial_player:
                v_prime, _ = max_value(next_state, alpha, beta, depth - 1 if depth != -1 else -1)
            # Se for o mesmo jogador (oponente), ele continua minimizando (chama min_value).
            else:
                v_prime, _ = min_value(next_state, alpha, beta, depth - 1 if depth != -1 else -1)

            if v_prime < v:
                v = v_prime
                best_action = action
            
            beta = min(beta, v)

            if beta <= alpha:
                break
        
        return v, best_action

    # A chamada inicial não muda, começa com o jogador MAX.
    _, move = max_value(state, -math.inf, math.inf, max_depth)
    
    return move