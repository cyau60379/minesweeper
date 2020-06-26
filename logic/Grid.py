import random
from .Square import Square


class Grid:
    def __init__(self):
        self.mine_grid = []
        self.shown_grid = []
        self.size = 0
        self.mines = 0
        self.flagged_square = 0

    def init_size(self, size, mines):
        try:
            int_size = int(size)
            int_mines = int(mines)
        except ValueError as e:
            raise e
        self.size = int_size
        self.mines = int_mines
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
            return False, []
        else:
            discovered = self.discover_squares(square)
            return True, discovered

    def discover_squares(self, square):
        queue = [square]
        deja_vu = set()
        while queue:
            self.discover_square(queue, deja_vu)
        return list(deja_vu)

    def discover_square(self, queue, deja_vu):
        square = queue.pop(0)
        if square not in deja_vu or not square.is_discovered() or not square.is_flagged:
            deja_vu.add(square)
            self.shown_grid[square.coords[0]][square.coords[1]] = square.mined_neighbors
            self.mine_grid[square.coords[0]][square.coords[1]].discover()
            if square.mined_neighbors == 0:
                queue += square.retrieve_good_neighbors()

    def show_all_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.mine_grid[i][j].has_mine():
                    self.shown_grid[i][j] = -2
                else:
                    self.shown_grid[i][j] = self.mine_grid[i][j].mined_neighbors

    def put_flag_on_square(self, square):
        if self.flagged_square >= self.mines:
            return False
        else:
            square.flag()
            self.flagged_square += 1
            return True

    def remove_flag_on_square(self, square):
        if self.flagged_square <= 0:
            return False
        else:
            square.unflag()
            self.flagged_square -= 1
            return True

    def end_game(self):
        new_grid = []
        for i in range(self.size):
            new_grid.append([])
            for j in range(self.size):
                if self.mine_grid[i][j].has_mine():
                    new_grid[i].append(-1)
                else:
                    new_grid[i].append(self.mine_grid[i][j].mined_neighbors)
        if new_grid == self.shown_grid:
            return True
        return False
