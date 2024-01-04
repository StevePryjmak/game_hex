import pygame
from classes.constants import BTN_COLOR, HOVER_COLOR, FONT, TEXT_COLOR


def nothing():
    return


class Button:
    def __init__(self, pos, width, height, text='', funk=nothing, arguments=-1, color=BTN_COLOR, border_radius=-1, enabled=True):
        self.color = color
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.text = text
        self.enabled = enabled
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.border_radius = int(min(width, height)/2 if border_radius == -1 else border_radius)
        self.func_to_execute_after_button_was_clicked = funk
        self.funk_arguments = arguments

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, border_radius=self.border_radius)

        text_surf = FONT.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)

    def clicked(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = HOVER_COLOR  # Change to hover color
            if event.type == pygame.MOUSEBUTTONUP:
                return True
        else:
            self.color = BTN_COLOR  # Change back to original color
        return False

    def execute_funk(self):
        if self.funk_arguments == -1:
            return self.func_to_execute_after_button_was_clicked()
        return self.func_to_execute_after_button_was_clicked(self.funk_arguments)
