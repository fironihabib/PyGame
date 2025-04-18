import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        
        # Create a simple enemy sprite
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)  # Red square as enemy placeholder
        
        # Set up rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement variables
        self.vel_x = 1  # Start moving right
        self.vel_y = 0
        
        # Animation variables
        self.current_frame = 0
        self.last_update = 0
    
    def update(self):
        # Apply movement
        self.rect.x += self.vel_x
        
        # Check for collisions with platforms
        self.check_collisions()
        
        # Check if at edge of platform
        self.check_edges()
        
        # Update animation
        self.animate()
    
    def check_collisions(self):
        # Check collision with platforms
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        for platform in hits:
            # Check for side collision and reverse direction
            if self.vel_x > 0:
                self.rect.right = platform.rect.left
                self.vel_x *= -1
            elif self.vel_x < 0:
                self.rect.left = platform.rect.right
                self.vel_x *= -1
    
    def check_edges(self):
        # Check if at edge of platform
        if self.vel_x != 0:  # Only check if moving horizontally
            # Create a rect below and to the right/left to check for platform
            check_rect = pygame.Rect(0, 0, 1, TILE_SIZE // 2)
            
            if self.vel_x > 0:  # Moving right
                check_rect.topleft = (self.rect.right, self.rect.bottom)
            else:  # Moving left
                check_rect.topright = (self.rect.left, self.rect.bottom)
            
            # Check if there's a platform below
            platform_below = False
            for platform in self.game.platforms:
                if check_rect.colliderect(platform.rect):
                    platform_below = True
                    break
            
            # If no platform below, reverse direction
            if not platform_below:
                self.vel_x *= -1
    
    def animate(self):
        # Simple animation to indicate movement direction
        now = pygame.time.get_ticks()
        
        # Change appearance every 200ms
        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 2
            
            # Alternate between two shades of red
            if self.current_frame == 0:
                self.image.fill(RED)
            else:
                self.image.fill((200, 0, 0))  # Slightly darker red
            
            # Draw an arrow to indicate direction
            arrow_points = []
            if self.vel_x > 0:  # Right-facing arrow
                arrow_points = [
                    (TILE_SIZE // 4, TILE_SIZE // 4),
                    (3 * TILE_SIZE // 4, TILE_SIZE // 2),
                    (TILE_SIZE // 4, 3 * TILE_SIZE // 4)
                ]
            else:  # Left-facing arrow
                arrow_points = [
                    (3 * TILE_SIZE // 4, TILE_SIZE // 4),
                    (TILE_SIZE // 4, TILE_SIZE // 2),
                    (3 * TILE_SIZE // 4, 3 * TILE_SIZE // 4)
                ]
            
            pygame.draw.polygon(self.image, BLACK, arrow_points)