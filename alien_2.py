import pygame
from pygame.sprite import Sprite
class Alien_2(Sprite):
    """A class to represent a single alien in the fleet"""
    
    def __init__(self,ai):
        super().__init__()
        self.screen=ai.screen
        self.rect_screen=self.screen.get_rect()

        #Load the alien image and set its rect attribute 
        self.image=pygame.image.load(r"C:\Users\Owner\Desktop\code.py\Project(Alien Invasion)\images\alien3.png")
        self.rect=self.image.get_rect()
        self.settings=ai.settings
        self.right=self.rect_screen.right 
    
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect=self.screen.get_rect()
        if (self.right > screen_rect.right) or (self.rect_screen.left < 0):
            return True
    def update(self):
        """Move the alien to the right"""
        while self.check_edges():
            self.x+=self.settings.alien_speed *self.settings.fleet_direction
            self.rect.x=self.x
    
