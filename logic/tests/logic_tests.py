import unittest
from logic.Square import Square
from logic.Grid import Grid


class LogicTests(unittest.TestCase):
    def test_square_init_wrong_value(self):
        with self.assertRaises(ValueError) as context:
            Square("re", "ze")
            self.assertTrue(context.exception)

    def test_square_init(self):
        square = Square(10, 10)
        self.aux(square)

    def test_square_init_float(self):
        square = Square(10.1254, 10.45615)
        self.aux(square)

    def test_square_init_string(self):
        square = Square("10", "10")
        self.aux(square)

    def aux(self, square):
        test_list = [(square.coords, (10, 10)),
                     (square.status, "empty"),
                     (square.neighbor_list, []),
                     (square.mined_neighbors, 0)]
        for square_element, expected_value in test_list:
            with self.subTest():
                self.assertEqual(square_element, expected_value)

    def test_add_mine(self):
        square = Square("100", "100")
        square2 = Square("200", "100")
        square.neighbor_list.append(square2)
        square2.neighbor_list.append(square)
        square.add_mine()
        test_list = [(square.coords, (100, 100)),
                     (square.status, "mine"),
                     (square.neighbor_list, [square2]),
                     (square.mined_neighbors, 0),
                     (square.has_mine(), True),
                     (square2.has_mine(), False),
                     (square2.mined_neighbors, 1)]
        for square_element, expected_value in test_list:
            with self.subTest():
                self.assertEqual(square_element, expected_value)

    def test_init_grid(self):
        grid = Grid()
        test_list = [(grid.mine_grid, []),
                     (grid.shown_grid, []),
                     (grid.size, 0)]
        for square_element, expected_value in test_list:
            with self.subTest():
                self.assertEqual(square_element, expected_value)

    def test_init_size_wrong_value(self):
        grid = Grid()
        with self.assertRaises(ValueError) as context:
            grid.init_size("dzdze", "feseff")
            self.assertTrue(context.exception)

    def test_init_size(self):
        grid = Grid()
        grid.init_size(3, 5)
        self.aux_size(grid, 3)

    def test_init_size2(self):
        grid = Grid()
        grid.init_size(3, 5)
        self.aux_size2(grid, 3, 5)

    def test_init_size_float(self):
        grid = Grid()
        grid.init_size(3.0, 5)
        self.aux_size(grid, 3)

    def test_init_size2_float(self):
        grid = Grid()
        grid.init_size(3, 5.0)
        self.aux_size2(grid, 3, 5)

    def test_init_size_string(self):
        grid = Grid()
        grid.init_size("3", 5)
        self.aux_size(grid, 3)

    def test_init_size2_string(self):
        grid = Grid()
        grid.init_size(3, "5")
        self.aux_size2(grid, 3, 5)

    def aux_size(self, grid, size):
        slst = []
        for i in range(size):
            slst.append([-1] * size)
        test_list = [(grid.shown_grid, slst),
                     (grid.size, 3)]
        for square_element, expected_value in test_list:
            with self.subTest():
                self.assertEqual(square_element, expected_value)

    def aux_size2(self, grid, size, mine):
        mine_number = 0
        for i in range(size):
            for j in range(size):
                if grid.mine_grid[i][j].has_mine():
                    mine_number += 1
        self.assertEqual(mine_number, mine)

    def test_show_square(self):
        grid = Grid()
        grid.init_size(3, 5)
        is_ok = False
        square = Square(0, 0)
        for i in range(grid.size):
            if is_ok:
                break
            for j in range(grid.size):
                if grid.mine_grid[i][j].has_mine():
                    square = grid.mine_grid[i][j]
                    is_ok = True
                    break
        result = grid.show_square(square)
        self.assertEqual(result, False)

    def test_show_square2(self):
        grid = Grid()
        grid.init_size(3, 5)
        is_ok = False
        square = Square(0, 0)
        for i in range(grid.size):
            if is_ok:
                break
            for j in range(grid.size):
                if not grid.mine_grid[i][j].has_mine():
                    square = grid.mine_grid[i][j]
                    is_ok = True
                    break
        result = grid.show_square(square)
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
