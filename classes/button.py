import pygame
from classes.constants import BTN_COLOR, HOVER_COLOR, FONT, TEXT_COLOR


def nothing():
    return


class Button:
    def __init__(self, pos, width, height, text='',
                 funk=nothing, arguments=None, color=BTN_COLOR, border_radius=-1, img='', enabled=True):
        if img != '':
            self.image = pygame.image.load(img).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))

        else:
            self.image = ''
        self.color = color
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.text = text
        self.enabled = enabled
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.border_radius = int(min(width, height)/2 if border_radius == -1 else border_radius)
        self.func_to_execute_after_button_was_clicked = funk
        self.funk_arguments = arguments if arguments is not None else ()

    def draw(self, win):
        if self.image:
            win.blit(self.image, (self.x, self.y))
        else:

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
        if not self.funk_arguments:
            return self.func_to_execute_after_button_was_clicked()
        else:
            return self.func_to_execute_after_button_was_clicked(self.funk_arguments)
