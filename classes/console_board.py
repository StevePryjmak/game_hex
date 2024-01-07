

class ConsoleBoard:
    def __init__(self):
        self.cells = [[0 for row in range(11)] for column in range(11)]

    def display_bord(self):
        offset = ''
        for row in self.cells:
            print(f'{offset}', end='')
            for element in row:
                print(f'{element} ', end='')
            offset += ' '
            print()


