import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, ai):
        super().__init__()
        self.screen = ai.screen
        self.settings = ai.settings
        self.original_image = pygame.image.load("C:\\Users\\Owner\\Desktop\\code.py\\Project(Alien Invasion)\\images\\bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (self.settings.bullet_width, self.settings.bullet_height))
        self.rect = self.image.get_rect()
        self.rect.midtop = ai.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the exact position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)
