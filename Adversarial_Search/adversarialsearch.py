from adversarialsearchproblem import AdversarialSearchProblem
from gamedag import GameDAG, DAGState


def minimax_helper(asp, state, vis, cnt):
    cnt['n'] += 1
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state), None

    if state in vis:
        return vis[state]

    best_score = None
    best_action = None
    for action in asp.get_available_actions(state):
        score, op_action = minimax_helper(asp, asp.transition(state, action), vis, cnt)
        if best_score is None or score[state.player_to_move()] > best_score[state.player_to_move()]:
            best_score = score
            best_action = action

    vis[state] = (best_score, best_action)

    return best_score, best_action


def minimax(asp):
    cnt = {'n': 0}
    vis = {}
    score, action = minimax_helper(asp, asp.get_start_state(), vis, cnt)
    print(str(cnt['n']) + ' states')
    return action


def ab_helper(asp, state, ab, cnt):
    cnt['n'] += 1
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state), None

    now_ab = [ab[0], ab[1]]
    best_score = [-float('inf'), -float('inf')]
    best_action = None
    idx = state.player_to_move()
    for action in asp.get_available_actions(state):
        score, op_action = ab_helper(asp, asp.transition(state, action), now_ab, cnt)
        if score[idx] > best_score[idx]:
            best_score = score
            best_action = action

        ab_score = score[0] - score[1]
        if idx == 0:
            if ab_score > now_ab[0]:
                now_ab[0] = ab_score
        else:
            if ab_score < now_ab[1]:
                now_ab[1] = ab_score

        if now_ab[0] >= 1 - now_ab[1]:
            break

    return best_score, best_action


def alpha_beta(asp):
    cnt = {'n': 0}
    score, action = ab_helper(asp, asp.get_start_state(), [-1, 1], cnt)
    print(str(cnt['n']) + ' states')
    return action


def eval_func_1(state):
    return [0, 1]


def abc_helper(asp, state, ab, level, eval_func, cnt):
    cnt['n'] += 1
    if level <= 0:
        return eval_func(state), None

    if asp.is_terminal_state(state):
        return asp.evaluate_state(state), None

    now_ab = [ab[0], ab[1]]
    best_score = [-float('inf'), -float('inf')]
    best_action = None
    idx = state.player_to_move()
    for action in asp.get_available_actions(state):
        score, op_action = abc_helper(asp, asp.transition(state, action), now_ab, level - 1, eval_func, cnt)
        if score[idx] > best_score[idx]:
            best_score = score
            best_action = action

        ab_score = score[0] - score[1]
        if idx == 0:
            if ab_score > now_ab[0]:
                now_ab[0] = ab_score
        else:
            if ab_score < now_ab[1]:
                now_ab[1] = ab_score

        if now_ab[0] >= 1 - now_ab[1]:
            break

    return best_score, best_action


def alpha_beta_cutoff(asp, cutoff_ply=10, eval_func=eval_func_1):
    cnt = {'n': 0}
    score, action = abc_helper(asp, asp.get_start_state(), [-1, 1], cutoff_ply, eval_func, cnt)
    print(str(cnt['n']) + ' states')
    return action


def general_minimax_helper(asp, state, cnt):
    cnt['n'] += 1
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state), None

    best_score = None
    best_action = None
    for action in asp.get_available_actions(state):
        score, op_action = general_minimax_helper(asp, asp.transition(state, action), cnt)
        if best_score is None or score[state.player_to_move()] > best_score[state.player_to_move()]:
            best_score = score
            best_action = action

    return best_score, best_action


def general_minimax(asp):
    cnt = {'n': 0}
    score, action = general_minimax_helper(asp, asp.get_start_state(), cnt)
    print(str(cnt['n']) + ' states')
    return action
