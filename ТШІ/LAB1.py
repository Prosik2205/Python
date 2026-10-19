import math
import heapq
from collections import deque
from itertools import count
from time import perf_counter


class Problem:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        return state == self.goal

    def step_cost(self, state, action, next_state):
        return 1

    def heuristic(self, state):
        return 0


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0 if parent is None else parent.depth + 1

    def expand(self, problem):
        children = []

        for action in problem.actions(self.state):
            next_state = problem.result(self.state, action)

            cost = self.path_cost + problem.step_cost(
                self.state,
                action,
                next_state
            )

            children.append(
                Node(next_state, self, action, cost)
            )

        return children

    def path(self):
        path = []
        node = self

        while node:
            path.append(node.state)
            node = node.parent

        return list(reversed(path))


# Координати міст для евристики
coordinates = {
    "A": (0, 0),
    "B": (2, 2),
    "C": (4, 1),
    "D": (5, 5),
    "E": (6, 2),
    "F": (8, 3),
    "G": (9, 1),
    "H": (10, 4),
}


# Граф міст: сусіднє місто -> вартість дороги
graph = {
    "A": {"B": 3, "C": 5, "D": 9},
    "B": {"A": 3, "C": 3, "D": 5},
    "C": {"A": 5, "B": 3, "E": 3, "G": 6},
    "D": {"A": 9, "B": 5, "F": 5, "H": 8},
    "E": {"C": 3, "F": 3, "G": 4},
    "F": {"D": 5, "E": 3, "H": 3},
    "G": {"C": 6, "E": 4, "H": 4},
    "H": {"D": 8, "F": 3, "G": 4},
}


class RouteProblem(Problem):
    def __init__(self, graph, coordinates, initial, goal):
        super().__init__(initial, goal)
        self.graph = graph
        self.coordinates = coordinates

    def actions(self, state):
        return list(self.graph[state].keys())

    def result(self, state, action):
        return action

    def step_cost(self, state, action, next_state):
        return self.graph[state][next_state]

    def heuristic(self, state):
        x1, y1 = self.coordinates[state]
        x2, y2 = self.coordinates[self.goal]

        return math.hypot(x2 - x1, y2 - y1)


def make_result(node, expanded, start_time):
    return {
        "found": node is not None,
        "path": node.path() if node else [],
        "length": node.depth if node else 0,
        "cost": node.path_cost if node else math.inf,
        "expanded": expanded,
        "time": perf_counter() - start_time
    }


# -------------------- BFS --------------------

def bfs(problem):
    start = perf_counter()

    root = Node(problem.initial)
    frontier = deque([root])
    frontier_states = {root.state}
    explored = set()
    expanded = 0

    while frontier:
        node = frontier.popleft()
        frontier_states.remove(node.state)

        if node.state in explored:
            continue

        explored.add(node.state)
        expanded += 1

        for child in node.expand(problem):

            if (
                child.state in explored
                or child.state in frontier_states
            ):
                continue

            if problem.goal_test(child.state):
                return make_result(child, expanded, start)

            frontier.append(child)
            frontier_states.add(child.state)

    return make_result(None, expanded, start)


# -------------------- DFS --------------------

def dfs(problem):
    start = perf_counter()

    frontier = [Node(problem.initial)]
    explored = set()
    expanded = 0

    while frontier:
        node = frontier.pop()

        if problem.goal_test(node.state):
            return make_result(node, expanded, start)

        if node.state in explored:
            continue

        explored.add(node.state)
        expanded += 1

        for child in reversed(node.expand(problem)):
            if child.state not in explored:
                frontier.append(child)

    return make_result(None, expanded, start)


# -------------------- IDDFS --------------------

def depth_limited_search(problem, limit):
    root = Node(problem.initial)
    expanded = 0

    def search(node, depth_left, path_states):
        nonlocal expanded

        if problem.goal_test(node.state):
            return node

        if depth_left == 0:
            return None

        expanded += 1

        for child in node.expand(problem):

            if child.state in path_states:
                continue

            path_states.add(child.state)

            result = search(
                child,
                depth_left - 1,
                path_states
            )

            if result:
                return result

            path_states.remove(child.state)

        return None

    result = search(root, limit, {root.state})

    return result, expanded


