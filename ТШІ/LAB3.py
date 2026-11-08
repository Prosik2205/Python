import random
import math
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
        max_gen=300,
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
        group = random.sample(population, self.k)
        return max(group, key=lambda x: x.fitness)

    # Однопунктове схрещування для базового ГА
    def one_point_crossover(self, p1, p2):
        point = random.randint(1, len(p1.chromosome) - 1)

        c1 = p1.chromosome[:point] + p2.chromosome[point:]
        c2 = p2.chromosome[:point] + p1.chromosome[point:]

        return Individual(c1), Individual(c2)

    # Адаптивна ймовірність мутації
    def adaptive_rate(self, population):
        values = [x.fitness for x in population]

        diversity = (
            statistics.pstdev(values)
            if len(values) > 1
            else 0
        )

        if diversity < 0.01:
            return 0.10

        return 0.01 + 0.09 * min(
            0.01 / diversity,
            1.0
        )

    def run(self):
        if self.seed is not None:
            random.seed(self.seed)

        population = [
            self.create_individual()
            for _ in range(self.pop_size)
        ]

        self.evaluate(population)

        best = copy.deepcopy(
            max(population, key=lambda x: x.fitness)
        )

        best_gen = 0
        self.history = []

        for gen in range(self.max_gen):

            current = max(
                population,
                key=lambda x: x.fitness
            )

            if current.fitness > best.fitness:
                best = copy.deepcopy(current)
                best_gen = gen

            # Найкращий fitness, знайдений до цього покоління
            self.history.append(best.fitness)

            # Елітизм
            elite = sorted(
                population,
                key=lambda x: x.fitness,
                reverse=True
            )[:self.elite_size]

            elite = [
                copy.deepcopy(x)
                for x in elite
            ]

            # Фіксована або адаптивна мутація
            rate = (
                self.adaptive_rate(population)
                if self.adaptive
                else self.p_mut
            )

            children = []

            needed = (
                self.pop_size -
                self.elite_size
            )

            while len(children) < needed:

                p1 = self.tournament_select(population)
                p2 = self.tournament_select(population)

                if random.random() < self.p_cross:
                    c1, c2 = self.crossover(p1, p2)
                else:
                    c1 = copy.deepcopy(p1)
                    c2 = copy.deepcopy(p2)

                self.mutate(c1, rate)
                self.mutate(c2, rate)

                children.extend([c1, c2])

            population = (
                elite +
                children[:needed]
            )

            self.evaluate(population)

        self.convergence_gen = best_gen

        return best


# ============================================================
# ONEMAX — ПЕРЕВІРКА БАЗОВОГО ГА
# ============================================================

class OneMaxGA(GeneticAlgorithm):
    def __init__(self, length=50, **kwargs):
        super().__init__(**kwargs)
        self.length = length

    def create_individual(self):
        return Individual([
            random.randint(0, 1)
            for _ in range(self.length)
        ])

    def fitness_fn(self, ind):
        return sum(ind.chromosome)

    def crossover(self, p1, p2):
        return self.one_point_crossover(p1, p2)

    def mutate(self, ind, p_mut=None):
        rate = (
            self.p_mut
            if p_mut is None
            else p_mut
        )

        ind.chromosome = [
            bit ^ 1
            if random.random() < rate
            else bit
            for bit in ind.chromosome
        ]

        ind.fitness = None


# ============================================================
# ВАРІАНТ 8 — XOR
# ============================================================

