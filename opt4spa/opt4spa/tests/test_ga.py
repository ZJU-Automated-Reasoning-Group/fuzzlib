# coding: utf-8
import random

from . import TestCase, main
from ..config import opt_options
from ..gaopt import GA
from ..params import Params


def tmp_callback(para: Params):
    """
    Use the callback function to compute the fitness of current configuration
    NOTE: the callback should be able to accept an argument of type Param
    """
    return random.randint(1, 100000)
    # The line below is more realistic
    # ret = subprocess.call(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class TestGA(TestCase):
    """
    This class illustrate the use of GA
    """

    def test_ga(self):
        try:
            ga = GA(opt_options)
            for i in range(120):
                ga.evaluate(callback=tmp_callback)
                ga.repopulate()
            res = ga.retained()
            print(res)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()
