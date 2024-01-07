import pygame
import sys
from classes.gui.constants import FIRST_PLAYER_COLOR, SECOND_PLAYER_COLOR, blit_background
from classes.gui.constants import WIDTH, HEIGHT, FONT, TEXT_COLOR, FPS
from classes.check_for_win import WinnerChecker

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
    def __init__(self, buttons, game, revert=False, back_button=None, gui_board=None):
        if gui_board:
            super().__init__(buttons, gui_board.win)
        else:
            super().__init__(buttons, game.win)
        self.game = game
        self.gui_board = gui_board
        self.back_button = back_button
        self.revert = revert
        self.graph = WinnerChecker(self.game.board.cells, 2 if self.game.player1_turn else 1, True)
        self.color = FIRST_PLAYER_COLOR if self.graph.color == 1 else SECOND_PLAYER_COLOR

    def animate_winner(self, graph, color):
        """Animate the winning path by flashing the cells."""
        for i, j in graph.wining_cluster:
            cell = self.gui_board.hex_cells[i][j]
            cell.color = color
            cell.draw(self.win)

    def display_menu(self):
        run = True
        pygame.draw.rect(self.surface, (128, 128, 128, 120), [0, 0, WIDTH, HEIGHT])
        self.win.blit(self.surface, (0, 0))
        self.draw_menu_background()
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
                        self.animate_winner(self.graph, self.color[0])

                        self.game.revert_move()
                        self.gui_board.update_board(self.game.board.cells)
                        return True
                    self.back_button.draw(self.win)
            if counter < 5000:
                counter += 1
            if counter % 600 == 0:
                self.animate_winner(self.graph, self.color[0])
                self.draw_menu_background()
            elif counter % 300 == 0:
                color = (0, 255, 0)
                self.animate_winner(self.graph, color)
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


class ShowInstruction(Menu):
    def draw_menu_background(self):
        super().draw_menu_background()
        instructions = [
            "Hex Game Rules:",
            "1. Objective: Connect opposing sides with an unbroken chain.",
            "2. Players alternate placing one piece on any empty space.",
            "3. First to connect their sides wins.",
            "4. No draws: There will always be a winner.",
            "5. Strategy: Create good blockade!",
            "6. MainPoint: Just have fun"
        ]
        rect = [WIDTH*0.02, HEIGHT*0.09, WIDTH*0.9, HEIGHT*0.65]
        pygame.draw.rect(self.surface, (0, 0, 0, 200), rect, 0, 10)
        self.win.blit(self.surface, (0, 0))

        y = HEIGHT*0.12  # Starting Y position of the first line
        for line in instructions:
            text = FONT.render(line, True, TEXT_COLOR)
            self.win.blit(text, (WIDTH*0.04, y))
            y += HEIGHT*0.09  # Move to the next line