class XORGA(GeneticAlgorithm):

    def __init__(
        self,
        weight_min=-5.0,
        weight_max=5.0,
        sigma=0.5,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.weight_min = weight_min
        self.weight_max = weight_max
        self.sigma = sigma

        # XOR dataset
        self.data = [
            (0, 0, 0),
            (0, 1, 1),
            (1, 0, 1),
            (1, 1, 0)
        ]

    # 9 параметрів мережі 2-2-1
    def create_individual(self):
        chromosome = [
            random.uniform(
                self.weight_min,
                self.weight_max
            )
            for _ in range(9)
        ]

        return Individual(chromosome)

    def sigmoid(self, x):
        # захист від переповнення exp()
        x = max(-60, min(60, x))

        return 1.0 / (
            1.0 + math.exp(-x)
        )

    # Пряме поширення сигналу
    def predict(self, chromosome, x1, x2):

        (
            w1, w2, b1,
            w3, w4, b2,
            w5, w6, b3
        ) = chromosome

        h1 = self.sigmoid(
            x1 * w1 +
            x2 * w2 +
            b1
        )

        h2 = self.sigmoid(
            x1 * w3 +
            x2 * w4 +
            b2
        )

        output = self.sigmoid(
            h1 * w5 +
            h2 * w6 +
            b3
        )

        return output

    # Середньоквадратична помилка
    def mse(self, chromosome):
        error = 0.0

        for x1, x2, target in self.data:

            output = self.predict(
                chromosome,
                x1,
                x2
            )

            error += (
                target - output
            ) ** 2

        return error / len(self.data)

    # Максимізуємо fitness
    def fitness_fn(self, ind):

        error = self.mse(
            ind.chromosome
        )

        return 1.0 / (
            1.0 + error
        )

    # Рівномірне схрещування
    def crossover(self, p1, p2):

        c1 = []
        c2 = []

        for g1, g2 in zip(
            p1.chromosome,
            p2.chromosome
        ):

            if random.random() < 0.5:
                c1.append(g1)
                c2.append(g2)
            else:
                c1.append(g2)
                c2.append(g1)

        return (
            Individual(c1),
            Individual(c2)
        )

    # Гаусова мутація
    def mutate(self, ind, p_mut=None):

        rate = (
            self.p_mut
            if p_mut is None
            else p_mut
        )

        chromosome = []

        for gene in ind.chromosome:

            if random.random() < rate:
                gene += random.gauss(
                    0,
                    self.sigma
                )

            gene = max(
                self.weight_min,
                min(
                    self.weight_max,
                    gene
                )
            )

            chromosome.append(gene)

        ind.chromosome = chromosome
        ind.fitness = None

    def accuracy(self, chromosome):

        correct = 0

        for x1, x2, target in self.data:

            output = self.predict(
                chromosome,
                x1,
                x2
            )

            predicted = (
                1 if output >= 0.5
                else 0
            )

            if predicted == target:
                correct += 1

        return correct / len(self.data)


# ============================================================
# СЕРІЯ ЕКСПЕРИМЕНТІВ
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
        accuracies = []
        run_histories = []

        for run in range(5):

            ga = XORGA(
                pop_size=n,
                p_cross=pc,
                p_mut=pm,
                elite_size=elite,
                max_gen=300,
                tournament_k=k,
                adaptive=adaptive,
                sigma=0.5,
                seed=100 + run
            )

            best = ga.run()

            fitnesses.append(
                best.fitness
            )

            generations.append(
                ga.convergence_gen
            )

            accuracies.append(
                ga.accuracy(
                    best.chromosome
                )
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
                overall_best = copy.deepcopy(
                    best
                )

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
                statistics.mean(fitnesses),

            "accuracy":
                statistics.mean(
                    accuracies
                ),

            "avg_generation":
                statistics.mean(
                    generations
                )
        })

    return results, histories, overall_best


# ============================================================
# ВИВЕДЕННЯ РЕЗУЛЬТАТІВ
# ============================================================

def print_results(results):

    print(
        "\nРезультати експериментів "
        "(5 запусків):"
    )

    print("-" * 120)

    print(
        f"{'Конфігурація':<42}"
        f"{'Best':>10}"
        f"{'Worst':>10}"
        f"{'Average':>12}"
        f"{'Accuracy':>12}"
        f"{'Avg gen':>12}"
    )

    print("-" * 120)

    for r in results:

        print(
            f"{r['name']:<42}"
            f"{r['best']:>10.4f}"
            f"{r['worst']:>10.4f}"
            f"{r['average']:>12.4f}"
            f"{r['accuracy'] * 100:>11.1f}%"
            f"{r['avg_generation']:>12.2f}"
        )


# ============================================================
# ГРАФІК ЗБІЖНОСТІ
# ============================================================

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
    plt.grid()
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

    # Варіант 8
    results, histories, best = (
        run_experiments()
    )

    print_results(results)

    ga = XORGA()

    print("\nНайкращі ваги:")

    for i, weight in enumerate(
        best.chromosome,
        start=1
    ):
        print(
            f"w{i} = {weight:.4f}"
        )

    print("\nРезультат XOR:")

    for x1, x2, target in ga.data:

        output = ga.predict(
            best.chromosome,
            x1,
            x2
        )

        predicted = (
            1 if output >= 0.5
            else 0
        )

        print(
            f"{x1} XOR {x2} "
            f"= {predicted} "
            f"(output={output:.4f}, "
            f"target={target})"
        )

    print(
        "\nMSE =",
        ga.mse(best.chromosome)
    )

    print(
        "Fitness =",
        best.fitness
    )

    print(
        "Accuracy =",
        f"{ga.accuracy(best.chromosome) * 100:.1f}%"
    )

    plot_convergence(histories)


if __name__ == "__main__":
    main()