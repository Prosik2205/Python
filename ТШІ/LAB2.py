import math
import time
from dataclasses import dataclass


MAX_PLAYER = 1
MIN_PLAYER = -1

WIN_SCORE = 10000


# ============================================================
# БАЗОВИЙ КЛАС ГРИ
# ============================================================

class Game:
    def initial_state(self):
        raise NotImplementedError

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_terminal(self, state):
        raise NotImplementedError

    def utility(self, state, player):
        raise NotImplementedError

    def eval(self, state, player):
        raise NotImplementedError

    def current_player(self, state):
        raise NotImplementedError


# ============================================================
# П'ЯТНАШКИ — ВАРІАНТ 7
# ============================================================

class FifteenGame(Game):

    GOAL = (
        1,  2,  3,  4,
        5,  6,  7,  8,
        9, 10, 11, 12,
        13, 14, 15, 0
    )

    MOVES = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1)
    }

    def initial_state(self):
        board = (
            1,  2,  3,  4,
            5,  0,  6,  8,
            9, 14,  7, 12,
            13, 11, 10, 15
        )

        return board, MAX_PLAYER

    def actions(self, state):
        board, _ = state

        zero_index = board.index(0)

        row, col = divmod(zero_index, 4)

        possible = []

        for action, (dr, dc) in self.MOVES.items():

            new_row = row + dr
            new_col = col + dc

            if (
                0 <= new_row < 4
                and 0 <= new_col < 4
            ):
                possible.append(action)

        return possible

    def result(self, state, action):
        board, player = state

        zero_index = board.index(0)

        row, col = divmod(zero_index, 4)

        dr, dc = self.MOVES[action]

        new_row = row + dr
        new_col = col + dc

        new_index = new_row * 4 + new_col

        new_board = list(board)

        new_board[zero_index], new_board[new_index] = (
            new_board[new_index],
            new_board[zero_index]
        )

        return tuple(new_board), -player

    def is_terminal(self, state):
        board, _ = state

        return board == self.GOAL

    def utility(self, state, player):
        if not self.is_terminal(state):
            return 0

        if player == MAX_PLAYER:
            return WIN_SCORE

        return -WIN_SCORE

    def manhattan_distance(self, board):
        distance = 0

        for index, tile in enumerate(board):

            if tile == 0:
                continue

            goal_index = tile - 1

            row, col = divmod(index, 4)
            goal_row, goal_col = divmod(goal_index, 4)

            distance += (
                abs(row - goal_row)
                + abs(col - goal_col)
            )

        return distance

    def eval(self, state, player):
        board, _ = state

        distance = self.manhattan_distance(board)

        # Чим менша відстань — тим краще для MAX
        score_for_max = -distance

        if player == MAX_PLAYER:
            return score_for_max

        return -score_for_max

    def current_player(self, state):
        _, player = state

        return player

    def score_for_max(self, state):
        if self.is_terminal(state):
            return self.utility(state, MAX_PLAYER)

        return self.eval(state, MAX_PLAYER)


# ============================================================
# ЛІЧИЛЬНИК ВІДВІДАНИХ ВУЗЛІВ
# ============================================================

@dataclass
class Counter:
    count: int = 0

    def inc(self):
        self.count += 1


# ============================================================
# MINIMAX
# ============================================================

def minimax(game, state, depth, counter):
    counter.inc()

    if depth == 0 or game.is_terminal(state):

        if game.is_terminal(state):
            return game.utility(
                state,
                MAX_PLAYER
            ), None

        return game.eval(
            state,
            MAX_PLAYER
        ), None

    maximizing = (
        game.current_player(state)
        == MAX_PLAYER
    )

    if maximizing:
        best_value = -math.inf
    else:
        best_value = math.inf

    best_action = None

    for action in game.actions(state):

        child = game.result(
            state,
            action
        )

        value, _ = minimax(
            game,
            child,
            depth - 1,
            counter
        )

        if maximizing:

            if value > best_value:
                best_value = value
                best_action = action

        else:

            if value < best_value:
                best_value = value
                best_action = action

    return best_value, best_action


# ============================================================
# ALPHA-BETA
# ============================================================

def alpha_beta(
    game,
    state,
    depth,
    alpha,
    beta,
    counter,
    ordered=False,
    deadline=None
):

    if (
        deadline is not None
        and time.perf_counter() >= deadline
    ):
        raise TimeoutError

    counter.inc()

    if depth == 0 or game.is_terminal(state):

        if game.is_terminal(state):
            return game.utility(
                state,
                MAX_PLAYER
            ), None

        return game.eval(
            state,
            MAX_PLAYER
        ), None

    maximizing = (
        game.current_player(state)
        == MAX_PLAYER
    )

    actions = game.actions(state)

    # Сортування ходів для покращення відсікання
    if ordered:

        actions.sort(
            key=lambda action:
                game.score_for_max(
                    game.result(state, action)
                ),
            reverse=maximizing
        )

    best_action = None

    # ---------------- MAX ----------------

    if maximizing:

        value = -math.inf

        for action in actions:

            child = game.result(
                state,
                action
            )

            child_value, _ = alpha_beta(
                game,
                child,
                depth - 1,
                alpha,
                beta,
                counter,
                ordered,
                deadline
            )

            if child_value > value:
                value = child_value
                best_action = action

            alpha = max(
                alpha,
                value
            )

            if alpha >= beta:
                break

        return value, best_action

    # ---------------- MIN ----------------

    value = math.inf

    for action in actions:

        child = game.result(
            state,
            action
        )

        child_value, _ = alpha_beta(
            game,
            child,
            depth - 1,
            alpha,
            beta,
            counter,
            ordered,
            deadline
        )

        if child_value < value:
            value = child_value
            best_action = action

        beta = min(
            beta,
            value
        )

        if alpha >= beta:
            break

    return value, best_action


