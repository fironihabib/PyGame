import pygame
import os
from settings import *

def load_image(filename, alpha=True):
    """Load an image and return a pygame surface.
    
    Args:
        filename: The filename of the image to load
        alpha: Whether the image has transparency
        
    Returns:
        A pygame surface
    """
    filepath = os.path.join(SPRITES_DIR, filename)
    
    try:
        if alpha:
            return pygame.image.load(filepath).convert_alpha()
        else:
            return pygame.image.load(filepath).convert()
    except pygame.error:
        # If file doesn't exist, create a placeholder
        print(f"Warning: Could not load image {filepath}")
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surf.fill((255, 0, 255))  # Magenta for missing textures
        if alpha:
            surf.set_colorkey((255, 0, 255))
        return surf

def load_sound(filename):
    filepath = os.path.join(SOUNDS_DIR, filename)
    
    try:
        return pygame.mixer.Sound(filepath)
    except (pygame.error, FileNotFoundError):
        print(f"Warning: Could not load sound {filepath}")
        return pygame.mixer.Sound(buffer=bytearray(44))  # Silent sound


def create_spritesheet(surface, width, height, colorkey=None):
    """Slice a spritesheet into individual frames.
    
    Args:
        surface: The spritesheet surface
        width: The width of each frame
        height: The height of each frame
        colorkey: The color to use as transparent
        
    Returns:
        A list of surfaces, each containing one frame
    """
    frames = []
    
    # Get the dimensions of the spritesheet
    sheet_width, sheet_height = surface.get_size()
    
    # Calculate how many frames we can fit
    columns = sheet_width // width
    rows = sheet_height // height
    
    # Extract each frame
    for row in range(rows):
        for col in range(columns):
            # Create a new surface for the frame
            frame = pygame.Surface((width, height))
            
            # Set colorkey for transparency
            if colorkey is not None:
                frame.fill(colorkey)
                frame.set_colorkey(colorkey)
            
            # Copy the frame from the spritesheet
            frame.blit(surface, (0, 0), 
                      (col * width, row * height, width, height))
            
            frames.append(frame)
    
    return frames

def draw_text(surface, text, size, x, y, color=WHITE, align="center"):
    """Draw text on a surface.
    
    Args:
        surface: The surface to draw on
        text: The text to draw
        size: The font size
        x: The x coordinate
        y: The y coordinate
        color: The text color
        align: Text alignment ("left", "center", or "right")
    """
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    # Set position based on alignment
    if align == "left":
        text_rect.topleft = (x, y)
    elif align == "center":
        text_rect.midtop = (x, y)
    elif align == "right":
        text_rect.topright = (x, y)
    
    surface.blit(text_surface, text_rect)