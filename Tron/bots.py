#!/usr/bin/python

import numpy as np
from tronproblem import *
from trontypes import CellType, PowerupType
import random, math
import queue

# Throughout this file, ASP means adversarial search problem.


class StudentBot:
    def __init__(self):
        self.BOT_NAME = "T_T"
        self.bot = Thinker()

    def decide(self, asp):
        return self.bot.decide(asp)

    def cleanup(self):
        self.bot = Thinker()

ARMOR_BASE = 0
SPEEDUP_BASE = -0.1
TRAP_BASE = 50
BOMB_BASE = 0.5

MAX_DISTANCE = 225


class Survivor:
    def __init__(self):
        order = ["U", "R", "D", "L"]
        self.order = order
        self.max_longest_path = -1

    def calc_is_met(self, loc, e_loc):
        if np.abs(loc[0] - e_loc[0]) <= 1 and np.abs(loc[1] - e_loc[1]) <= 1:
            return True
        return False

    def calc_enemy_threat(self, asp, intent_state):
        locs = intent_state.player_locs
        board = intent_state.board
        ptm = intent_state.ptm
        loc = locs[ptm]

        possibilities = list(TronProblem.get_safe_actions(board, loc))
        for o in self.order:
            new_loc = TronProblem.move(loc, o)
            if intent_state.player_has_armor(ptm) and board[new_loc[0]][new_loc[1]] == CellType.BARRIER:
                possibilities.append(o)

        max_threat = 1000
        threat_act = "U"
        for act in possibilities:
            new_state = TronProblem.transition(asp, intent_state, act)
            new_loc = TronProblem.move(loc, act)
            e_armor = new_state.player_has_armor(1 - ptm)
            e_longest_path = self.calc_board_longest_path(new_state.board, locs[1 - ptm], e_armor, "3")
            # print(act + ": (me)" + str(tmp_longest_path) + "(enemy)" + str(e_longest_path))

            # tmp_longest_path = self.calc_board_loc_score(new_state.board, TronProblem.move(loc, act), locs[1 - ptm])
            if e_longest_path < max_threat:
                max_threat = e_longest_path
                threat_act = act

        return max_threat

    def calc_board_longest_path(self, board, loc, armor, mark):

        def dfs(pos, step, vis, order, armor):
            res = -1
            vis[pos] = step
            if step > res:
                res = step

                for dir in order:
                    new_pos = TronProblem.move(pos, dir)
                    mark = board[new_pos[0]][new_pos[1]]
                    has_armor = armor
                    if mark != CellType.WALL \
                            and mark != '1' and mark != '2' and vis.get(new_pos) is None:
                        if mark == CellType.BARRIER:
                            if has_armor:
                                has_armor = False
                            else:
                                continue

                        if mark == CellType.ARMOR:
                            has_armor = True

                        tmp_res = dfs(new_pos, step + 1, vis, order, has_armor)
                        if tmp_res > res:
                            res = tmp_res

            return res

        max_res = -1
        order = ["U", "R", "D", "L"]
        # for i in range(4):
        #     tmp = dfs(loc, 0, {}, order)
        #     if tmp > max_res:
        #         max_res = tmp
        #     tmp = dfs(loc, 0, {}, order[::-1])
        #     if tmp > max_res:
        #         max_res = tmp
        #     order.append(order[0])
        #     order = order[1:]
        bonus = 0

        max_res = dfs(loc, bonus, {}, order, armor)
        return max_res

    def calc_powerups_adjopencells(self, board, loc, self_mark):
        q = queue.Queue()
        q.put(loc)
        vis = {loc: 0}
        powerups = []
        adjopencells = [0, 0]

        if self_mark == CellType.ARMOR or self_mark == CellType.BOMB or self_mark == CellType.SPEED or self_mark == CellType.TRAP:
            powerups.append((0, self_mark))

        while not q.empty():
            h = q.get()
            for dir in self.order:
                new_pos = TronProblem.move(h, dir)
                mark = board[new_pos[0]][new_pos[1]]
                if mark != CellType.WALL and mark != CellType.BARRIER \
                        and mark != '1' and mark != '2' and vis.get(new_pos) is None:
                    now_dist = vis.get(h) + 1
                    vis[new_pos] = now_dist
                    q.put(new_pos)
                    if mark == CellType.ARMOR or mark == CellType.BOMB \
                            or mark == CellType.SPEED or mark == CellType.TRAP:
                        powerups.append((now_dist, mark))
                    if now_dist == 1:
                        adjopencells[0] += 1
                    elif now_dist == 2:
                        adjopencells[1] += 1

        return powerups, adjopencells

    def calc_board_loc_score(self, board, loc, enemy_loc, self_mark, armor, asp, new_state):
        longest_path = self.calc_board_longest_path(board, loc, armor, self_mark)
        if longest_path > self.max_longest_path:
            self.max_longest_path = longest_path
        powerups, adjopencells = self.calc_powerups_adjopencells(board, loc, self_mark)

        e_longest_path = self.calc_board_longest_path(board, enemy_loc, False, "3")
        if e_longest_path > self.max_longest_path:
            self.max_longest_path = e_longest_path
        e_powerups, e_adjopencells = self.calc_powerups_adjopencells(board, enemy_loc, board[enemy_loc[0]][enemy_loc[1]])

        max_threat = self.calc_enemy_threat(asp, new_state)

        def calc_openlvl(aoc):
            return (aoc[0] * 2 + aoc[1]) / (8 * 2 + 12)

        def calc_armor_score(dist):
            return ARMOR_BASE * (1 - dist / MAX_DISTANCE)

        def calc_speedup_score(dist, pathlen):
            return SPEEDUP_BASE * (1 - dist / MAX_DISTANCE) ** 3

        def calc_bomb_score(dist, openlvl):
            return BOMB_BASE * (1 - dist / MAX_DISTANCE) * np.sqrt(1 - openlvl)

        def calc_trap_score(dist, e_openlvl):
            return TRAP_BASE * (1 - dist / MAX_DISTANCE) * np.sqrt(1 - e_openlvl)

        total_score = (longest_path - e_longest_path + max_threat) / self.max_longest_path
        for p in powerups:
            if p[1] == '^':
                total_score += calc_speedup_score(p[0], longest_path)
            elif p[1] == '@':
                total_score += calc_armor_score(p[0])
            elif p[1] == '*':
                total_score += calc_trap_score(p[0], calc_openlvl(e_adjopencells))
            elif p[1] == '!':
                total_score += calc_bomb_score(p[0], calc_openlvl(adjopencells))

        # print("Path Score: " + str(longest_path / self.max_longest_path))
        # print("Powerup Score: " + str(total_score - longest_path / self.max_longest_path))

        return total_score

    def decide(self, asp):
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board

        ptm = state.ptm
        loc = locs[ptm]

        possibilities = list(TronProblem.get_safe_actions(board, loc))
        for o in self.order:
            new_loc = TronProblem.move(loc, o)
            if state.player_has_armor(ptm) and board[new_loc[0]][new_loc[1]] == CellType.BARRIER:
                possibilities.append(o)

        longest = -1
        longest_act = "U"
        for act in possibilities:
            new_state = TronProblem.transition(asp, state, act)
            # tmp_longest_path = self.calc_board_longest_path(new_state.board, TronProblem.move(loc, act))
            new_loc = TronProblem.move(loc, act)
            tmp_longest_path = self.calc_board_loc_score(new_state.board, new_loc, locs[1 - ptm],
                                                         board[new_loc[0]][new_loc[1]], new_state.player_has_armor(ptm), asp, new_state)
            if tmp_longest_path > longest:
                longest = tmp_longest_path
                longest_act = act

        return longest_act

    def cleanup(self):
        self.max_longest_path = -1
        pass


