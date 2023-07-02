import pygame
from settings import *

# Bullet class for creating and managing a bullet object
class Bullet(pygame.sprite.Sprite):
  def __init__(self, pos, surf, direction, groups):
    super().__init__(groups)
    self.image = surf  # Image of the bullet

    # Flips the image of the bullet if the direction is negative
    if direction.x < 0:
      self.image = pygame.transform.flip(self.image, True, False)

    # Position and layer of the bullet
    self.rect = self.image.get_rect(center = pos)
    self.z = LAYERS['Level']

    # Direction and speed of the bullet
    self.direction = direction
    self.speed = 1200
    self.pos = pygame.math.Vector2(self.rect.center)

    # Time of bullet creation
    self.start_time = pygame.time.get_ticks()
    self.mask = pygame.mask.from_surface(self.image)

  # Updates the position of the bullet
  def update(self, dt):
    self.pos += self.direction * self.speed * dt
    self.rect.center = (round(self.pos.x), round(self.pos.y))

    # Removes the bullet after a second
    if pygame.time.get_ticks() - self.start_time > 1000:
      self.kill()


# FireAnimation class for creating and managing a fire animation
class FireAnimation(pygame.sprite.Sprite):
  def __init__(self, entity, surf_list, direction, groups):
    super().__init__(groups)
    self.entity = entity  # Entity on which the fire animation is applied
    self.frames = surf_list  # List of images for the fire animation

    # Flips the fire animation if the direction is negative
    if direction.x < 0:
      self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]

    # Setting the initial frame
    self.frame_index = 0
    self.image = self.frames[self.frame_index]

    # Setting the offset for the fire animation
    x_offset = 60 if direction.x > 0 else -60
    y_offset = 10 if entity.duck else -16
    self.offset = pygame.math.Vector2(x_offset, y_offset)

    # Position and layer of the fire animation
    self.rect = self.image.get_rect(center = self.entity.rect.center + self.offset)
    self.z = LAYERS['Level']

  # Animates the fire
  def animate(self, dt):
    self.frame_index += 15 * dt
    if self.frame_index >= len(self.frames):
      self.kill()  # Ends the animation if all frames are shown
    else:
      self.image = self.frames[int(self.frame_index)]

  # Moves the animation with the entity
  def move(self):
    self.rect.center = self.entity.rect.center + self.offset

  # Updates the animation
  def update(self, dt):
    self.animate(dt)
    self.move()
