# coding: utf-8

from . import TestCase, main

from ..config import opt_options
from ..params import Params


class TestParams(TestCase):

    def test_mutate(self):
        para = Params()
        para.load(opt_options)

        for key, param in para._storage.items():
            if "(bool)" == param.ttype:
                para._storage[key] = param._replace(value="true")

        print("XXXXXXXXXXXXX")
        print(" ".join(para.to_llvm_opt_args()))
        print("XXXXXXXXXXXXX")


if __name__ == '__main__':
    main()
