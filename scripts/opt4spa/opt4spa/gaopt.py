""" Genetic algorithm for optimizing LLVM opt parameters
"""
import random
from .params import Params


class GA:
    _population_size = 8
    _retain_percentage = 0.25
    _retain_size = int(_retain_percentage * _population_size) + 1

    _rand = random.Random()
    _rand.seed()

    def __init__(self, options):
        # for _ in range(self._population_size):
        self._population = [Params().load(options).mutate() for _ in range(self._population_size)]
        self._new = []
        self._retained = []

    def evaluate(self, callback):
        """
        Use the callback function to compute the fitness of current configuration
        NOTE: the callback should be able to accept an argument of type Param?
        """
        for param in self._population:
            param.fitness = callback(param)
            self._new.append(param)

    def retained(self):
        min_time = -1
        min_opt = ""
        for i, param in enumerate(self._retained):
            # print("Fitness: {0}\n".format(param.fitness))
            # param.print()
            min_time = param.fitness
            min_opt = " ".join(param.to_llvm_opt_args())
            break
        return min_time, min_opt

    def repopulate(self):
        self._new.extend(self._retained)
        self._new = list(set(self._new))
        self._new = sorted(self._new, key=lambda e: e.fitness)

        self._population = []
        self._retained = []

        self._retained.extend(self._new[:self._retain_size])

        while len(self._population) < self._population_size:
            i1 = self._rand.randint(0, len(self._new) - 1)
            i2 = self._rand.randint(0, len(self._new) - 1)
            if i1 == i2: continue
            if self._new[i1].fitness == 4294967295 or self._new[i2].fitness == 4294967295: continue
            self._population.append(
                Params.crossover(
                    self._new[i1],
                    self._new[i2]
                ).mutate()
            )
        self._new = []
