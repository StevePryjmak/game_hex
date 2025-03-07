import pygame
from classes.gui.hexagon import Hexagon
from classes.gui.constants import WIDTH, HEIGHT, FIRST_PLAYER_COLOR, SECOND_PLAYER_COLOR
import math
from itertools import product


class GuiBoard:
    def __init__(self, win):
        self.win = win
        self.hex_cells = []
        self.shadow_hex = []
        self.size = ((min(HEIGHT, WIDTH) * 0.9) / math.cos(math.radians(30))) / 22.5
        self.first_hex_center_x, self.first_hex_center_y = self.calculate_first_hexagon_center()
        self.polygon_points = self.calculate_polygon_points()
        self.create_hex_cells()
        self.coordinates = False

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

    def create_hex_cells(self):
        for j in range(0, 11):
            center_y = self.first_hex_center_y + j * (self.size * 2) * math.cos(math.radians(30))
            iterable_list_hexes = []
            iterable_list_shadow_hexes = []
            for i in range(0, 11):
                center_x = self.first_hex_center_x + (2 * i + j) * self.size
                basic_hex = Hexagon((center_x, center_y), self.size, (128, 128, 128))
                iterable_list_shadow_hexes.append(basic_hex)
                basic_hex = Hexagon((center_x, center_y), self.size*0.95, (255, 255, 255))
                iterable_list_hexes.append(basic_hex)

            self.hex_cells.append(iterable_list_hexes)
            self.shadow_hex.append(iterable_list_shadow_hexes)

    def draw_board(self, win):
        win.fill((0, 0, 0))
        bg_image = pygame.image.load("images/background_img3.jpg")
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
        win.blit(bg_image, (0, 0))
        pygame.draw.polygon(win, SECOND_PLAYER_COLOR[0], self.polygon_points, 0)
        self.polygon_points[-1], self.polygon_points[-2] = self.polygon_points[-2], self.polygon_points[-1]

        pygame.draw.polygon(win, FIRST_PLAYER_COLOR[0], self.polygon_points, 0)
        self.polygon_points[-1], self.polygon_points[-2] = self.polygon_points[-2], self.polygon_points[-1]
        for i, j in product(range(11), repeat=2):
            self.shadow_hex[i][j].draw(win)
            self.hex_cells[i][j].draw(win)

    def get_hex_cords(self, position):
        for row_index in range(0, 11):
            hex_cell = self.hex_cells[row_index][0]

            if abs(position[1] - hex_cell.center[1]) <= hex_cell.radius_of_circle:
                possible_rows = ([row_index + 1] if row_index + 1 < 11 else []) + [row_index]
                column_distance = (position[0] - (hex_cell.center[0] - hex_cell.height)) / (2 * self.size)

                possible_columns = (
                                       [int(column_distance) - 1] if 0 <= int(column_distance) - 1 <= 10 else []
                                   ) + [int(column_distance)] if 0 <= int(column_distance) <= 10 else []

                for i, j in product(possible_rows, possible_columns):
                    if self.hex_cells[i][j].clicked(position):
                        return i, j
                return -1, False
        return -1, False

    def highlight_hex_cell(self, window, color, previous_pointer, pos):
        current_row, current_column = self.get_hex_cords(pos)

        # Save the previous pointer if the cursor is outside the hex grid
        if current_row == -1:
            if previous_pointer:
                self.hex_cells[previous_pointer[0]][previous_pointer[1]].draw(window)
            return previous_pointer

        # Highlighting the current cell
        current_cell = self.hex_cells[current_row][current_column]
        pygame.draw.circle(window, color, current_cell.center, 0.3 * current_cell.height)

        # Redrawing the previously highlighted cell to remove highlight
        if previous_pointer and (current_row, current_column) != previous_pointer:
            self.hex_cells[previous_pointer[0]][previous_pointer[1]].draw(window)

        return current_row, current_column

    def update_hex_cell(self, row, column, player1_turn):
        cell = self.hex_cells[row][column]
        cell.used = True
        cell.color, cell.owner = FIRST_PLAYER_COLOR if not player1_turn else SECOND_PLAYER_COLOR
        cell.draw(self.win)

    def clear_hex_cell(self, row, column):
        cell = self.hex_cells[row][column]
        cell.used = False
        cell.color, cell.owner = (255, 255, 255), None
        cell.draw(self.win)

    def update_board(self, array):
        for row, column in product(range(11), repeat=2):
            cell = self.hex_cells[row][column]
            # if do in one line, line would be E501 line too long ( > 120 characters)
            if array[row][column] == 1:
                cell.used = True
                cell.color, cell.owner = FIRST_PLAYER_COLOR
            elif array[row][column] == 2:
                cell.used = True
                cell.color, cell.owner = SECOND_PLAYER_COLOR
            else:
                cell.used = False
                cell.color, cell.owner = (255, 255, 255), None
            cell.draw(self.win)

    def draw_dot(self, pos, player1_turn):
        color = FIRST_PLAYER_COLOR[0] if player1_turn else SECOND_PLAYER_COLOR[0]
        self.coordinates = self.highlight_hex_cell(self.win, color, self.coordinates, pos)