class BadSurvivor(Survivor):
    def decide(self, asp):
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board

        ptm = state.ptm
        loc = locs[ptm]

        e_armor = state.player_has_armor(1 - ptm)

        possibilities = list(TronProblem.get_safe_actions(board, loc))
        # if len(possibilities) == 0:
        for o in self.order:
            new_loc = TronProblem.move(loc, o)
            if state.player_has_armor(ptm) and board[new_loc[0]][new_loc[1]] == CellType.BARRIER:
                possibilities.append(o)

        longest = -1000
        longest_act = "U"
        for act in possibilities:
            new_state = TronProblem.transition(asp, state, act)
            new_loc = TronProblem.move(loc, act)
            armor = new_state.player_has_armor(ptm)
            tmp_longest_path = self.calc_board_longest_path(new_state.board, new_loc, armor, board[new_loc[0]][new_loc[1]])
            e_longest_path = self.calc_board_longest_path(new_state.board, locs[1 - ptm], e_armor, "3")
            max_threat = self.calc_enemy_threat(asp, new_state)
            val = tmp_longest_path - e_longest_path + max_threat

            # print(act + board[new_loc[0]][new_loc[1]] + ": (me)" + str(tmp_longest_path) + "(enemy)" + str(e_longest_path) + "(threat)" + str(max_threat))

            # tmp_longest_path = self.calc_board_loc_score(new_state.board, TronProblem.move(loc, act), locs[1 - ptm])
            if val > longest:
                longest = val
                longest_act = act

        return longest_act

    def calc_enemy_threat(self, asp, intent_state):
        locs = intent_state.player_locs
        board = intent_state.board
        ptm = intent_state.ptm
        loc = locs[ptm]

        possibilities = list(TronProblem.get_safe_actions(board, loc))
        for o in self.order:
            new_loc = TronProblem.move(loc, o)
            if intent_state.player_has_armor(ptm) and board[new_loc[0]][new_loc[1]] == CellType.BARRIER:
                possibilities.append(o)

        max_threat = 1000
        threat_act = "U"
        for act in possibilities:
            new_state = TronProblem.transition(asp, intent_state, act)
            new_loc = TronProblem.move(loc, act)
            e_armor = new_state.player_has_armor(1 - ptm)
            e_longest_path = self.calc_board_longest_path(new_state.board, locs[1 - ptm], e_armor, "3")
            # print(act + ": (me)" + str(tmp_longest_path) + "(enemy)" + str(e_longest_path))

            # tmp_longest_path = self.calc_board_loc_score(new_state.board, TronProblem.move(loc, act), locs[1 - ptm])
            if e_longest_path < max_threat:
                max_threat = e_longest_path
                threat_act = act

        return max_threat

    def calc_board_longest_path(self, board, loc, armor, mark):

        def dfs(pos, step, vis, order, armor, bonus):
            res = -1
            vis[pos] = step
            if step > res:
                # print(bonus)
                res = step

                for dir in order:
                    new_pos = TronProblem.move(pos, dir)
                    mark = board[new_pos[0]][new_pos[1]]
                    has_armor = armor
                    if mark != CellType.WALL \
                            and mark != '1' and mark != '2' and vis.get(new_pos) is None:
                        if mark == CellType.BARRIER:
                            if has_armor:
                                has_armor = False
                            else:
                                continue

                        tmp_bonus = 0
                        if mark == CellType.ARMOR:
                            has_armor = True
                            tmp_bonus = (MAX_DISTANCE - step) / 2
                        if mark == CellType.TRAP:
                            tmp_bonus = (MAX_DISTANCE - step) / 2
                        tmp_res = dfs(new_pos, step + 1, vis, order, has_armor, tmp_bonus + bonus)
                        if tmp_res > res:
                            res = tmp_res

            return res

        max_res = -1
        order = ["U", "R", "D", "L"]
        bonus_ = 0
        if mark == CellType.ARMOR:
            bonus_ = 225
        if mark == CellType.TRAP:
            bonus_ = 225
        for i in range(4):
            tmp = dfs(loc, 0, {}, order, armor, bonus_)
            if tmp > max_res:
                max_res = tmp
            tmp = dfs(loc, 0, {}, order[::-1], armor, bonus_)
            if tmp > max_res:
                max_res = tmp
            order.append(order[0])
            order = order[1:]

        # max_res = dfs(loc, 0, {}, order, armor, bonus_)
        return max_res


