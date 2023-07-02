import pygame, sys

from settings import *
from entity import Entity

# Player class for creating and managing a player
class Player(Entity):
  def __init__(self, pos, groups, path, collision_sprites, shoot):
    super().__init__(pos, path, groups, shoot)

    self.collision_sprites = collision_sprites

    self.gravity = 15  # Gravity affecting the player
    self.jump_speed = 1400  # Jump speed of the player
    self.on_floor = False  # Whether the player is on the floor or not
    self.moving_floor = None  # The floor the player is currently on

    self.health = 10  # Health of the player

  # Method for getting the player's status
  def get_status(self):
    if self.direction.x == 0 and self.on_floor:
      self.status = self.status.split('_')[0] + '_idle'

    if self.direction.y != 0 and not self.on_floor:
      self.status = self.status.split('_')[0] + '_jump'

    if self.on_floor and self.duck:
      self.status = self.status.split('_')[0] + '_duck'

  # Method for checking if the player is in contact with anything
  def check_contact(self):
    bottom_rect = pygame.Rect(0, 0, self.rect.width, 5)
    bottom_rect.midtop = self.rect.midbottom
    for sprite in self.collision_sprites.sprites():
      if sprite.rect.colliderect(bottom_rect):
        if self.direction.y > 0:
          self.on_floor = True
        if hasattr(sprite, 'direction'):
          self.moving_floor = sprite

  # Method for handling player input
  def input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
      self.direction.x = 1
      self.status = 'right'
    elif keys[pygame.K_LEFT]:
      self.direction.x = -1
      self.status = 'left'
    else:
      self.direction.x = 0

    if keys[pygame.K_UP] and self.on_floor:
      self.direction.y = -self.jump_speed

    if keys[pygame.K_DOWN]:
      self.duck = True
    else:
      self.duck = False

    if keys[pygame.K_SPACE] and self.can_shoot:
      direction = pygame.math.Vector2(1, 0) if self.status.split('_')[0] == 'right' else pygame.math.Vector2(-1, 0)
      pos = self.rect.center + direction * 60
      y_offset = pygame.math.Vector2(0, -16) if not self.duck else pygame.math.Vector2(0, 10)

      self.shoot(pos + y_offset, direction, self)

      self.can_shoot = False
      self.shoot_time = pygame.time.get_ticks()
      self.shoot_sound.play()

    # DEBUG: Fly Mode
    # if keys[pygame.K_DOWN]:
    #  self.direction.y = 1
    # elif keys[pygame.K_UP]:
    #  self.direction.y = -1
    # else:
    #  self.direction.y = 0

  # Method for handling player collision with other objects
  def collision(self, direction):
    for sprite in self.collision_sprites.sprites():
      if sprite.rect.colliderect(self.rect):

        if direction == 'horizontal':
          if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
            self.rect.left = sprite.rect.right

          if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
            self.rect.right = sprite.rect.left

          self.pos.x = self.rect.x
        else:
          if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
            self.rect.bottom = sprite.rect.top
            self.on_floor = True

          if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
            self.rect.top = sprite.rect.bottom

          self.pos.y = self.rect.y
          self.direction.y = 0

    if self.on_floor and self.direction.y != 0:
      self.on_floor = False

  # Method for moving the player
  def move(self, dt):
    if self.duck and self.on_floor:
      self.direction.x = 0

    self.pos.x += self.direction.x * self.speed * dt
    self.rect.x = round(self.pos.x)
    self.collision('horizontal')

    self.direction.y += self.gravity
    self.pos.y += self.direction.y * dt

    if self.moving_floor and self.moving_floor.direction.y > 0 and self.direction.y > 0:
      self.direction.y = 0
      self.rect.bottom = self.moving_floor.rect.top
      self.pos.y = self.rect.y
      self.on_floor = True

    self.rect.y = round(self.pos.y)
    self.collision('vertical')
    self.moving_floor = None

    # DEBUG: Fly Mode
    # self.pos.y += self.direction.y * self.speed * dt
    # self.rect.y = round(self.pos.y)
    # self.collision('vertical')

  # Method for checking if the player is dead
  def check_death(self):
    if self.health <= 0:
      pygame.quit()
      sys.exit()

  # Method for updating the player's status
  def update(self, dt):
    self.old_rect = self.rect.copy()
    self.input()
    self.get_status()
    self.move(dt)
    self.check_contact()

    self.animate(dt)
    self.blink()

    self.shoot_timer()
    self.invulnerability_timer()

    self.check_death()
