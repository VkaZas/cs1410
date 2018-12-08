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

ARMOR_BASE = 0.2
SPEEDUP_BASE = -0.5
TRAP_BASE = 0.2
BOMB_BASE = 0.2

MAX_DISTANCE = 28


class Survivor:
    def __init__(self):
        order = ["U", "D", "L", "R"]
        self.order = order
        self.max_longest_path = -1

    def calc_board_longest_path(self, board, loc):

        def dfs(pos, step, vis):
            res = -1
            vis[pos] = step
            if step > res:
                res = step

                for dir in self.order:
                    new_pos = TronProblem.move(pos, dir)
                    mark = board[new_pos[0]][new_pos[1]]
                    if mark != CellType.WALL and mark != CellType.BARRIER \
                            and mark != '1' and mark != '2' and vis.get(new_pos) is None:
                        tmp_res = dfs(new_pos, step + 1, vis)
                        if tmp_res > res:
                            res = tmp_res

            return res

        return dfs(loc, 0, {})

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
            tmp_longest_path = self.calc_board_loc_score(new_state.board, TronProblem.move(loc, act), locs[1 - ptm])
            if tmp_longest_path > longest:
                longest = tmp_longest_path
                longest_act = act

        return longest_act

    def cleanup(self):
        self.max_longest_path = -1
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