class Mocker(Survivor):
    def __init__(self):
        super().__init__()
        self.e_last_loc = None
        self.met = False

    def decide(self, asp):
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))

        # if np.random.random() < 0.2 and len(possibilities) > 0:
        #     # print("RANDOM!!!!!!!!!!!!!!!!!!")
        #     random.choice(possibilities)

        nxt_dir = "U"
        e_now_loc = locs[1 - ptm]
        if self.e_last_loc is not None:
            if e_now_loc[0] == self.e_last_loc[0] - 1:
                nxt_dir = "D"
            elif e_now_loc[0] == self.e_last_loc[0] + 1:
                nxt_dir = "U"
            elif e_now_loc[1] == self.e_last_loc[1] - 1:
                nxt_dir = "R"
            else:
                nxt_dir = "L"
        else:
            if board[e_now_loc[0] - 1][e_now_loc[1]] == 'x':
                self.e_last_loc = e_now_loc
                nxt_dir = 'U'
            elif board[e_now_loc[0]][e_now_loc[1] - 1] == 'x':
                self.e_last_loc = e_now_loc
                nxt_dir = 'L'

        # print(nxt_dir)

        # print("Enemy longest Path: " + str(self.calc_board_longest_path(board, e_now_loc)))

        if nxt_dir not in possibilities or self.calc_is_met(loc, e_now_loc) or (self.e_last_loc is not None and self.calc_is_met(loc, self.e_last_loc)):
            self.met = True

        if self.e_last_loc is None or self.met:
            possibilities = list(TronProblem.get_safe_actions(board, loc))
            longest = -1
            longest_act = "U"
            for act in possibilities:
                new_state = TronProblem.transition(asp, state, act)
                new_loc = TronProblem.move(loc, act)
                armor = new_state.player_has_armor(ptm)
                # tmp_longest_path = self.calc_board_loc_score(new_state.board, TronProblem.move(loc, act), locs[1 - ptm])
                tmp_longest_path = self.calc_board_longest_path(new_state.board, TronProblem.move(loc, act), armor, board[new_loc[0]][new_loc[1]])
                # print(act + ":" + str(tmp_longest_path))
                if tmp_longest_path > longest:
                    longest = tmp_longest_path
                    longest_act = act

            self.e_last_loc = e_now_loc
            return longest_act
        else:
            self.e_last_loc = e_now_loc
            return nxt_dir

    def cleanup(self):
        self.e_last_loc = None
        self.met = False


