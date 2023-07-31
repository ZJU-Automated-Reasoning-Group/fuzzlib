"""
Manging configurations of LLVM opt
"""
import random
import re
from collections import namedtuple, OrderedDict
from typing import List

"""An option"""
Param = namedtuple('Param', ['key', 'value', 'ttype'])


def random_bool(rand: random.Random) -> str:
    """Generate a random bool"""
    return "true" if rand.random() < 0.5 else "false"


def random_double(rand: random.Random) -> float:
    return rand.uniform(0.0, 100.0)


def random_uint(rand: random.Random) -> int:
    return rand.randint(0, 4294967295)


def mutate_param(param: Param, rand) -> Param:
    if "(bool)" == param.ttype:
        return param._replace(value=random_bool(rand))
    elif "(double)" == param.ttype:
        return param._replace(value=random_double(rand))
    elif "(unsigned int)" == param.ttype:
        return param._replace(value=random_uint(rand))
    elif "(string)" == param.ttype:
        return param
    else:
        raise LookupError("Unsupported param type: {0}".format(param.ttype))


class Params:
    """
    A group of parameters
    """
    _rex = re.compile(r"(.*)\s=\s(.*)\s(\(.*\))")
    _mutate_probability = 0.5
    _rand = random.Random()
    _rand.seed()

    def __init__(self):
        self._storage = OrderedDict()
        self.fitness = 0

    def add(self, param: Param):
        self._storage[param.key] = param
        return self

    def load(self, optlist: List[str]):
        """See opt_options of config.py for an example of optlist
            opt_options = [
                "dce = false (bool)",  # Dead Code Elimination
                "adce = false (bool)",  # Aggressive DCE
                "argpromotion = false (bool)",  # ArgumentPromotion
                "simplifycfg = false (bool)",  # CFGSimplification
            ]
        """
        for line in optlist:
            match = self._rex.match(line)
            self.add(Param(match.group(1), match.group(2), match.group(3)))
        return self

    def print(self):
        for param in self._storage.values():
            print("{0} = {1} {2}".format(param.key, param.value, param.ttype))
        # return self

    def mutate(self):
        """
        Mutate each Param in self._storages (this could be improved)
        """
        for key, param in self._storage.items():
            if self._rand.random() < self._mutate_probability:
                self._storage[key] = mutate_param(param, self._rand)
        return self

    @staticmethod
    def crossover(p1, p2):
        """
        For genetic algorithm
        """
        res = Params()
        crossover_point = p1._rand.randint(0, len(p1._storage) - 1)
        res._storage.update(list(p1._storage.items())[:crossover_point])
        res._storage.update(list(p2._storage.items())[crossover_point:])
        return res

    def to_llvm_opt_args(self):
        """
        :return: a cmd command
        """
        ret = []
        for param in self._storage.values():
            # print(param.ttype)
            if "(bool)" == param.ttype:
                if param.value == "true":
                    ret.append("--" + str(param.key))
        return ret

    def __cmp__(self, obj):
        if obj is None: return 1
        if not isinstance(obj, Params): return 1
        return self._storage.__cmp__(obj._storage)
