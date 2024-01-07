import pygame
import math


class Hexagon:
    def __init__(self, center, size, color):
        self.center = center
        self.radius_of_circle = size/math.cos(math.radians(30))
        self.color = color
        self.height = size
        self.used = False
        self.owner = None
        self.points = self.get_points()

    def draw(self, win):
        pygame.draw.polygon(win, self.color, self.points, 0)

    def get_points(self):
        points = []
        for i in range(6):
            angle_deg = 30 + 60 * i
            angle_rad = math.radians(angle_deg)
            x = self.center[0] + self.radius_of_circle * math.cos(angle_rad)
            y = self.center[1] + self.radius_of_circle * math.sin(angle_rad)
            points.append((int(x), int(y)))
        return points

    def clicked(self, pos):
        is_odd = False

        for (x1, y1), (x2, y2) in zip(self.points, self.points[1:] + [self.points[0]]):
            if min(y1, y2) <= pos[1] <= max(y1, y2) and (x1 <= pos[0] or x2 <= pos[0]):
                # ray casting algorithm
                if x1 + (pos[1] - y1) / (y2 - y1) * (x2 - x1) < pos[0]:
                    is_odd = not is_odd

        return is_odd

    def click_and_block(self, pos):
        if self.used:
            return False
        is_odd = self.clicked(pos)
        if is_odd:
            self.used = True
        return is_odd


def example_hexagon():
    import sys
    pygame.init()
    win = pygame.display.set_mode((800, 600))
    hexagon = Hexagon((400, 300), 100, (255, 0, 0))

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if hexagon.clicked(pos):
                    hexagon.color = (0, 255, 0)

        win.fill((255, 255, 255))
        hexagon.draw(win)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    example_hexagon()