def iddfs(problem, max_depth=50):
    start = perf_counter()
    total_expanded = 0

    for limit in range(max_depth + 1):

        node, expanded = depth_limited_search(
            problem,
            limit
        )

        total_expanded += expanded

        if node:
            return make_result(
                node,
                total_expanded,
                start
            )

    return make_result(None, total_expanded, start)


# -------------------- GREEDY --------------------

def greedy(problem):
    start = perf_counter()

    root = Node(problem.initial)
    frontier = []
    order = count()

    explored = set()
    frontier_states = {root.state}
    expanded = 0

    heapq.heappush(
        frontier,
        (
            problem.heuristic(root.state),
            next(order),
            root
        )
    )

    while frontier:
        _, _, node = heapq.heappop(frontier)

        frontier_states.discard(node.state)

        if node.state in explored:
            continue

        if problem.goal_test(node.state):
            return make_result(node, expanded, start)

        explored.add(node.state)
        expanded += 1

        for child in node.expand(problem):

            if (
                child.state in explored
                or child.state in frontier_states
            ):
                continue

            heapq.heappush(
                frontier,
                (
                    problem.heuristic(child.state),
                    next(order),
                    child
                )
            )

            frontier_states.add(child.state)

    return make_result(None, expanded, start)


# -------------------- A* --------------------

def astar(problem):
    start = perf_counter()

    root = Node(problem.initial)
    frontier = []
    order = count()

    best_g = {root.state: 0}
    expanded = 0

    heapq.heappush(
        frontier,
        (
            problem.heuristic(root.state),
            next(order),
            root
        )
    )

    while frontier:
        _, _, node = heapq.heappop(frontier)

        if node.path_cost > best_g.get(node.state, math.inf):
            continue

        if problem.goal_test(node.state):
            return make_result(node, expanded, start)

        expanded += 1

        for child in node.expand(problem):

            if child.path_cost < best_g.get(
                child.state,
                math.inf
            ):
                best_g[child.state] = child.path_cost

                f = (
                    child.path_cost
                    + problem.heuristic(child.state)
                )

                heapq.heappush(
                    frontier,
                    (
                        f,
                        next(order),
                        child
                    )
                )

    return make_result(None, expanded, start)


# -------------------- IDA* --------------------

def ida_search(problem, node, threshold, path_states):
    f = node.path_cost + problem.heuristic(node.state)

    if f > threshold:
        return None, f, 0

    if problem.goal_test(node.state):
        return node, threshold, 0

    minimum = math.inf
    expanded = 1

    for child in node.expand(problem):

        if child.state in path_states:
            continue

        path_states.add(child.state)

        result, new_threshold, child_expanded = ida_search(
            problem,
            child,
            threshold,
            path_states
        )

        expanded += child_expanded

        if result:
            return result, threshold, expanded

        minimum = min(minimum, new_threshold)

        path_states.remove(child.state)

    return None, minimum, expanded


def idastar(problem):
    start = perf_counter()

    root = Node(problem.initial)
    threshold = problem.heuristic(root.state)
    total_expanded = 0

    while True:

        node, new_threshold, expanded = ida_search(
            problem,
            root,
            threshold,
            {root.state}
        )

        total_expanded += expanded

        if node:
            return make_result(
                node,
                total_expanded,
                start
            )

        if new_threshold == math.inf:
            return make_result(
                None,
                total_expanded,
                start
            )

        threshold = new_threshold


# -------------------- MAIN --------------------

def main():
    problem = RouteProblem(
        graph,
        coordinates,
        "A",
        "H"
    )

    algorithms = {
        "BFS": bfs,
        "DFS": dfs,
        "IDDFS": iddfs,
        "Greedy": greedy,
        "A*": astar,
        "IDA*": idastar
    }

    results = {
        name: algorithm(problem)
        for name, algorithm in algorithms.items()
    }

    print(
        f"{'Алгоритм':<10}"
        f"{'Рішення':<12}"
        f"{'Переходів':<12}"
        f"{'Вартість':<12}"
        f"{'Вузлів':<12}"
        f"{'Час, с':<14}"
        f"Маршрут"
    )

    print("-" * 100)

    for name, result in results.items():

        print(
            f"{name:<10}"
            f"{'Так' if result['found'] else 'Ні':<12}"
            f"{result['length']:<12}"
            f"{result['cost']:<12.2f}"
            f"{result['expanded']:<12}"
            f"{result['time']:<14.8f}"
            f"{' -> '.join(result['path'])}"
        )


if __name__ == "__main__":
    main()