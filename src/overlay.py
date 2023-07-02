import pygame

# Overlay class for creating and displaying an overlay
class Overlay:
  def __init__(self, player):
    self.player = player  # Player for which the overlay is displayed
    self.display_surface = pygame.display.get_surface()  # Surface on which the overlay is displayed
    self.health_surf = pygame.image.load('./resources/graphics/health.png').convert_alpha()  # Image of the health icon

  # Displays the health of the player
  def display(self):
    for h in range(self.player.health):
      # Position of each health icon
      x = 10 + h * (self.health_surf.get_width() + 4)
      y = 10
      self.display_surface.blit(self.health_surf, (x, y))  # Blits the health icon on the surface
