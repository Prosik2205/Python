import random
import copy
import statistics
import matplotlib.pyplot as plt


# ============================================================
# БАЗОВІ КЛАСИ
# ============================================================

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = None


class GeneticAlgorithm:
    def __init__(
        self,
        pop_size=100,
        p_cross=0.8,
        p_mut=0.01,
        elite_size=0,
        max_gen=200,
        tournament_k=3,
        adaptive=False,
        seed=None
    ):
        self.pop_size = pop_size
        self.p_cross = p_cross
        self.p_mut = p_mut
        self.elite_size = elite_size
        self.max_gen = max_gen
        self.k = tournament_k
        self.adaptive = adaptive
        self.seed = seed

        self.history = []
        self.convergence_gen = 0

    def create_individual(self):
        raise NotImplementedError

    def fitness_fn(self, individual):
        raise NotImplementedError

    def crossover(self, p1, p2):
        raise NotImplementedError

    def mutate(self, individual, p_mut=None):
        raise NotImplementedError

    def evaluate(self, population):
        for ind in population:
            if ind.fitness is None:
                ind.fitness = self.fitness_fn(ind)

    # Турнірний відбір
    def tournament_select(self, population):
        contestants = random.sample(population, self.k)
        return max(contestants, key=lambda ind: ind.fitness)

    # Однопунктове схрещування
    def one_point_crossover(self, p1, p2):
        point = random.randint(1, len(p1.chromosome) - 1)

        c1 = Individual(
            p1.chromosome[:point] +
            p2.chromosome[point:]
        )

        c2 = Individual(
            p2.chromosome[:point] +
            p1.chromosome[point:]
        )

        return c1, c2

    # Адаптивна мутація
    def adaptive_mutation_rate(
        self,
        population,
        p_min=0.01,
        p_max=0.10,
        threshold=0.01
    ):
        fitnesses = [
            ind.fitness for ind in population
        ]

        diversity = (
            statistics.pstdev(fitnesses)
            if len(fitnesses) > 1 else 0
        )

        if diversity < threshold:
            return p_max

        ratio = min(
            threshold / diversity,
            1.0
        )

        return (
            p_min +
            (p_max - p_min) * ratio
        )

    def run(self):
        if self.seed is not None:
            random.seed(self.seed)

        population = [
            self.create_individual()
            for _ in range(self.pop_size)
        ]

        self.evaluate(population)
        self.history = []

        global_best = copy.deepcopy(
            max(
                population,
                key=lambda ind: ind.fitness
            )
        )

        best_generation = 0

        for gen in range(self.max_gen):

            current_best = max(
                population,
                key=lambda ind: ind.fitness
            )

            self.history.append(
                current_best.fitness
            )

            if current_best.fitness > global_best.fitness:
                global_best = copy.deepcopy(
                    current_best
                )
                best_generation = gen

            # Елітизм
            elite = sorted(
                population,
                key=lambda ind: ind.fitness,
                reverse=True
            )[:self.elite_size]

            elite = [
                copy.deepcopy(ind)
                for ind in elite
            ]

            # Фіксована або адаптивна мутація
            if self.adaptive:
                current_p_mut = (
                    self.adaptive_mutation_rate(
                        population
                    )
                )
            else:
                current_p_mut = self.p_mut

            offspring = []

            needed = (
                self.pop_size -
                self.elite_size
            )

            while len(offspring) < needed:

                p1 = self.tournament_select(
                    population
                )

                p2 = self.tournament_select(
                    population
                )

                if random.random() < self.p_cross:
                    c1, c2 = self.crossover(
                        p1, p2
                    )
                else:
                    c1 = copy.deepcopy(p1)
                    c2 = copy.deepcopy(p2)

                self.mutate(
                    c1,
                    current_p_mut
                )

                self.mutate(
                    c2,
                    current_p_mut
                )

                offspring.extend(
                    [c1, c2]
                )

            population = (
                elite +
                offspring[:needed]
            )

            self.evaluate(population)

        self.convergence_gen = (
            best_generation
        )

        return global_best


