import pygame


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.pressed = 0
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

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
        if self.button_rect.collidepoint(pos) and not self.pressed:
            print("Button clicked!")
            self.pressed = 1
            return True
        return False
