# NOTE TO STUDENT: Please read the handout before continuing.

from tilegameproblem import TileGame
from dgraph import DGraph
from queue import Queue, LifoQueue, PriorityQueue


def bfs(problem):
    start_state = problem.get_start_state()
    dist = {start_state: 0}
    prev = {start_state: None}
    q = Queue()
    q.put(start_state)

    ans = []

    while not q.empty():
        head_state = q.get()

        # Found goal state
        if problem.is_goal_state(head_state):
            while head_state is not None:
                ans.append(head_state)
                head_state = prev.get(head_state)
            ans.reverse()
            return ans

        # Extend current state
        next_states = problem.get_successors(head_state)
        for next_state in next_states:

            if next_state in dist:
                continue

            q.put(next_state)
            dist[next_state] = dist.get(head_state) + 1
            prev[next_state] = head_state

    return ans


def dfs(problem):
    start_state = problem.get_start_state()
    ans = []
    prev = {start_state: None}
    stack = LifoQueue()
    stack.put(start_state)

    while not stack.empty():
        head_state = stack.get()
        next_states = [s for s in problem.get_successors(head_state).keys() if s not in prev]

        for next_state in next_states:
            stack.put(next_state)
            prev[next_state] = head_state

            if problem.is_goal_state(next_state):
                while next_state is not None:
                    ans.append(next_state)
                    next_state = prev.get(next_state)
                ans.reverse()
                return ans
    return [start_state]


def helper(state, vis, ans, dep, problem):
    if dep < 0:
        return False

    if problem.is_goal_state(state):
        return True

    next_states = problem.get_successors(state)
    for next_state in next_states:
        if problem.is_goal_state(next_state):
            ans.append(next_state)
            return True

    for next_state in next_states:
        if (next_state not in vis) or (vis[next_state] < dep - 1):
            vis[next_state] = dep - 1
            ans.append(next_state)
            is_found = helper(next_state, vis, ans, dep - 1, problem)
            if is_found:
                return True
            ans.pop()

    return False


def ids(problem):
    for max_depth in range(1000):
        start_state = problem.get_start_state()
        ans = [start_state]

        vis = {start_state: max_depth}
        is_found = helper(start_state, vis, ans, max_depth, problem)
        if is_found:
            return ans

    return []


def bds(problem, goal):
    q = [Queue(), Queue()]
    q_idx = 0
    start_state = problem.get_start_state()
    prev = [{start_state: None}, {goal: None}]
    q[0].put(start_state)
    q[1].put(goal)

    while True:
        qt = Queue()
        while not q[q_idx].empty():
            head_state = q[q_idx].get()
            if head_state in prev[1 - q_idx]:
                ans = []
                now_state = head_state
                while now_state is not None:
                    ans.append(now_state)
                    now_state = prev[0][now_state]
                ans.reverse()

                now_state = prev[1][head_state]
                while now_state is not None:
                    ans.append(now_state)
                    now_state = prev[1][now_state]

                return ans

            next_states = [s for s in problem.get_successors(head_state).keys() if s not in prev[q_idx]]
            for next_state in next_states:
                prev[q_idx][next_state] = head_state
                qt.put(next_state)
        q[q_idx] = qt

        q_idx = 1 - q_idx


def astar(problem, heur):
    start_state = problem.get_start_state()
    dist = {start_state: 0}
    prev = {start_state: None}
    q = PriorityQueue()
    q.put((heur(start_state), start_state))
    vis = {}
    ans = []

    while not q.empty():
        head_f, head_state = q.get()
        vis[head_state] = True

        # Found goal state
        if problem.is_goal_state(head_state):
            while head_state is not None:
                ans.append(head_state)
                head_state = prev.get(head_state)
            ans.reverse()
            return ans

        # Extend current state
        next_states = problem.get_successors(head_state)
        for next_state in next_states:

            if next_state in vis:
                continue

            dist[next_state] = dist.get(head_state) + 1
            q.put((heur(next_state) + dist.get(next_state), next_state))
            prev[next_state] = head_state

    return ans


### SPECIFIC TO THE TILEGAME PROBLEM


def tilegame_heuristic(state):
    dist = 0
    sample = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    pos = {}
    for i in range(3):
        for j in range(3):
            pos[sample[i][j]] = (i, j)

    for i in range(3):
        for j in range(3):
            p = pos[state[i][j]]
            dist += abs(p[0] - i) + abs(p[1] - j)

    return dist / 2.0

### YOUR SANDBOX ###


def main():
    """
	Do whatever you want in here; this is for you.
	An example below shows how your functions might be used.
	"""
    # sys.setrecursionlimit(100000)
    # initialize a random 3x3 TileGame problem
    tg = TileGame(3)
    # print(TileGame.board_to_pretty_string(tg.get_start_state()))
    # compute path
    # path = bfs(tg)
    # path = dfs(tg)
    # path = ids(tg)
    path = bds(tg, ((1, 2, 3), (4, 5, 6), (7, 8, 9)))
    # path = bds(tg, ((1,2),(3,4)))
    # path = astar(tg, tilegame_heuristic)
    # display path
    TileGame.print_pretty_path(path)
    print(len(path))

    # an example with DGraphs:
    small_dgraph = DGraph([[None, 1], [1, None]], {1})
    print(bfs(small_dgraph))


if __name__ == "__main__":
    main()
