class Square:
    def __init__(self, n, m):
        try:
            self.coords = (int(n), int(m))
        except ValueError as e:
            raise e
        self.status = "empty"
        self.neighbor_list = []
        self.mined_neighbors = 0
        self.is_flagged = False

    def add_mine(self):
        self.status = "mine"
        for neighbor in self.neighbor_list:
            neighbor.mined_neighbors += 1

    def has_mine(self):
        return self.status == "mine"

    def is_discovered(self):
        return self.status == "discover"

    def discover(self):
        self.status = "discover"

    def flag(self):
        self.is_flagged = True

    def unflag(self):
        self.is_flagged = False

    def retrieve_good_neighbors(self):
        neighbors = self.neighbor_list[:]
        for neighbor in self.neighbor_list:
            if neighbor.is_flagged or neighbor.is_discovered():  # neighbor flagged or already discovered
                neighbors.remove(neighbor)
                continue
            if (neighbor not in neighbors) or (not neighbor.has_mine()):  # neighbor already removed or no mine
                continue
            if neighbor.has_mine():
                neighbors.remove(neighbor)
                if (neighbor.coords[0] == self.coords[0] - 1) or (neighbor.coords[0] == self.coords[0] + 1):
                    for n in neighbors:
                        if n.coords[0] == neighbor.coords[0]:
                            neighbors.remove(n)
                if (neighbor.coords[1] == self.coords[1] - 1) or (neighbor.coords[1] == self.coords[1] + 1):
                    for n in neighbors:
                        if n.coords[1] == neighbor.coords[1]:
                            neighbors.remove(n)
        return neighbors
