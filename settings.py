
class Settings:
    def __init__(self):
        """Initialize the game's static settings."""
        
        self.bullet_width=50
        self.bullet_height=100
        self.bullet_color=(60,60,60)
        self.bullets_allowed=3
        self.alien_speed=8.5
        self.fleet_drop_speed=9
       
        #fleet_direction of 1 represents right: -1 represents left.
        self.fleet_direction=1
        self.ship_limit=3
        #How quickly the game speeds up
        self.speedup_scale=1.1
        #How quickly the alien point values increaes
        self.score_scale=1.5
        self.initialize_dynamic_settings()
        self.increase_speed()
    def initialize_dynamic_settings(self):
        """"Initialize settings that change throughout the game."""
        self.ship_speed=14    #11.5
        self.bullet_speed=20
        self.alien_speed=10
        
        # Scoring settings
        self.alien_points=50
        #fleet_direction of 1 represent right; -1 represents left.
        self.fleet_direction=1
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *=self.speedup_scale
        self.bullet_speed *=self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points=int(self.alien_points * self.score_scale)
        #print(self.alien_points)

        
        

        