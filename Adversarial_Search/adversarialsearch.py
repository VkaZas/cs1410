from adversarialsearchproblem import AdversarialSearchProblem
from gamedag import GameDAG, DAGState


def minimax_helper(asp, state, cnt):
    if asp.is_terminal_state(state):
        cnt['n'] += 1
        return asp.evaluate_state(state), None

    # if state in vis:
    #     return vis[state]

    best_score = None
    best_action = None
    for action in asp.get_available_actions(state):
        score, op_action = minimax_helper(asp, asp.transition(state, action), cnt)
        if best_score is None or score[state.player_to_move()] > best_score[state.player_to_move()]:
            best_score = score
            best_action = action

    # vis[state] = (best_score, best_action)

    return best_score, best_action


def minimax(asp):
    cnt = {'n': 0}
    score, action = minimax_helper(asp, asp.get_start_state(), cnt)
    # print(str(cnt['n']) + ' states')
    return action


def ab_helper(asp, state, ab, player, cnt):
    if asp.is_terminal_state(state):
        cnt['n'] += 1
        return asp.evaluate_state(state)[player], None

    now_ab = [ab[0], ab[1]]
    best_score = None
    best_action = None
    idx = state.player_to_move()
    for action in asp.get_available_actions(state):
        score, op_action = ab_helper(asp, asp.transition(state, action), now_ab, player, cnt)
        if idx == player:
            if best_score is None or score > best_score:
                best_score = score
                best_action = action
            if best_score > now_ab[0]:
                now_ab[0] = best_score
        else:
            if best_score is None or score < best_score:
                best_score = score
                best_action = action
            if best_score < now_ab[1]:
                now_ab[1] = best_score

        if now_ab[0] >= now_ab[1]:
            break

    return best_score, best_action


def alpha_beta(asp):
    cnt = {'n': 0}
    player = asp.get_start_state().player_to_move()
    score, action = ab_helper(asp, asp.get_start_state(), [-float('inf'), float('inf')], player, cnt)
    # print(str(cnt['n']) + ' states')
    return action


def eval_func_1(state):
    import random
    return random.random()


def abc_helper(asp, state, ab, level, eval_func, player, cnt):
    if asp.is_terminal_state(state):
        cnt['n'] += 1
        return asp.evaluate_state(state)[player], None

    if level <= 0:
        cnt['n'] += 1
        return eval_func(state), None

    now_ab = [ab[0], ab[1]]
    best_score = None
    best_action = None
    idx = state.player_to_move()
    for action in (asp.get_available_actions(state)):
        score, op_action = abc_helper(asp, asp.transition(state, action), now_ab, level - 1, eval_func, player, cnt)
        if idx == player:
            if best_score is None or score > best_score:
                best_score = score
                best_action = action
            if best_score > now_ab[0]:
                now_ab[0] = best_score
        else:
            if best_score is None or score < best_score:
                best_score = score
                best_action = action
            if best_score < now_ab[1]:
                now_ab[1] = best_score

        if now_ab[0] >= now_ab[1]:
            break

    return best_score, best_action


def alpha_beta_cutoff(asp, cutoff_ply=4, eval_func=eval_func_1):
    cnt = {'n': 0}
    player = asp.get_start_state().player_to_move()
    score, action = abc_helper(asp, asp.get_start_state(), [-float('inf'), float('inf')], cutoff_ply, eval_func, player, cnt)
    # print(str(cnt['n']) + ' states')
    return action


def general_minimax_helper(asp, state, player, cnt):
    if asp.is_terminal_state(state):
        cnt['n'] += 1
        return asp.evaluate_state(state)[player], None

    best_score = None
    worst_score = None
    best_action = None
    for action in asp.get_available_actions(state):
        score, op_action = general_minimax_helper(asp, asp.transition(state, action), player, cnt)
        if best_score is None or score > best_score:
            best_score = score
            best_action = action
        if worst_score is None or score < worst_score:
            worst_score = score

        if state.player_to_move() == player:
            worst_score = best_score

    return worst_score, best_action


def general_minimax(asp):
    cnt = {'n': 0}
    player = asp.get_start_state().player_to_move()
    score, action = general_minimax_helper(asp, asp.get_start_state(), player, cnt)
    # print(str(cnt['n']) + ' states')
    return action
