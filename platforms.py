import pygame
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Create a simple platform sprite
        self.image = pygame.image.load("assets/sprites/platform.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        
        # Set up rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class MovingPlatform(Platform):
    def __init__(self, x, y, move_x=0, move_y=0, range=100, speed=1):
        super().__init__(x, y)
        self.image.fill(YELLOW)  # Yellow for moving platforms
        
        # Movement parameters
        self.move_x = move_x  # 1 for right, -1 for left
        self.move_y = move_y  # 1 for down, -1 for up
        self.range = range    # How far it moves
        self.speed = speed    # How fast it moves
        
        # Track original position and movement
        self.start_x = x
        self.start_y = y
        self.current_distance = 0
    
    def update(self):
        # Update position based on movement direction
        if self.move_x != 0:
            self.rect.x += self.move_x * self.speed
            self.current_distance += abs(self.move_x * self.speed)
            
            # Change direction if we've moved far enough
            if self.current_distance >= self.range:
                self.move_x *= -1  # Reverse direction
                self.current_distance = 0
        
        if self.move_y != 0:
            self.rect.y += self.move_y * self.speed
            self.current_distance += abs(self.move_y * self.speed)
            
            # Change direction if we've moved far enough
            if self.current_distance >= self.range:
                self.move_y *= -1  # Reverse direction
                self.current_distance = 0

class BreakablePlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill(RED)  # Red for breakable platforms
        
        # Platform state
        self.broken = False
        self.break_timer = 0
    
    def break_platform(self):
        if not self.broken:
            self.broken = True
            self.break_timer = pygame.time.get_ticks()
            # Change appearance to show it's breaking
            self.image.fill((100, 0, 0))  # Darker red
    
    def update(self):
        # Check if platform should be removed
        if self.broken:
            now = pygame.time.get_ticks()
            if now - self.break_timer > 500:  # Remove after 500ms
                self.kill()