import pygame
import sys

# Initialize Pygame
pygame.init()

# ========================================
# CONSTANTS - Define once, use everywhere
# ========================================

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB format: Red, Green, Blue)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Frame rate
FPS = 60

# ========================================
# GAME SETUP - Initialize game components
# ========================================

# Set up the display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Simple Game")

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()

# ========================================
# GAME VARIABLES - Store game state
# ========================================

# Add your game variables here (positions, scores, etc.)


# ========================================
# GAME CLASSES - Define game objects
# ========================================

# Add your classes here (Player, Enemy, Item, etc.)


# ========================================
# GAME FUNCTIONS - Helper functions
# ========================================

# Add your functions here (collision detection, score updates, etc.)


# ========================================
# MAIN GAME LOOP
# ========================================

running = True
while running:
    
    # ----------------------------------------
    # 1. EVENT HANDLING
    # ----------------------------------------
    # Process user inputs (keyboard, mouse, window events)
    
    for event in pygame.event.get():
        # Check if user wants to quit
        if event.type == pygame.QUIT:
            running = False
        
        # Handle other events here (key presses, mouse clicks, etc.)
    
    
    # ----------------------------------------
    # 2. GAME LOGIC
    # ----------------------------------------
    # Update game state (move objects, check collisions, update scores)
    
    # Add your game logic here
    
    
    # ----------------------------------------
    # 3. DRAWING
    # ----------------------------------------
    # Render everything to the screen
    
    # Clear the screen
    screen.fill(WHITE)
    
    # Draw your game objects here
    
    # Update the display
    pygame.display.flip()
    
    
    # ----------------------------------------
    # 4. FRAME RATE
    # ----------------------------------------
    # Control how fast the game runs
    clock.tick(FPS)


# ========================================
# CLEANUP - End the game properly
# ========================================
pygame.quit()
sys.exit()
