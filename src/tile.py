import pygame
from settings import *

# Tile class for creating and managing a tile
class Tile(pygame.sprite.Sprite):
  def __init__(self, pos, surf, groups, z):
    super().__init__(groups)
    self.image = surf  # Image of the tile
    self.rect = self.image.get_rect(topleft = pos)  # Position of the tile
    self.z = z  # Layer of the tile

# CollisionTile class for creating and managing a collision tile
class CollisionTile(Tile):
  def __init__(self, pos, surf, groups):
    super().__init__(pos, surf, groups, LAYERS['Level'])
    self.old_rect = self.rect.copy()  # Previous position of the tile

# MovingPlatform class for creating and managing a moving platform
class MovingPlatform(CollisionTile):
  def __init__(self, pos, surf, groups):
    super().__init__(pos, surf, groups)

    self.direction = pygame.math.Vector2(0, -1)  # Direction of the platform
    self.speed = 200  # Speed of the platform
    self.pos = pygame.math.Vector2(self.rect.topleft)  # Position of the platform

  # Updates the position of the platform
  def update(self, dt):
    self.old_rect = self.rect.copy()
    self.pos.y += self.direction.y * self.speed * dt
    self.rect.topleft = (round(self.pos.x), round(self.pos.y))