class Attacker(Survivor):
    def __init__(self):
        order = ["R", "D", "L", "U"]
        Survivor.__init__(self)
        self.order = order
        self.visited_barrier_map = {0: [], 1: []}

    def decide(self, asp):
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        self.visited_barrier_map[ptm].append(loc)
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if not possibilities:
            return "R"
        # random.shuffle(possibilities)

        met = self.check_meet(board, locs, ptm)
        same_room, _ = self.get_dist(board, locs[ptm], locs[1 - ptm])

        if same_room and (not met):  # not met yet, attack, shorter dist
            decision = possibilities[0]
            dist = 100
            for move in possibilities:
                next_loc = TronProblem.move(loc, move)
                new_state = TronProblem.transition(asp, state, move)
                if len(TronProblem.get_safe_actions(new_state.board, next_loc)) > 0:
                    cur_same_room, cur_dist = self.get_dist(new_state.board, next_loc, locs[1 - ptm])
                    if cur_same_room and cur_dist < dist:
                        dist = cur_dist
                        decision = move
            return decision
        else:  # met or in different room, survive, longer dist
            longest = -1
            longest_act = possibilities[0]
            for act in possibilities:
                new_state = TronProblem.transition(asp, state, act)
                # tmp_longest_path = self.calc_board_loc_score(new_state.board, TronProblem.move(loc, act), locs[1 - ptm])
                tmp_longest_path = self.calc_board_longest_path(new_state.board, TronProblem.move(loc, act))
                if tmp_longest_path > longest:
                    longest = tmp_longest_path
                    longest_act = act
            return longest_act

    def check_meet(self, board, locs, ptm):
        for i in [0, 0, 0, 0, 1, 1, -1, -1]:
            for j in [1, 1, -1, -1, 0, 0, 0, 0]:
                new_pos = (locs[ptm][0] + i, locs[ptm][1] + j)
                mark = board[new_pos[0]][new_pos[1]]
                if new_pos == locs[1 - ptm]:
                    return True
                if mark == CellType.BARRIER and (new_pos in self.visited_barrier_map[1 - ptm]):
                    return True
        return False

    def get_dist(self, board, loc1, loc2):
        q = queue.Queue()
        visited = {}

        cur_dist = 0
        q.put(loc1)
        visited[loc1] = 0
        while not q.empty():
            loc = q.get()
            cur_dist = visited[loc]

            for i in [0, 0, 1, -1]:
                for j in [1, -1, 0, 0]:
                    new_pos = (loc[0] + i, loc[1] + j)
                    if new_pos == loc2:
                        return True, cur_dist

            possibilities = list(TronProblem.get_safe_actions(board, loc))
            for act in possibilities:
                next_loc = TronProblem.move(loc, act)
                if next_loc not in visited:
                    q.put(next_loc)
                    visited[next_loc] = visited[loc] + 1

        return False, cur_dist

    def cleanup(self):
        self.visited_barrier_map = {0: [], 1: []}


