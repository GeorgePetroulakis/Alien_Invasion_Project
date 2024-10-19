import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats 
from ship import Ship
from bullet import Bullet
from alien_0 import Alien_0
from button import Button
from scoreboard import Scoreboard
from power_up import PowerUp
class AlienInvasion:
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.BG = pygame.transform.scale(
            pygame.image.load("C:\\Users\\Owner\\Desktop\\code.py\\Project(Alien Invasion)\\images\\galaxy.bmp"),
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.game_active = False
        self.play_button = Button(self, "Play")
        self.alien_direction=1
        self.original_bullet_speed=self.ship.bullet_cooldown

        self.powerup = PowerUp(self)
    def run_game(self):
        """Start the main loop for the game."""
        running = True
        while running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.sb.prep_ships()
                if self.ship.firing:
                    self._fire_bullet()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
                self.powerup.check_for_power_up()
                self.powerup.update() 
            self._update_screen()
            self.clock.tick(60)
            

    def _update_aliens(self):
        """Check if the fleet is at an edge then update positions."""
        self.move_alien(self.alien_direction,self.settings.alien_speed)
        self.alien_direction_change()
        

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
           self._ship_hit()
        self._check_aliens_bottom()

   
   
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
          

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
             self.ship.firing = True 
         

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            self.ship.firing = False 
            
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.stats.score=0
            self.stats.level = 1 
            self.sb.prep_score()
            self.sb.prep_level() 
            self.sb.prep_ships()
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.game_active = True
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet_0()
            
           
            self.ship.center_ship()

            # Redraw the screen immediately to remove the play button
            self._update_screen()

        # Hide the mouse cursor
            pygame.mouse.set_visible(False)
        pygame.display.flip()
    def alien_direction_change(self):

        all_aliens=self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= self.screen.get_width():
                self.alien_direction=-1
                self.alien_move_down(self.settings.fleet_drop_speed)
            elif alien.rect.left <=0:
                self.alien_direction=1
                self.alien_move_down(self.settings.fleet_drop_speed)
    
    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y+=distance

    def move_alien(self,direction,speed):
        for alien in self.aliens:
            alien.rect.x+= direction*speed

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed and self.ship.bullet_cooldown == 0:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.ship.bullet_cooldown=6
            
    def _update_screen(self):
        self.screen.blit(self.BG, (0, 0))               # Blit the background onto the screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()                              # Blit the ship onto the screen
        self.aliens.draw(self.screen)                   # Draw aliens on the screen

        #Draw the score information.
        self.sb.show_score()
        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()                         # Display the newest screen
       


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
       
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score +=self.settings.alien_points*len(aliens)
                self.stats.aliens_killed += len(aliens)  # Increment aliens killed
            self.sb.prep_score()
            self.sb.check_high_score()

            # Check if the player should receive a power-up
           
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet_0()
            self.settings.increase_speed()
            
            #Increase level.
            self.stats.level+=1
            self.sb.prep_level()

    def _create_fleet_0(self):
        """Create the fleet of aliens."""
        alien = Alien_0(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y =100, 0
        while current_y < (self.settings.screen_height - 350):
            while current_x <= self.screen.get_width() - 400:
                self._create_alien_0(current_x, current_y)
                current_x += 1.5 * alien_width
            current_x = 100
            current_y += 1.5 * alien_height

    def _create_alien_0(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien_0(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

   
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
       
        if self.stats.ships_left > 0:
         # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
        
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet_0()
            
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_height():
              
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
