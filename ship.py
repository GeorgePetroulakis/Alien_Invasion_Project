import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai.screen
        self.settings = ai.settings
        self.screen_rect = ai.screen.get_rect()
        
        # Load ship images for normal and power-up states
        self.original_image = pygame.image.load(r"C:\Users\Owner\Desktop\code.py\Project(Alien Invasion)\images\ship.png").convert_alpha()
        self.original_power_up_image = pygame.image.load(r"C:\Users\Owner\Desktop\code.py\Project(Alien Invasion)\images\plain.png").convert_alpha()
        
        self.power_up_image=pygame.transform.scale(self.original_power_up_image, (225, 225))
        self.image = pygame.transform.scale(self.original_image, (225, 225))
        self.rect = self.image.get_rect()
        self.rect.x = 687.5
        self.rect.y = 720
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        self.firing = False
        self.bullet_cooldown = 6
        self.update()
        self.center_ship()
        
        self.power_up_active = False  # To track if the power-up is active
        
        # Initialize font for displaying messages
        self.font = pygame.font.SysFont(None, 48)
        self.message = ""

    def update(self):
        """Update the ship's position and bullet cooldown."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
        
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
        self.draw_message()

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.x = 687.5
        self.rect.y = 720
        self.x = float(self.rect.x)
    
    def activate_power_up(self):
        """Change the ship's image when power-up is active."""
        self.image = pygame.transform.scale(self.power_up_image, (225, 225))
        self.power_up_active = True
        self.message = "Power-Up Activated!"

    def deactivate_power_up(self):
        """Revert the ship's image back to normal."""
        self.image = pygame.transform.scale(self.original_image, (225, 225))
        self.power_up_active = False
        self.message = ""

    def draw_message(self):
        """Draw the message on the screen."""
        if self.message:
            text_surface = self.font.render(self.message, True, (255, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.centerx = self.screen_rect.centerx*1.5
            text_rect.top = 820
            self.screen.blit(text_surface, text_rect) 