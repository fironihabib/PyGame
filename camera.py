import pygame
from settings import *

class Camera:
    def __init__(self, width, height):
        # The size of the camera view
        self.width = width
        self.height = height
        
        # The camera offset
        self.offset_x = 0
        self.offset_y = 0
        
        # Camera boundaries (world size)
        self.world_width = width
        self.world_height = height
        
        # Smoothing factor for camera movement
        self.smoothing = 0.1
    
    def update(self, target):
        # Calculate where the camera should be positioned
        # Center the camera on the target
        target_x = -target.rect.centerx + self.width // 2
        target_y = -target.rect.centery + self.height // 2
        
        # Apply smoothing to camera movement
        self.offset_x += (target_x - self.offset_x) * self.smoothing
        self.offset_y += (target_y - self.offset_y) * self.smoothing
        
        # Apply clamping to ensure camera doesn't show outside the level
        self.offset_x = min(0, self.offset_x)  # Left edge
        self.offset_y = min(0, self.offset_y)  # Top edge
        
        # Right/bottom edges (adjust with world size)
        self.offset_x = max(-(self.world_width - self.width), self.offset_x)
        self.offset_y = max(-(self.world_height - self.height), self.offset_y)
    
    def apply(self, entity):
        # Apply camera offset to an entity
        return pygame.Rect(
            entity.rect.x + self.offset_x,
            entity.rect.y + self.offset_y,
            entity.rect.width,
            entity.rect.height
        )
    
    def set_world_size(self, width, height):
        # Set the size of the game world
        self.world_width = width
        self.world_height = height