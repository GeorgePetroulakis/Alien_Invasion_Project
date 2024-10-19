import pygame.font
import json
from pathlib import Path
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai):
        """Initialize scorekeeping attributes."""
        self.ai=ai
        self.screen = ai.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai.settings
        self.stats = ai.stats
        self.path=Path('high_score.json')
        # Font settings for scoring information.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.GREEN = (0, 255, 0)
        self.font1=pygame.font.SysFont(None, 68)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    def prep_score(self):
        """Turn the score into a rendered image."""
       
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw scores, level and ships, to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        self.load_high_score()
        high_score_str = str(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.store_high_score()
            self.prep_high_score()

    def store_high_score(self):
        contents=json.dumps(self.stats.high_score)
        self.path.write_text(contents)

    def load_high_score(self):
        if self.path.exists():
            contents=self.path.read_text()
            self.stats.high_score=json.loads(contents)
    
    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font1.render(level_str, True, self.GREEN)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right+5
        self.level_rect.top = self.score_rect.bottom + 20
    
    def prep_ships(self):
        """Show how many ships are left."""
       
        self.ships = pygame.sprite.Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai)
        
            # Scale down the ship image
            scaled_ship_image = pygame.transform.scale(ship.image, (int(ship.rect.width * 0.5), int(ship.rect.height * 0.5)))
            ship.image = scaled_ship_image
        
            # Update the rect to match the scaled image size
            ship.rect = ship.image.get_rect()
            ship.rect.x =  ship_number * ship.rect.width-15
            ship.rect.y = -20
        
            self.ships.add(ship)




    
 
    
        

    
  
   