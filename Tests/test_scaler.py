from unittest import TestCase

import numpy as np

from nssPCA.preprocessing import Scaler


class TestScaler(TestCase):
    def test_transform_size_plain(self):
        """
        Test vectors and matrix with random size and values for size.
        """
        for i in range(100):
            size_x = int(99 * np.random.random() + 1)
            size_y = int(99 * np.random.random() + 1)
            dim = round(np.random.random())
            matrix = np.full((size_x, size_y), np.random.random())
            transformed = Scaler(False, False, inplace=False, axis=dim).transform(matrix)
            self.assertEqual(matrix.size, transformed.size)

    def test_transform_size_mean(self):
        """
        Test vectors and matrix with random size and values for size.
        """
        for i in range(100):
            size_x = int(99 * np.random.random() + 1)
            size_y = int(99 * np.random.random() + 1)
            dim = round(np.random.random())
            matrix = np.full((size_x, size_y), np.random.random())
            transformed = Scaler(False, True, inplace=False, axis=dim).transform(matrix)
            self.assertEqual(matrix.size, transformed.size)

    def test_transform_size_std(self):
        """
        Test vectors and matrix with random size and values for size.
        """
        for i in range(100):
            size_x = int(99 * np.random.random() + 1)
            size_y = int(99 * np.random.random() + 1)
            dim = round(np.random.random())
            matrix = np.full((size_x, size_y), np.random.random())
            transformed = Scaler(True, False, inplace=False, axis=dim).transform(matrix)
            self.assertEqual(matrix.size, transformed.size)

    def test_transform_size_mean_std(self):
        """
        Test vectors and matrix with random size and values for size.
        """
        for i in range(100):
            size_x = int(99 * np.random.random() + 1)
            size_y = int(99 * np.random.random() + 1)
            dim = round(np.random.random())
            matrix = np.full((size_x, size_y), np.random.random())
            transformed = Scaler(True, True, inplace=False, axis=dim).transform(matrix)
            self.assertEqual(matrix.size, transformed.size)

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

        input = Scaler(calc_std=False, calc_mean=True, axis=1).transform(np.array([[0], [5], [10]]))
        result = [[0], [0], [0]]
        for i in range(input.shape[0]):
            for j in range(input.shape[1]):
                self.assertAlmostEqual(input[i, j], result[i][j])

        self.assertAlmostEqual(
            Scaler(calc_std=False, calc_mean=True, axis=1).transform(np.array([[1, 0, 3.5]])).tolist(),
            [[-.5, -1.5, 2]])

        self.assertAlmostEqual(Scaler(calc_std=False, calc_mean=True).transform(np.array([[1, 0, 3.5]])).tolist(),
                               [[0, 0, 0]])

        input = Scaler(calc_std=False, calc_mean=True, axis=1).transform(np.array([[1], [0], [3.5]]))
        result = [[0], [0], [0]]
        for i in range(input.shape[0]):
            for j in range(input.shape[1]):
                self.assertAlmostEqual(input[i, j], result[i][j])

        input = Scaler(calc_std=False, calc_mean=True, axis=0).transform(np.array([[1], [0], [3.5]]))
        result = [[-.5], [-1.5], [2]]
        for i in range(input.shape[0]):
            for j in range(input.shape[1]):
                self.assertAlmostEqual(input[i, j], result[i][j])

    def test_transform_matrix_mean(self):
        """
        Test matrix with mean centering.
        """
        matrix = np.array([[21, 6, 9, 0],
                           [9, 4, 1, 2],
                           [6, 5, 8, 1]], dtype=np.float64)

        input = Scaler(calc_mean=True, calc_std=False, axis=0).transform(matrix)

        result = np.array([[9., 1., 3., -1.],
                           [-3., -1., -5., 1.],
                           [-6., 0., 2., 0.]])

        for i in range(input.shape[0]):
            for j in range(input.shape[1]):
                self.assertAlmostEqual(input[i, j], result[i][j])

        input = Scaler(calc_mean=True, calc_std=False, axis=1).transform(matrix)

        result = np.array([[12., -3., 0., -9.],
                           [5., 0., -3., -2.],
                           [1., 0., 3., -4.]])

        for i in range(input.shape[0]):
            for j in range(input.shape[1]):
                self.assertAlmostEqual(input[i, j], result[i][j])

        matrix = np.array([[0.5, -0.9, 0.12],
                           [7.1, 9.5, 2],
                           [2.36, 1, 1]], dtype=np.float64)

        input = Scaler(calc_mean=True, calc_std=False, axis=0).transform(matrix)

        result = np.array([[-2.82, -4.1, -.92],
                           [3.78, 6.3, 0.96],
                           [-0.96, -2.2, -0.04]])

        for i in range(input.shape[0]):
            for j in range(input.shape[1]):
                self.assertAlmostEqual(input[i, j], result[i][j])

        input = Scaler(calc_mean=True, calc_std=False, axis=1).transform(matrix).round(4)

        result = np.array([[0.5933, -.8067, .2133],
                           [0.9, 3.3, -4.2],
                           [0.9067, -.4533, -.4533]])

        for i in range(input.shape[0]):
            for j in range(input.shape[1]):
                self.assertAlmostEqual(input[i, j], result[i][j])

    # TODO: tests with calc_std=True