# ============================================================
# ONEMAX — ПЕРЕВІРКА БАЗОВОГО ГА
# ============================================================

class OneMaxGA(GeneticAlgorithm):
    def __init__(
        self,
        length=50,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.length = length

    def create_individual(self):
        chromosome = [
            random.randint(0, 1)
            for _ in range(self.length)
        ]

        return Individual(chromosome)

    def fitness_fn(self, individual):
        return sum(
            individual.chromosome
        )

    def crossover(self, p1, p2):
        return self.one_point_crossover(
            p1, p2
        )

    def mutate(
        self,
        individual,
        p_mut=None
    ):
        rate = (
            self.p_mut
            if p_mut is None
            else p_mut
        )

        individual.chromosome = [
            bit ^ 1
            if random.random() < rate
            else bit
            for bit in individual.chromosome
        ]

        individual.fitness = None


# ============================================================
# ВАРІАНТ 7 — PARTITION PROBLEM
# ============================================================

class PartitionGA(GeneticAlgorithm):
    def __init__(
        self,
        numbers,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.numbers = numbers
        self.length = len(numbers)

    def create_individual(self):
        # 0 -> множина A
        # 1 -> множина B

        chromosome = [
            random.randint(0, 1)
            for _ in range(self.length)
        ]

        return Individual(chromosome)

    def difference(self, chromosome):

        sum_a = sum(
            number
            for number, bit
            in zip(
                self.numbers,
                chromosome
            )
            if bit == 0
        )

        sum_b = sum(
            number
            for number, bit
            in zip(
                self.numbers,
                chromosome
            )
            if bit == 1
        )

        return abs(
            sum_a - sum_b
        )

    # Fitness максимізується
    def fitness_fn(self, individual):

        difference = self.difference(
            individual.chromosome
        )

        return (
            1.0 /
            (1.0 + difference)
        )

    # Двопунктове схрещування
    def crossover(self, p1, p2):

        i, j = sorted(
            random.sample(
                range(1, self.length),
                2
            )
        )

        c1 = (
            p1.chromosome[:i] +
            p2.chromosome[i:j] +
            p1.chromosome[j:]
        )

        c2 = (
            p2.chromosome[:i] +
            p1.chromosome[i:j] +
            p2.chromosome[j:]
        )

        return (
            Individual(c1),
            Individual(c2)
        )

    # Bit Flip mutation
    def mutate(
        self,
        individual,
        p_mut=None
    ):

        rate = (
            self.p_mut
            if p_mut is None
            else p_mut
        )

        individual.chromosome = [
            bit ^ 1
            if random.random() < rate
            else bit
            for bit in individual.chromosome
        ]

        individual.fitness = None

    def split(self, chromosome):

        group_a = [
            number
            for number, bit
            in zip(
                self.numbers,
                chromosome
            )
            if bit == 0
        ]

        group_b = [
            number
            for number, bit
            in zip(
                self.numbers,
                chromosome
            )
            if bit == 1
        ]

        return group_a, group_b


# Методичка не задає конкретні 20 елементів.
NUMBERS = [
    853, 746, 639, 582, 491,
    437, 386, 335, 294, 251,
    217, 183, 157, 131, 109,
    89, 73, 61, 47, 31
]


# ============================================================
# ЕКСПЕРИМЕНТИ
# ============================================================

def run_experiments():

    configs = [
        ("N=50 pc=0.8 pm=0.01 k=2",
         50, 0.8, 0.01, 2, 0, False),

        ("N=50 pc=0.8 pm=0.05 k=2",
         50, 0.8, 0.05, 2, 0, False),

        ("N=100 pc=0.8 pm=0.01 k=3",
         100, 0.8, 0.01, 3, 0, False),

        ("N=100 pc=0.9 pm=0.01 k=3",
         100, 0.9, 0.01, 3, 0, False),

        ("N=100 pc=0.8 pm=0.01 k=5",
         100, 0.8, 0.01, 5, 0, False),

        ("N=200 pc=0.8 pm=0.01 k=3",
         200, 0.8, 0.01, 3, 0, False),

        ("N=100 pc=0.8 pm=0.01 k=3 elite=5",
         100, 0.8, 0.01, 3, 5, False),

        ("N=100 pc=0.8 adaptive k=3",
         100, 0.8, 0.01, 3, 0, True)
    ]

    results = []
    histories = {}

    overall_best = None

    for (
        name,
        n,
        pc,
        pm,
        k,
        elite,
        adaptive
    ) in configs:

        fitnesses = []
        generations = []
        run_histories = []

        # 5 запусків кожної конфігурації
        for run in range(5):

            ga = PartitionGA(
                NUMBERS,
                pop_size=n,
                p_cross=pc,
                p_mut=pm,
                elite_size=elite,
                max_gen=200,
                tournament_k=k,
                adaptive=adaptive,
                seed=100 + run
            )

            best = ga.run()

            fitnesses.append(
                best.fitness
            )

            generations.append(
                ga.convergence_gen
            )

            run_histories.append(
                ga.history
            )

            if (
                overall_best is None
                or
                best.fitness >
                overall_best.fitness
            ):
                overall_best = (
                    copy.deepcopy(best)
                )

        # Середня крива збіжності
        histories[name] = [
            statistics.mean(values)
            for values
            in zip(*run_histories)
        ]

        results.append({
            "name": name,

            "best":
                max(fitnesses),

            "worst":
                min(fitnesses),

            "average":
                statistics.mean(
                    fitnesses
                ),

            "avg_generation":
                statistics.mean(
                    generations
                )
        })

    return (
        results,
        histories,
        overall_best
    )


# ============================================================
# ВИВЕДЕННЯ ТА ГРАФІК
# ============================================================

def print_results(results):

    print(
        "\nРезультати експериментів "
        "(5 запусків):"
    )

    print("-" * 105)

    print(
        f"{'Конфігурація':<42}"
        f"{'Best':>10}"
        f"{'Worst':>10}"
        f"{'Average':>12}"
        f"{'Avg gen':>12}"
    )

    print("-" * 105)

    for r in results:

        print(
            f"{r['name']:<42}"
            f"{r['best']:>10.4f}"
            f"{r['worst']:>10.4f}"
            f"{r['average']:>12.4f}"
            f"{r['avg_generation']:>12.2f}"
        )


def plot_convergence(histories):

    baseline = (
        "N=100 pc=0.8 "
        "pm=0.01 k=3"
    )

    adaptive = (
        "N=100 pc=0.8 "
        "adaptive k=3"
    )

    plt.plot(
        histories[baseline],
        label="Базовий GA"
    )

    plt.plot(
        histories[adaptive],
        label="Адаптивна мутація"
    )

    plt.xlabel("Покоління")
    plt.ylabel("Найкращий fitness")
    plt.title("Порівняння збіжності")

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ============================================================
# MAIN
# ============================================================

def main():

    # Перевірка базового ГА на OneMax
    one_max = OneMaxGA(
        length=50,
        pop_size=100,
        p_cross=0.8,
        p_mut=0.02,
        elite_size=2,
        max_gen=100,
        tournament_k=3,
        seed=42
    )

    one_best = one_max.run()

    print(
        "OneMax fitness:",
        one_best.fitness,
        "/ 50"
    )

    # Варіант 7
    results, histories, best = (
        run_experiments()
    )

    print_results(results)

    # Найкраще розбиття
    ga = PartitionGA(NUMBERS)

    group_a, group_b = ga.split(
        best.chromosome
    )

    print("\nНайкраще розбиття:")

    print(
        "A =",
        group_a,
        "sum =",
        sum(group_a)
    )

    print(
        "B =",
        group_b,
        "sum =",
        sum(group_b)
    )

    print(
        "Різниця =",
        abs(
            sum(group_a) -
            sum(group_b)
        )
    )

    print(
        "Fitness =",
        best.fitness
    )

    # Графік збіжності
    plot_convergence(histories)


if __name__ == "__main__":
    main()