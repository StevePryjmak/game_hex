import pygame


class Button:
    def __init__(self, color, x, y, width, height, text='', enabled=False):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.enabled = enabled
        self.button_rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        button_surface = pygame.Surface((self.width, self.height))
        button_surface.fill(self.color)
        win.blit(button_surface, self.button_rect.topleft)
        if self.text:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.button_rect.center)
            win.blit(text_surface, text_rect.topleft)

    def mouse(self, pos):
        if self.button_rect.collidepoint(pos) and not self.enabled:
            return True
        return False

    def toggle_state(self):
        self.enabled = not self.enabled
