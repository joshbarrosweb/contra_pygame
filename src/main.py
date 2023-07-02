# Import necessary modules
import pygame, sys
from pytmx.util_pygame import load_pygame

from settings import *
from tile import Tile, CollisionTile, MovingPlatform
from player import Player
from bullet import Bullet, FireAnimation
from enemy import Enemy
from overlay import Overlay

# Define the AllSprites group, where all the sprites in the game will be stored
class AllSprites(pygame.sprite.Group):
  def __init__(self):
    super().__init__()
    # Get the display surface where the sprites will be drawn
    self.display_surface = pygame.display.get_surface()
    # Initialize an offset vector to adjust the drawing of the sprites based on the player's position
    self.offset = pygame.math.Vector2()

    # Load images for the sky and the TMX map
    self.fg_sky = pygame.image.load('./resources/graphics/sky/fg_sky.png').convert_alpha()
    self.bg_sky = pygame.image.load('./resources/graphics/sky/bg_sky.png').convert_alpha()
    tmx_map = load_pygame('./resources/data/map.tmx')

    # Calculate the number of times the sky image should be drawn to cover the whole map
    self.padding = WINDOW_WIDTH / 2
    self.sky_width = self.bg_sky.get_width()
    map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
    self.sky_num = int(map_width // self.sky_width)

  # Method to draw the sprites on the screen, sorted by their z attribute
  def customize_draw(self, player):
    # Update the offset according to the player's position
    self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
    self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

    # Draw the sky images
    for x in range(self.sky_num):
      x_pos = -self.padding + (x * self.sky_width)
      self.display_surface.blit(self.bg_sky, (x_pos - self.offset.x / 2.5, 900 - self.offset.y / 2.5))
      self.display_surface.blit(self.fg_sky, (x_pos - self.offset.x / 2, 900 - self.offset.y / 2))

    # Draw the sprites
    for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
      offset_rect = sprite.image.get_rect(center = sprite.rect.center)
      offset_rect.center -= self.offset
      self.display_surface.blit(sprite.image, offset_rect)

# Define the Game class, which manages the game loop and the game state
class Game:
  def __init__(self):
    # Initialize Pygame, create the game window and set the window title
    pygame.init()
    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Contra Clone')
    self.clock = pygame.time.Clock()

    # Create the groups of sprites
    self.all_sprites = AllSprites()
    self.collision_sprites = pygame.sprite.Group()
    self.platform_sprites = pygame.sprite.Group()
    self.bullet_sprites = pygame.sprite.Group()
    self.vulnerable_sprites = pygame.sprite.Group()

    # Set up the game, create the overlay and load the bullet and fire images
    self.setup()
    self.overlay = Overlay(self.player)

    self.bullet_surf = pygame.image.load('./resources/graphics/bullet.png').convert_alpha()
    self.fire_surfs = [
      pygame.image.load('./resources/graphics/fire/0.png').convert_alpha(),
      pygame.image.load('./resources/graphics/fire/1.png').convert_alpha()
    ]

    # Load and play the game music
    self.music = pygame.mixer.Sound('./resources/audio/music.wav')
    self.music.play(loops = -1)

  # Set up the game level, and create the player and enemy entities
  def setup(self):
    tmx_map = load_pygame('./resources/data/map.tmx')

    for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
      CollisionTile((x * 64, y * 64), surf, [self.all_sprites, self.collision_sprites])

    for layer in ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']:
      for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
        Tile((x * 64, y * 64), surf, self.all_sprites, LAYERS[layer])

    for obj in tmx_map.get_layer_by_name('Entities'):
      if obj.name == 'Player':
        self.player = Player(
            pos = (obj.x, obj.y),
            groups = [self.all_sprites, self.vulnerable_sprites],
            path = './resources/graphics/player',
            collision_sprites = self.collision_sprites,
            shoot = self.shoot
          )

      if obj.name == 'Enemy':
        Enemy(
          pos = (obj.x, obj.y),
          path = './resources/graphics/enemy',
          groups = [self.all_sprites, self.vulnerable_sprites],
          shoot = self.shoot,
          player = self.player,
          collision_sprites = self.collision_sprites
        )

    self.platform_border_rects = []

    for obj in tmx_map.get_layer_by_name('Platforms'):
      if obj.name == 'Platform':
        MovingPlatform((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.platform_sprites])
      else:
        border_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        self.platform_border_rects.append(border_rect)

  # Check for collisions between platforms and borders, and the player and the platforms
  def platform_collisions(self):
    for platform in self.platform_sprites.sprites():
      for border in self.platform_border_rects:
        if platform.rect.colliderect(border):
          if platform.direction.y < 0:
            platform.rect.top = border.bottom
            platform.pos.y = platform.rect.y
            platform.direction.y = 1
          else:
            platform.rect.bottom = border.top
            platform.pos.y = platform.rect.y
            platform.direction.y = -1

      if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
        platform.rect.bottom = self.player.rect.top
        platform.pos.y = platform.rect.y
        platform.direction.y = -1

  # Check for collisions between bullets and other entities, and deal damage accordingly
  def bullet_collisions(self):
    for obstacle in self.collision_sprites.sprites():
      pygame.sprite.spritecollide(obstacle, self.bullet_sprites, True)

    for sprite in self.vulnerable_sprites.sprites():
      if pygame.sprite.spritecollide(sprite, self.bullet_sprites, True, pygame.sprite.collide_mask):
        sprite.damage()

  # Shoot a bullet
  def shoot(self, pos, direction, entity):
    Bullet(pos, self.bullet_surf, direction, [self.all_sprites, self.bullet_sprites])
    FireAnimation(entity, self.fire_surfs, direction, self.all_sprites)

  # The game loop, which handles events, updates the game state and renders the game objects
  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      dt = self.clock.tick() / 1000
      self.display_surface.fill((249, 131, 103))

      self.platform_collisions()
      self.all_sprites.update(dt)
      self.bullet_collisions()
      self.all_sprites.customize_draw(self.player)
      self.overlay.display()

      pygame.display.update()

# The entry point of the script, which creates a Game instance and starts the game loop
if __name__ == '__main__':
  game = Game()
  game.run()
