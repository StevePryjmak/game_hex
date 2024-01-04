import pygame
import sys
from classes.constants import WIDTH, HEIGHT, FIRST_PLAYER_COLOR, SECOND_PLAYER_COLOR, blit_background
from classes.button import Button
from classes.constants import WIDTH, HEIGHT, BG_COLOR, FONT, TEXT_COLOR, FPS
from classes.checking_for_winner import Graph

clock = pygame.time.Clock()

class Menu:
    def __init__(self, buttons, win):
        self.buttons = buttons
        self.win = win

    def display_menu(self):
        run = True
        self.draw_menu_background()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in self.buttons:
                    if button.clicked(event):
                        button.execute_funk()

            for button in self.buttons:
                button.draw(self.win)
            pygame.display.flip()
            clock.tick(FPS)

    def draw_menu_background(self):
        blit_background(self.win)


class SelectNetworkMenu(Menu):
    def draw_menu_background(self):
        super().draw_menu_background()
        instruction_text = FONT.render(
            f'Choose Network Mod: Server goes first, Client goes second', True, TEXT_COLOR)
        instruction_text_rect = instruction_text.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        self.win.blit(instruction_text, instruction_text_rect)

class GameEndMenu(Menu):
    def __init__(self, buttons, game):
        super().__init__(buttons, game.win)
        self.game = game
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def display_menu(self):
        run = True
        pygame.draw.rect(self.surface, (128, 128, 128, 120), [0, 0, WIDTH, HEIGHT])
        self.win.blit(self.surface, (0, 0))
        counter = 0
        graph = Graph(self.game.board.hex_cells, 2 if self.game.player1_turn else 1)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in self.buttons:
                    if button.clicked(event):
                        button.execute_funk()
                if self.game.board.back_button.clicked(event):
                    color = FIRST_PLAYER_COLOR[0] if graph.color == 1 else SECOND_PLAYER_COLOR[0]
                    self.game.animate_winner(graph, color)
                    self.game.revert_move(pygame.mouse.get_pos())
                    return True
                self.game.board.back_button.draw(self.win)
            if counter < 5000:
                counter += 1
            if counter % 600 == 0:
                color = FIRST_PLAYER_COLOR[0] if graph.color == 1 else SECOND_PLAYER_COLOR[0]
                self.game.animate_winner(graph, color)
            elif counter % 300 == 0:
                color = (0, 255, 0)
                self.game.animate_winner(graph, color)

            self.draw_menu_background()
            for button in self.buttons:
                button.draw(self.win)
            pygame.display.flip()

    def draw_menu_background(self):
        offset = 0.3
        rect = [WIDTH*offset, HEIGHT*offset, WIDTH-2*WIDTH*offset, HEIGHT-2*HEIGHT*offset]
        pygame.draw.rect(self.win, (128, 128, 128), rect, 0, 10)


