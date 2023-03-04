import pygame
class Spark:
    width = 28
    height = 28
    def __init__(self, x, y, isMoving, distance, direction, speed):
        self.position = pygame.Vector2()
        self.position.xy = x, y
        self.isMoving = isMoving
        self.initialDistance = distance
        self.direction = direction
        self.initalDirection = direction
        self.distance = 0
        self.speed = speed
        if direction == -1:
            self.distance = distance
    def update(self, dt):
        self.position.xy 
        if self.isMoving:
            self.position.xy = (self.position.x + self.direction*self.speed*dt, self.position.y)
            self.distance += self.direction*self.speed*dt
            if self.distance >= self.initialDistance:
                self.direction = -1
            if self.distance <= 0:
                self.direction = 1