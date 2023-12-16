import pygame
from .hexagon import Hexagon
from .constants import WIDTH,HEIGHT
import math


class Board():
    def __init__(self):
        self.hex_cells = []
        self.size = ((min(HEIGHT,WIDTH)*0.9)/math.cos(math.radians(30)))/22.5 # ok but need some corections
        self.center_of_first_hexagon_x = WIDTH / 2 - 15.5 * self.size
        self.center_of_first_hexagon_y = HEIGHT / 2 - 10 * self.size*math.cos(math.radians(30))# - self.size / math.cos(math.radians(30))
        # point1_x, point1_y = self.center_of_first_hexagon_x-3.35*self.size, self.center_of_first_hexagon_y-2*self.size/math.cos(math.radians(30))
        # full_lenght_of_board_y = point1_y + 22 * self.size * math.cos(math.radians(30)) - 2 * self.size + 4 * self.size / math.cos(math.radians(30))
        # point2_x, point2_y = point1_x + full_lenght_of_board_y * math.tan(math.radians(30)), point1_y + full_lenght_of_board_y
        # self.polygon_points = [(point1_x, point1_y), (point2_x, point2_y), (point2_x+24*self.size, point2_y), (point1_x+24*self.size, point1_y)]
        self.polygon_points = [(self.center_of_first_hexagon_x-4*self.size, 0), (self.center_of_first_hexagon_x+21.5*self.size, 0), (self.center_of_first_hexagon_x+21.5*self.size + HEIGHT*math.tan(math.radians(30)),HEIGHT), (self.center_of_first_hexagon_x-4*self.size + HEIGHT*math.tan(math.radians(30)),HEIGHT)]

    def draw_board(self, win):
        pygame.draw.polygon(win, (0, 0, 255), self.polygon_points, 0)
        self.polygon_points[-1], self.polygon_points[-2] = self.polygon_points[-2], self.polygon_points[-1]
        pygame.draw.polygon(win, (255, 255, 0), self.polygon_points, 0)
        for j in range(0, 11):
            center_y = self.center_of_first_hexagon_y + j * (self.size * 2) * math.cos(math.radians(30))
            iterable_list = []
            for i in range(0, 11):
                center_x = self.center_of_first_hexagon_x + (2 * i + j) * self.size
                basic_hex = Hexagon((center_x, center_y), self.size, (128, 128, 128))
                basic_hex.draw(win)
                basic_hex = Hexagon((center_x, center_y), self.size*0.85, (255, 255, 255))
                iterable_list.append(basic_hex)
                basic_hex.draw(win)

            self.hex_cells.append(iterable_list)


