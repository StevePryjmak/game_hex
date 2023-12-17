
class Graph:
    def __init__(self, board, color):
        self.board = [
            [1 if cell.occupated_by == 'Yellow' else 2 if cell.occupated_by == 'Blue' else 0 for cell in row]
            for row in board
        ]
        self.color = color
        self.winner = False
        if color == 1:
            self.check_positions = [(0, j) for j in range(11)]
            self.end_positions = [(10, j) for j in range(11)]
        elif color == 2:
            self.check_positions = [(i, 0) for i in range(11)]
            self.end_positions = [(i, 10) for i in range(11)]

        if self.is_winner(self.check_positions):
            self.winner, path = True, [self.is_winner(self.check_positions)[1]]
            print(path)
            self.wining_cluster = self.is_winner(path, True)

            print(f'Winner found {self.color}')

    def get_neighbors(self, i, j, color, visited):
        neighbors = []
        potential_neighbors = [(i, j + 1), (i, j - 1), (i + 1, j - 1), (i + 1, j), (i - 1, j), (i - 1, j + 1)]

        for n, m in potential_neighbors:
            if 0 <= n <= 10 and 0 <= m <= 10 and self.board[n][m] == color and (n, m) not in visited:
                neighbors.append((n, m))
                if (n, m) in self.end_positions:
                    return True, neighbors, (n, m)

        return False, neighbors, None

    def is_winner(self, check_positions, move_through_all=False):
        visited = []
        while check_positions:
            depth_checking_positions = []

            for i, j in check_positions:
                if self.board[i][j] != self.color:
                    continue
                visited.append((i, j))
                end, neighbors, path = self.get_neighbors(i, j, self.color, visited)
                depth_checking_positions.extend(neighbors)

                if end and not move_through_all:
                    return True, path

            check_positions = depth_checking_positions
        if move_through_all:
            return visited


def example():
    array = [[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    graph = Graph(array, 1)
    print(graph.get_neighbors(0, 1, 1, [(0, 2)]))


if __name__ == '__main__':
    example()
