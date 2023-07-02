import pygame

from settings import *
from entity import Entity

# Enemy class for creating and managing an enemy
class Enemy(Entity):
  def __init__(self, pos, path, groups, shoot, player, collision_sprites):
    super().__init__(pos, path, groups, shoot)
    self.player = player  # Player to attack
    # Check if the enemy is colliding with any other sprite
    for sprite in collision_sprites.sprites():
      if sprite.rect.collidepoint(self.rect.midbottom):
        self.rect.bottom = sprite.rect.top
    self.cooldown = 1000  # Cooldown for the enemy attack
    self.health = 3  # Health of the enemy

  # Gets the status of the enemy based on the player's position
  def get_status(self):
    if self.player.rect.centerx < self.rect.centerx:
      self.status = 'left'
    else:
      self.status = 'right'

  # Checks if the enemy can fire at the player
  def check_fire(self):
    enemy_pos = pygame.math.Vector2(self.rect.center)
    player_pos = pygame.math.Vector2(self.player.rect.center)

    distance = (player_pos - enemy_pos).magnitude()  # Distance to the player
    # Check if the player is on the same y-axis
    same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False

    # Fires a bullet if the conditions are met
    if distance < 600 and same_y and self.can_shoot:
      bullet_direction = pygame.math.Vector2(1, 0) if self.status == 'right' else pygame.math.Vector2(-1, 0)
      y_offset = pygame.math.Vector2(0, -16)
      pos = self.rect.center + bullet_direction * 80
      self.shoot(pos + y_offset, bullet_direction, self)

      self.can_shoot = False
      self.shoot_time = pygame.time.get_ticks()
      self.shoot_sound.play()

  # Updates the enemy's status, animation and checks for possible actions
  def update(self, dt):
    self.get_status()
    self.animate(dt)
    self.blink()

    self.shoot_timer()
    self.invulnerability_timer()
    self.check_fire()

    self.check_death()
