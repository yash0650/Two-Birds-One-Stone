import pygame
class Box:
    width = 64
    height = 64
    def __init__(self, x, y):
        self.position = pygame.Vector2()
        self.position.xy = x, y
    def update(self, dt):
        self.position.xy 