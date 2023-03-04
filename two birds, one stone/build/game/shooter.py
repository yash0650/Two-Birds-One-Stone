import pygame
from pygame.constants import TIMER_RESOLUTION
class Shooter:
    position = pygame.Vector2()
    width = 70
    height = 67
    direction = 0
    hasBullet = True
    def __init__(self):
        self.position.xy = 320 - self.width/2, 400
    def setDirection(self, direction):
        self.direction = direction
    def update(self, dt):
        self.direction = 0
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_LEFT]:
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            self.direction = 1
        if (not(self.position.x < 0 and self.direction == -1) and not(self.position.x + self.width > 640 and self.direction == 1)):
            self.position.xy = (self.position.x + self.direction*120*dt, self.position.y) 
    def reset(self):
        self.hasBullet = True
        self.position.xy = 320 - self.width/2, 400