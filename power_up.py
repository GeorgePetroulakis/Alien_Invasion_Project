import pygame
from pygame.time import set_timer

class PowerUp:
    def __init__(self, ai):
        """Initialize the power-up related attributes."""
        self.stats = ai.stats
        self.settings = ai.settings
        self.ship = ai.ship
        self.active = False  # To track if a power-up is currently active
        self.duration = 5000  # Duration of the power-up in milliseconds (5 seconds)
        self.end_time = None  # To track when the power-up should end

    def check_for_power_up(self):
        """Check if a power-up should be activated."""
        if self.stats.level % 5 == 0 and not self.active:
            self.activate_power_up()

    def activate_power_up(self):
        """Activate the power-up and set a timer for its duration."""
        self.settings.bullets_allowed = 10
        self.ship.bullet_cooldown = 0
        self.active = True
        self.end_time = pygame.time.get_ticks() + self.duration
        
        # Notify the ship about the power-up activation
        self.ship.activate_power_up()
        
    
        # Set a timer event to deactivate the power-up after the duration
        set_timer(pygame.USEREVENT + 1, self.duration)

    def update(self):
        """Check if the power-up's duration has ended."""
        if self.active and pygame.time.get_ticks() >= self.end_time:
            self.deactivate_power_up()

    def deactivate_power_up(self):
        """Revert the settings after the power-up ends."""
        self.settings.bullets_allowed = 3 # Assuming 2 is the default value
        self.ship.bullet_cooldown = 6  # Reset to the default value
        self.active = False
        
        # Notify the ship about the power-up deactivation
        self.ship.deactivate_power_up()
