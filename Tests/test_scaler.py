from unittest import TestCase

import numpy as np

from nssPCA.preprocessing import Scaler


class TestScaler(TestCase):
    def test_transform_vec_plain(self):
        """
        Test vectors with random size and values with no transformation.
        """
        for i in range(100):
            size = int(99 * np.random.random() + 1)
            vector = np.full((1, size), np.random.random())  # "horizontal" vector
            self.assertEqual(Scaler(False, False).transform(vector).tolist(), vector.tolist())
            self.assertEqual(Scaler(False, False, axis=1).transform(vector).tolist(), vector.tolist())

            vector = np.full((size, 1), np.random.random())  # "vertical" vector
            self.assertEqual(Scaler(False, False).transform(vector).tolist(), vector.tolist())
            self.assertEqual(Scaler(False, False, axis=1).transform(vector).tolist(), vector.tolist())

    def test_transform_matrix_plain(self):
        """
        Test matrix with random size and values with no transformation.
        """
        for i in range(100):
            size_x = int(99 * np.random.random() + 1)
            size_y = int(99 * np.random.random() + 1)
            matrix = np.full((size_x, size_y), np.random.random())
            self.assertEqual(Scaler(False, False).transform(matrix).tolist(), matrix.tolist())
            self.assertEqual(Scaler(False, False, axis=1).transform(matrix).tolist(), matrix.tolist())

    def test_transform_vec_mean(self):
        """
        Test vectors with mean centering.
        """

        # 1x5 vector of zeros
        self.assertEqual(Scaler(calc_std=False, calc_mean=True).transform(np.zeros((1, 5))).tolist(),
                         np.zeros((1, 5)).tolist())
        self.assertEqual(Scaler(calc_std=False, calc_mean=True, axis=1).transform(np.zeros((1, 5))).tolist(),
                         np.zeros((1, 5)).tolist())

        # 5x1 vector of zeros
        self.assertEqual(Scaler(calc_std=False, calc_mean=True).transform(np.zeros((5, 1))).tolist(),
                         np.zeros((5, 1)).tolist())
        self.assertEqual(Scaler(calc_std=False, calc_mean=True, axis=1).transform(np.zeros((5, 1))).tolist(),
                         np.zeros((5, 1)).tolist())

        # 1x5 vector of ones
        self.assertEqual(Scaler(calc_std=False, calc_mean=True).transform(np.ones((1, 5))).tolist(),
                         np.zeros((1, 5)).tolist())
        self.assertEqual(Scaler(calc_std=False, calc_mean=True, axis=1).transform(np.ones((1, 5))).tolist(),
                         np.zeros((1, 5)).tolist())

        # 5x1 vector of ones
        self.assertEqual(Scaler(calc_std=False, calc_mean=True).transform(np.ones((5, 1))).tolist(),
                         np.zeros((5, 1)).tolist())
        self.assertEqual(Scaler(calc_std=False, calc_mean=True, axis=1).transform(np.ones((5, 1))).tolist(),
                         np.zeros((5, 1)).tolist())

        self.assertAlmostEqual(
            Scaler(calc_std=False, calc_mean=True).transform(np.array([[0, 5, 10]])).tolist(), [[0, 0, 0]])

        self.assertAlmostEqual(
            Scaler(calc_std=False, calc_mean=True, axis=1).transform(np.array([[0, 5, 10]])).tolist(),
            [[-5, 0, 5]])

        # self.assertAlmostEqual(
        #     Scaler(calc_std=False, calc_mean=True, axis=1).transform(np.array([[0], [5], [10]])).tolist(),
        #     [[-5], [0], [5]])
