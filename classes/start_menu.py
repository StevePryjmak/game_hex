import pygame
import sys
from classes.constants import FIRST_PLAYER_COLOR, SECOND_PLAYER_COLOR, blit_background
from classes.constants import WIDTH, HEIGHT, FONT, TEXT_COLOR, FPS
from classes.checking_for_winner import Graph

clock = pygame.time.Clock()


def quit_game():
    pygame.quit()
    sys.exit()


class Menu:
    def __init__(self, buttons, win):
        self.buttons = buttons
        self.win = win
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def display_menu(self):
        try:
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
        except KeyboardInterrupt:
            quit_game()

    def draw_menu_background(self):
        blit_background(self.win)


class GameEndMenu(Menu):
    def __init__(self, buttons, game, revert=False, back_button=None):
        super().__init__(buttons, game.win)
        self.game = game
        self.back_button = back_button
        self.revert = revert
        self.graph = Graph(self.game.board.hex_cells, 2 if self.game.player1_turn else 1)
        self.color = FIRST_PLAYER_COLOR if self.graph.color == 1 else SECOND_PLAYER_COLOR

    def display_menu(self):
        run = True
        pygame.draw.rect(self.surface, (128, 128, 128, 120), [0, 0, WIDTH, HEIGHT])
        self.win.blit(self.surface, (0, 0))
        counter = 0
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in self.buttons:
                    if button.clicked(event):
                        button.execute_funk()
                if self.revert:
                    if self.back_button.clicked(event):
                        self.game.animate_winner(self.graph, self.color[0])
                        self.game.revert_move(pygame.mouse.get_pos())
                        return True
                    self.back_button.draw(self.win)
            if counter < 5000:
                counter += 1
            if counter % 600 == 0:
                self.game.animate_winner(self.graph, self.color[0])
                self.draw_menu_background()
            elif counter % 300 == 0:
                color = (0, 255, 0)
                self.game.animate_winner(self.graph, color)
                self.draw_menu_background()
            pygame.display.flip()
            for button in self.buttons:
                button.draw(self.win)

    def draw_menu_background(self):
        offset = 0.3
        rect = [WIDTH*offset, HEIGHT*offset, WIDTH-2*WIDTH*offset, HEIGHT-2*HEIGHT*offset]
        pygame.draw.rect(self.win, (128, 128, 128), rect, 0, 10)
        font = pygame.font.SysFont('8-BIT WONDER.TTF', int(min(HEIGHT, WIDTH)*0.15))
        instruction_text = font.render(
            f'{self.color[1]} wins', True, self.color[0])
        instruction_text_rect = instruction_text.get_rect(center=(WIDTH / 2, HEIGHT * 0.37))
        self.win.blit(instruction_text, instruction_text_rect)


class SelectNetworkMenu(Menu):
    def draw_menu_background(self):
        super().draw_menu_background()
        instruction_text = FONT.render(
            f'Choose Network Mod: Server goes first, Client goes second', True, TEXT_COLOR)
        instruction_text_rect = instruction_text.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        self.win.blit(instruction_text, instruction_text_rect)


class OpponentAbandonedGameMenu(Menu):
    def draw_menu_background(self):
        super().draw_menu_background()
        offset = 0.28
        rect = [WIDTH * offset, HEIGHT * offset, WIDTH - 2 * WIDTH * offset, HEIGHT - 2 * HEIGHT * offset]
        pygame.draw.rect(self.surface, (128, 128, 128, 150), rect, 0, 10)
        self.win.blit(self.surface, (0, 0))
        font = pygame.font.SysFont('8-BIT WONDER.TTF', int(min(HEIGHT, WIDTH) * 0.12))
        instruction_text = font.render(
            f'Opponent Left', True, TEXT_COLOR)
        instruction_text_rect = instruction_text.get_rect(center=(WIDTH / 2, HEIGHT * 0.37))
        self.win.blit(instruction_text, instruction_text_rect)
