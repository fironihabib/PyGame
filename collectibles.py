import pygame
import math

from settings import *

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE // 2, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.centerx = x + TILE_SIZE // 2
        self.rect.centery = y + TILE_SIZE // 2
        
        # Animation variables
        self.animation_timer = 0
        self.animation_speed = 100  # ms between frames
        self.current_frame = 0
        
        # Movement variables for floating effect
        self.original_y = self.rect.centery
        self.offset = 0
        self.float_speed = 0.05

class Coin(Collectible):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill(YELLOW)  # Yellow circle as coin placeholder
        
        # Make the coin a circle
        pygame.draw.circle(self.image, YELLOW, 
                          (TILE_SIZE // 4, TILE_SIZE // 4), 
                          TILE_SIZE // 4)
        
        # Make the background transparent
        self.image.set_colorkey(BLACK)
    
    def update(self):
        # Create floating effect
        self.offset = 4 * (pygame.time.get_ticks() / 1000 % 1)
        if pygame.time.get_ticks() / 1000 % 2 > 1:
            self.offset = 4 - self.offset
        
        self.rect.centery = self.original_y + self.offset
        
        # Create spinning animation by changing size slightly
        scale = 0.8 + 0.2 * abs(math.sin(pygame.time.get_ticks() / 200))
        size = int(TILE_SIZE // 2 * scale)
        
        # Recreate image with new size
        self.image = pygame.Surface((TILE_SIZE // 2, TILE_SIZE // 2))
        self.image.fill(BLACK)  # Fill with transparent color
        pygame.draw.circle(self.image, YELLOW, 
                          (TILE_SIZE // 4, TILE_SIZE // 4), 
                          int(TILE_SIZE // 4 * scale))
        self.image.set_colorkey(BLACK)

class PowerUp(Collectible):
    def __init__(self, x, y, power_type="speed"):
        super().__init__(x, y)
        self.power_type = power_type
        
        # Different colors for different power-ups
        if power_type == "speed":
            self.image.fill(BLUE)
        elif power_type == "jump":
            self.image.fill(GREEN)
        elif power_type == "invincible":
            self.image.fill(PURPLE)
        
        # Make the powerup a square with rounded corners
        pygame.draw.rect(self.image, self.image.get_at((0, 0)), 
                         pygame.Rect(0, 0, TILE_SIZE // 2, TILE_SIZE // 2), 
                         border_radius=TILE_SIZE // 8)
    
    def update(self):
        # Create pulsing effect
        scale = 0.8 + 0.2 * abs(pygame.sin(pygame.time.get_ticks() / 300))
        size = int(TILE_SIZE // 2 * scale)
        
        # Update position with floating effect
        self.rect.centery = self.original_y + 3 * pygame.sin(pygame.time.get_ticks() / 500)