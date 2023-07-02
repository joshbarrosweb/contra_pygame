import pygame
import os
from math import sin

from settings import *

# Entity class for creating and managing an entity
class Entity(pygame.sprite.Sprite):
  def __init__(self, pos, path, groups, shoot):
    super().__init__(groups)

    self.import_assets(path)  # Importing assets for the entity
    self.frame_index = 0  # Index for the entity's animation frame
    self.status = 'right'  # Initial status of the entity

    self.image = self.animations[self.status][self.frame_index]
    self.rect = self.image.get_rect(topleft = pos)
    self.old_rect = self.rect.copy()
    self.z = LAYERS['Level']  # Layer of the entity
    self.mask = pygame.mask.from_surface(self.image)

    self.direction = pygame.math.Vector2()  # Direction of the entity
    self.pos = pygame.math.Vector2(self.rect.topleft)  # Position of the entity
    self.speed = 400  # Speed of the entity

    self.shoot = shoot  # Shoot method for the entity
    self.can_shoot = True  # Entity's ability to shoot
    self.shoot_time = None  # Time when the entity shot
    self.cooldown = 200  # Cooldown time for shooting
    self.duck = False  # Whether the entity is ducking or not

    self.health = 3  # Health of the entity
    self.is_vulnerable = True  # Entity's vulnerability to attacks
    self.hit_time = None  # Time when the entity got hit
    self.invulnerability_duration = 500  # Time duration for invulnerability after getting hit

    self.hit_sound = pygame.mixer.Sound('./resources/audio/hit.wav')  # Sound when the entity gets hit
    self.hit_sound.set_volume(0.5)
    self.shoot_sound = pygame.mixer.Sound('./resources/audio/bullet.wav')  # Sound when the entity shoots
    self.hit_sound.set_volume(0.5)

  # Method for importing assets for the entity
  def import_assets(self, path):
    self.animations = {}
    for index, folder in enumerate(os.walk(path)):
      if index == 0:
        for name in folder[1]:
          self.animations[name] = []
      else:
        for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
          path = folder[0].replace(os.sep, '/') + '/' + file_name
          surf = pygame.image.load(path).convert_alpha()
          key = folder[0].split(os.sep)[4]
          self.animations[key].append(surf)

  # Method for making the entity blink
  def blink(self):
    if not self.is_vulnerable:
      if self.wave_value():
        mask = pygame.mask.from_surface(self.image)
        white_surf = mask.to_surface()
        white_surf.set_colorkey((0, 0, 0))
        self.image = white_surf

  # Method for getting the wave value for blinking
  def wave_value(self):
    value = sin(pygame.time.get_ticks())
    if value >= 0:
      return True
    else:
      return False

  # Method for causing damage to the entity
  def damage(self):
    if self.is_vulnerable:
      self.health -= 1
      self.is_vulnerable = False
      self.hit_time = pygame.time.get_ticks()
      self.hit_sound.play()

  # Method for checking if the entity is dead
  def check_death(self):
    if self.health <= 0:
      self.kill()

  # Method for handling the entity's shooting timer
  def shoot_timer(self):
    if not self.can_shoot:
      current_time = pygame.time.get_ticks()
      if current_time - self.shoot_time > self.cooldown:
        self.can_shoot = True

  # Method for handling the entity's invulnerability timer
  def invulnerability_timer(self):
    if not self.is_vulnerable:
      current_time = pygame.time.get_ticks()
      if current_time - self.hit_time > self.invulnerability_duration:
        self.is_vulnerable = True

  # Method for animating the entity
  def animate(self, dt):
    self.frame_index += 7 * dt
    if self.frame_index >= len(self.animations[self.status]):
      self.frame_index = 0

    self.image = self.animations[self.status][int(self.frame_index)]
    self.mask = pygame.mask.from_surface(self.image)