# ============================================================
# NEGAMAX + ALPHA-BETA
# ============================================================

def negamax_ab(
    game,
    state,
    depth,
    alpha,
    beta,
    counter
):

    counter.inc()

    player = game.current_player(state)

    if depth == 0 or game.is_terminal(state):

        if game.is_terminal(state):

            return game.utility(
                state,
                player
            ), None

        return game.eval(
            state,
            player
        ), None

    best_value = -math.inf
    best_action = None

    for action in game.actions(state):

        child = game.result(
            state,
            action
        )

        child_value, _ = negamax_ab(
            game,
            child,
            depth - 1,
            -beta,
            -alpha,
            counter
        )

        score = -child_value

        if score > best_value:
            best_value = score
            best_action = action

        alpha = max(
            alpha,
            score
        )

        if alpha >= beta:
            break

    return best_value, best_action


# ============================================================
# ITERATIVE DEEPENING MINIMAX
# ============================================================

def iterative_deepening(
    game,
    state,
    max_depth,
    time_limit=5.0
):

    start = time.perf_counter()

    deadline = start + time_limit

    total_counter = Counter()

    best_action = None
    best_value = None

    completed_depth = 0

    for depth in range(
        1,
        max_depth + 1
    ):

        counter = Counter()

        try:

            value, action = alpha_beta(
                game,
                state,
                depth,
                -math.inf,
                math.inf,
                counter,
                ordered=False,
                deadline=deadline
            )

        except TimeoutError:

            total_counter.count += (
                counter.count
            )

            break

        total_counter.count += (
            counter.count
        )

        best_value = value
        best_action = action

        completed_depth = depth

    return (
        best_value,
        best_action,
        total_counter.count,
        completed_depth
    )


# ============================================================
# ЗАПУСК ОДНОГО АЛГОРИТМУ
# ============================================================

def run_algorithm(
    name,
    game,
    state,
    depth
):

    start = time.perf_counter()

    # ---------------- MINIMAX ----------------

    if name == "Minimax":

        counter = Counter()

        value, action = minimax(
            game,
            state,
            depth,
            counter
        )

        nodes = counter.count

    # ---------------- ALPHA-BETA ----------------

    elif name == "Alpha-Beta":

        counter = Counter()

        value, action = alpha_beta(
            game,
            state,
            depth,
            -math.inf,
            math.inf,
            counter
        )

        nodes = counter.count

    # ---------------- NEGAMAX ----------------

    elif name == "NegaMax+AB":

        counter = Counter()

        value, action = negamax_ab(
            game,
            state,
            depth,
            -math.inf,
            math.inf,
            counter
        )

        nodes = counter.count

    # ---------------- ID-MINIMAX ----------------

    elif name == "ID-Minimax":

        (
            value,
            action,
            nodes,
            completed_depth
        ) = iterative_deepening(
            game,
            state,
            max_depth=depth,
            time_limit=5.0
        )

    # ---------------- SORTED ALPHA-BETA ----------------

    elif name == "Alpha-Beta sorted":

        counter = Counter()

        value, action = alpha_beta(
            game,
            state,
            depth,
            -math.inf,
            math.inf,
            counter,
            ordered=True
        )

        nodes = counter.count

    else:
        raise ValueError(
            "Невідомий алгоритм"
        )

    elapsed = (
        time.perf_counter()
        - start
    )

    return {
        "value": value,
        "action": action,
        "nodes": nodes,
        "time": elapsed
    }


# ============================================================
# ВИВЕДЕННЯ ДОШКИ
# ============================================================

def print_board(board):

    for row in range(4):

        values = board[
            row * 4:
            row * 4 + 4
        ]

        print(
            " ".join(
                f"{x:2}"
                if x != 0
                else " _"
                for x in values
            )
        )


# ============================================================
# MAIN
# ============================================================

def main():

    game = FifteenGame()

    state = game.initial_state()

    board, player = state

    print(
        "Початкова позиція:"
    )

    print_board(board)

    print()

    print(
        "Манхеттенська відстань:",
        game.manhattan_distance(board)
    )

    print(
        "Поточний гравець:",
        "MAX"
        if player == MAX_PLAYER
        else "MIN"
    )

    algorithms = [
        "Minimax",
        "Alpha-Beta",
        "NegaMax+AB",
        "ID-Minimax",
        "Alpha-Beta sorted"
    ]

    depths = [
        2,
        4,
        6
    ]

    results = {}

    for name in algorithms:

        results[name] = {}

        for depth in depths:

            result = run_algorithm(
                name,
                game,
                state,
                depth
            )

            results[name][depth] = result

    print()

    print("=" * 105)

    print(
        f"{'Алгоритм':<20}"
        f"{'d=2 вузлів':<14}"
        f"{'d=2 час':<14}"
        f"{'d=4 вузлів':<14}"
        f"{'d=4 час':<14}"
        f"{'d=6 вузлів':<14}"
        f"{'d=6 час':<14}"
    )

    print("-" * 105)

    for name in algorithms:

        r2 = results[name][2]
        r4 = results[name][4]
        r6 = results[name][6]

        print(
            f"{name:<20}"
            f"{r2['nodes']:<14}"
            f"{r2['time']:<14.8f}"
            f"{r4['nodes']:<14}"
            f"{r4['time']:<14.8f}"
            f"{r6['nodes']:<14}"
            f"{r6['time']:<14.8f}"
        )

    print()
    print("Найкращі ходи при d = 6:")

    for name in algorithms:

        result = results[name][6]

        print(
            f"{name:<20}"
            f"хід = {result['action']:<6} "
            f"оцінка = {result['value']}"
        )


if __name__ == "__main__":
    main()