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


class Survivor:
    def __init__(self):
        order = ["U", "D", "L", "R"]
        self.order = order

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

    def calc_board_loc_score(self, board, loc):

        pass

    def decide(self, asp):
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board

        ptm = state.ptm
        loc = locs[ptm]
        print(self.calc_board_longest_path(board, loc))

        return "U"

    def cleanup(self, asp):
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
