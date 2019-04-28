from unittest import TestCase

import numpy as np

from nssPCA.decomposition.Eigen import check_symmetric
from nssPCA.preprocessing import Squarer


class TestSquarer(TestCase):
    def test_transfrom_symetric(self):
        for _ in range(100):
            size_x = int(99 * np.random.random() + 1)
            size_y = int(99 * np.random.random() + 1)
            dim = np.random.randint(0, 1)
            matrix = np.full((size_x, size_y), np.random.random())
            square = Squarer(axis=dim).transform(matrix)

            self.assertTrue(check_symmetric(square))

# TODO: check values