def calc_dist(asp, start):
    state = asp.get_start_state()
    board = state.board
    q = queue.Queue()
    q.put(start)
    dist = {start: 0}

    while not q.empty():
        head = q.get()
        for move in asp.get_available_actions(state):
            new_loc = TronProblem.move(head, move)
            new_mark = board[new_loc[0]][new_loc[1]]
            if new_mark != CellType.WALL and new_mark != CellType.BARRIER and new_mark != '1' and new_mark != '2' and dist.get(new_loc) is None:
                dist[new_loc] = dist.get(head) + 1
                q.put(new_loc)

    return dist


def calc_grid_value(mark, same_room):
    if mark == CellType.SPACE:
        return 1
    if mark == CellType.ARMOR:
        if same_room:
            return 2
        else:
            return 3
    if mark == CellType.TRAP:
        if same_room:
            return 2
        else:
            return 3
    if mark == CellType.SPEED:
        if same_room:
            return 4
        else:
            return -3
    if mark == CellType.BOMB:
        if same_room:
            return 4
        else:
            return 6
    return 1


def eval_board(asp, state, player):
    dists = [calc_dist(asp, state.player_locs[0]), calc_dist(asp, state.player_locs[1])]
    scores = [0, 0]
    same_room = dists[0].get(state.player_locs[1]) is not None

    for r in range(len(state.board)):
        for c in range(len(state.board[0])):
            loc = (r, c)
            mark = state.board[r][c]
            if dists[0].get(loc) is None and dists[1].get(loc) is not None:
                scores[1] += calc_grid_value(mark, same_room)
            elif dists[1].get(loc) is None and dists[0].get(loc) is not None:
                scores[0] += calc_grid_value(mark, same_room)
            elif dists[0].get(loc) is not None and dists[1].get(loc) is not None:
                if dists[0].get(loc) < dists[1].get(loc):
                    scores[0] += calc_grid_value(mark, same_room)
                else:
                    scores[1] += calc_grid_value(mark, same_room)

    if scores[0] < 0:
        scores[0] = 0
    if scores[1] < 0:
        scores[1] = 0
    sum_score = scores[0] + scores[1]
    # print(sum_score)
    return [scores[0] / sum_score, scores[1] / sum_score][player]


def abc_helper(asp, state, ab, level, eval_func, player, cnt):
    if asp.is_terminal_state(state):
        cnt['n'] += 1
        return asp.evaluate_state(state)[player], None

    if level <= 0:
        cnt['n'] += 1
        return eval_func(asp, state, player), None

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


def alpha_beta_cutoff(asp, cutoff_ply=4, eval_func=eval_board):
    cnt = {'n': 0}
    player = asp.get_start_state().player_to_move()
    score, action = abc_helper(asp, asp.get_start_state(), [-float('inf'), float('inf')], cutoff_ply, eval_func, player, cnt)
    # print(str(cnt['n']) + ' states')
    return action


class Thinker:
    def decide(self, asp):
        return alpha_beta_cutoff(asp)

    def cleanup(self):
        pass

class RandBot:
    """Moves in a random (safe) direction"""

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if possibilities:
            return random.choice(possibilities)
        return "U"

    def cleanup(self):
        pass


class WallBot:
    """Hugs the wall"""

    def __init__(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def cleanup(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if not possibilities:
            return "U"
        decision = possibilities[0]
        for move in self.order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            if len(TronProblem.get_safe_actions(board, next_loc)) < 3:
                decision = move
                break
        return decision
