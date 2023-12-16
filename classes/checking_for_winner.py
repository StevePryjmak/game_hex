
class Graph:
    def __init__(self,array,color):
        self.array = [[1 if array[i][j].occupated_by == 'Green' else 2 if array[i][j].occupated_by == 'Blue' else 0 for j in range(11)] for i in range(11)]
        #self.array = array
        #print(self.array)
        #print(self.array[0][1])
        self.neighbors = []
        self.check_list = []
        self.color = color
        self.already_checked = []
        for j in range(0,11):
            self.check_list.append((0,j))
        self.end_list = []
        for j in range(0,11):
            self.end_list.append((10,j))

        if self.is_winner(self.check_list):
            print('Winner finded')


        pass

    def get_neighbors(self, i, j, color, already_checked):
        neighbors = []
        potential_neighbors = [(i, j+1), (i, j-1), (i+1,j-1), (i+1, j), (i-1,j),(i-1,j+1)]
        for n,m in potential_neighbors:
            if n < 0 or m < 0 or m > 10 or n > 10:
                continue
            if (self.array[n][m] == color
                and ((n, m) not in already_checked)):
                neighbors.append((n,m))
                if (n, m) in self.end_list:
                    return True,neighbors

        return False, neighbors

    def is_winner(self,check_list):

        already_checked = []
        while check_list:

            depth_checking_list = []
            for i, j in check_list:
                already_checked.append((i, j))
                end, neighbors = self.get_neighbors(i, j, self.color, already_checked)
                depth_checking_list = depth_checking_list + neighbors
                if end:
                    return True
            check_list = depth_checking_list


def exemple():
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
    graph = Graph(array)
    print(graph.get_neighbors(0,1,1,[(0,2)]))


if __name__ == '__main__':
    exemple()