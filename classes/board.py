import pygame
from classes.hexagon import Hexagon
from classes.constants import WIDTH, HEIGHT
import math
from itertools import product


class Board:
    def __init__(self):
        self.hex_cells = []
        self.size = ((min(HEIGHT, WIDTH) * 0.9) / math.cos(math.radians(30))) / 22.5
        self.first_hex_center_x, self.first_hex_center_y = self.calculate_first_hexagon_center()
        self.polygon_points = self.calculate_polygon_points()

    def calculate_first_hexagon_center(self):
        center_x = WIDTH / 2 - 15.5 * self.size
        center_y = HEIGHT / 2 - 10 * self.size * math.cos(math.radians(30))
        return center_x, center_y

    def calculate_polygon_points(self):

        point1_x, point1_y = self.first_hex_center_x - 4 * self.size, 0
        point2_x, point2_y = self.first_hex_center_x + 21.5*self.size, 0
        offset = HEIGHT*math.tan(math.radians(30))

        polygon_points = [
            (point1_x, point1_y),
            (point2_x, point2_y),
            (point2_x + offset, HEIGHT),
            (point1_x + offset, HEIGHT),
        ]
        return polygon_points

    def draw_board(self, win):
        pygame.draw.polygon(win, (0, 0, 255), self.polygon_points, 0)
        self.polygon_points[-1], self.polygon_points[-2] = self.polygon_points[-2], self.polygon_points[-1]
        pygame.draw.polygon(win, (255, 255, 0), self.polygon_points, 0)

        for j in range(0, 11):
            center_y = self.first_hex_center_y + j * (self.size * 2) * math.cos(math.radians(30))
            iterable_list = []
            for i in range(0, 11):
                center_x = self.first_hex_center_x + (2 * i + j) * self.size
                basic_hex = Hexagon((center_x, center_y), self.size, (128, 128, 128))
                basic_hex.draw(win)
                basic_hex = Hexagon((center_x, center_y), self.size*0.85, (255, 255, 255))
                iterable_list.append(basic_hex)
                basic_hex.draw(win)

            self.hex_cells.append(iterable_list)

    def get_hex_cords(self, position):
        for row_index in range(0, 11):
            hex_cell = self.hex_cells[row_index][0]

            if abs(position[1] - hex_cell.center[1]) <= hex_cell.radius_of_circle:
                possible_rows = ([row_index + 1] if row_index + 1 < 11 else []) + [row_index]
                column_distance = (position[0] - (hex_cell.center[0] - hex_cell.height)) / (2 * self.size)

                if column_distance < 0 or column_distance > 11:
                    return -1, False
                possible_columns = (
                                       [int(column_distance) - 1] if 0 <= int(column_distance) - 1 <= 10 else []
                                   ) + [int(column_distance)] if 0 <= int(column_distance) <= 10 else []

                for i, j in product(possible_rows, possible_columns):
                    if self.hex_cells[i][j].clicked(position):
                        return i, j
                return -1, False
        return -1, False
