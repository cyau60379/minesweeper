import random
from .Square import Square


class Grid:
    def __init__(self):
        self.mine_grid = []
        self.shown_grid = []
        self.size = 0

    def init_size(self, size, mines):
        try:
            int_size = int(size)
            int_mines = int(mines)
        except ValueError as e:
            raise e
        self.size = int_size
        for i in range(int_size):
            self.mine_grid.append([] * int_size)
            self.shown_grid.append([-1] * int_size)
            for j in range(int_size):
                self.mine_grid[i].append(Square(i, j))
                if i > 0:
                    self.mine_grid[i][j].neighbor_list.append(self.mine_grid[i - 1][j])
                    self.mine_grid[i - 1][j].neighbor_list.append(self.mine_grid[i][j])
                    if j < int_size - 1:
                        self.mine_grid[i][j].neighbor_list.append(self.mine_grid[i - 1][j + 1])
                        self.mine_grid[i - 1][j + 1].neighbor_list.append(self.mine_grid[i][j])
                    if j > 0:
                        self.mine_grid[i][j].neighbor_list.append(self.mine_grid[i - 1][j - 1])
                        self.mine_grid[i - 1][j - 1].neighbor_list.append(self.mine_grid[i][j])
                if j > 0:
                    self.mine_grid[i][j].neighbor_list.append(self.mine_grid[i][j - 1])
                    self.mine_grid[i][j - 1].neighbor_list.append(self.mine_grid[i][j])
        self.fill(int_size, int_mines)

    def fill(self, size, mines):
        try:
            numbers = random.sample(range(0, size * size), mines)
            columns = [n % size for n in numbers]
            lines = [int((numbers[i] - columns[i]) / size) for i in range(len(numbers))]
            for i in range(mines):
                self.mine_grid[lines[i]][columns[i]].add_mine()
        except ValueError as e:
            raise e

    def show_square(self, square):
        if square.has_mine():
            self.show_all_grid()
            return False
        else:
            self.discover_squares(square)
            return True

    def discover_squares(self, square):
        queue = [square]
        while queue:
            self.discover_square(queue)

    def discover_square(self, queue):
        square = queue.pop(0)
        self.shown_grid[square.coords[0]][square.coords[1]] = square.mined_neighbors
        queue += square.retrieve_good_neighbors()

    def show_all_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.mine_grid[i][j].has_mine():
                    self.shown_grid[i][j] = -2
                else:
                    self.shown_grid[i][j] = self.mine_grid[i][j].mined_neighbors
