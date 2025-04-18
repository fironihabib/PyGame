import pygame
import sys
from settings import *
from game import Game

# Initialize pygame
pygame.init()
pygame.mixer.init()  # For sound effects
pygame.display.set_caption("Pixel Platformer")

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create game instance
game = Game()

# Main game loop
def main():
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        # Update game state
        game.update()
        
        # Draw everything
        screen.fill(BG_COLOR)
        game.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()