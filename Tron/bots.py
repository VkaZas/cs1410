#!/usr/bin/python

import numpy as np
from tronproblem import *
from trontypes import CellType, PowerupType
import random, math
import queue

# Throughout this file, ASP means adversarial search problem.


class StudentBot:
    """ Write your student bot here"""

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}

        To get started, you can get the current
        state by calling asp.get_start_state()
        """
        return "U"

    def cleanup(self):
        """
        Input: None
        Output: None

        This function will be called in between
        games during grading. You can use it
        to reset any variables your bot uses during the game
        (for example, you could use this function to reset a
        turns_elapsed counter to zero). If you don't need it,
        feel free to leave it as "pass"
        """
        pass

ARMOR_BASE = 0.5
SPEEDUP_BASE = -0.1
TRAP_BASE = 0.5
BOMB_BASE = 0.5

MAX_DISTANCE = 100


class Survivor:
    def __init__(self):
        order = ["U", "R", "D", "L"]
        self.order = order
        self.max_longest_path = -1

    def calc_is_met(self, loc, e_loc):
        if np.abs(loc[0] - e_loc[0]) <= 1 and np.abs(loc[1] - e_loc[1]) <= 1:
            return True
        return False

    def calc_board_longest_path(self, board, loc):

        def dfs(pos, step, vis, order):
            res = -1
            vis[pos] = step
            if step > res:
                res = step

                for dir in order:
                    new_pos = TronProblem.move(pos, dir)
                    mark = board[new_pos[0]][new_pos[1]]
                    if mark != CellType.WALL and mark != CellType.BARRIER \
                            and mark != '1' and mark != '2' and vis.get(new_pos) is None:
                        tmp_res = dfs(new_pos, step + 1, vis, order)
                        if tmp_res > res:
                            res = tmp_res

            return res

        max_res = -1
        order = ["U", "D", "L", "R"]
        for i in range(4):
            tmp = dfs(loc, 0, {}, order)
            if tmp > max_res:
                max_res = tmp
            tmp = dfs(loc, 0, {}, order[::-1])
            if tmp > max_res:
                max_res = tmp
            order.append(order[0])
            order = order[1:]

        # max_res = dfs(loc, 0, {}, order)

        return max_res

    def calc_powerups_adjopencells(self, board, loc):
        q = queue.Queue()
        q.put(loc)
        vis = {loc: 0}
        powerups = []
        adjopencells = [0, 0]

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
                    if mark == CellType.ARMOR or mark == CellType.BOMB or mark == CellType.SPEED or mark == CellType.TRAP:
                        powerups.append((now_dist, mark))
                    if now_dist == 1:
                        adjopencells[0] += 1
                    elif now_dist == 2:
                        adjopencells[1] += 1

        return powerups, adjopencells

    def calc_board_loc_score(self, board, loc, enemy_loc):
        longest_path = self.calc_board_longest_path(board, loc)
        if longest_path > self.max_longest_path:
            self.max_longest_path = longest_path
        powerups, adjopencells = self.calc_powerups_adjopencells(board, loc)
        e_longest_path = self.calc_board_longest_path(board, enemy_loc)
        if e_longest_path > self.max_longest_path:
            self.max_longest_path = e_longest_path
        e_powerups, e_adjopencells = self.calc_powerups_adjopencells(board, enemy_loc)

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

        total_score = longest_path / self.max_longest_path
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
        longest = -1
        longest_act = "U"
        for act in possibilities:
            new_state = TronProblem.transition(asp, state, act)
            tmp_longest_path = self.calc_board_longest_path(new_state.board, TronProblem.move(loc, act))
            # tmp_longest_path = self.calc_board_loc_score(new_state.board, TronProblem.move(loc, act), locs[1 - ptm])
            if tmp_longest_path > longest:
                longest = tmp_longest_path
                longest_act = act

        return longest_act

    def cleanup(self):
        self.max_longest_path = -1
        pass

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
                tmp_longest_path = self.calc_board_loc_score(new_state.board, TronProblem.move(loc, act), locs[1 - ptm])
                # tmp_longest_path = self.calc_board_longest_path(new_state.board, TronProblem.move(loc, act))
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
        # print("met: " + str(met))
        same_room, _ = self.get_dist(board, locs[ptm], locs[1 - ptm])
        # print("same_room: " + str(same_room))

        if same_room and (not met):  # not met yet, attack, shorter dist
            decision = possibilities[0]
            dist = 100
            for move in possibilities:
                next_loc = TronProblem.move(loc, move)
                if len(TronProblem.get_safe_actions(board, next_loc)) > 0:
                    cur_same_room, cur_dist = self.get_dist(board, next_loc, locs[1 - ptm])
                    # print("next loc " + move + " to op: " + str(cur_dist))
                    if cur_same_room and cur_dist < dist:
                        dist = cur_dist
                        decision = move
            return decision
        else:  # met or in different room, survive, longer dist
            longest = -1
            longest_act = possibilities[0]
            for act in possibilities:
                new_state = TronProblem.transition(asp, state, act)
                tmp_longest_path = self.calc_board_loc_score(new_state.board, TronProblem.move(loc, act), locs[1 - ptm])
                # tmp_longest_path = self.calc_board_longest_path(new_state.board, TronProblem.move(loc, act))
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
