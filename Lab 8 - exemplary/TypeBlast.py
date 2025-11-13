import pygame
import sys
import random  # Import the random module for picking random words

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
DARK_BLUE = (30, 30, 60)      # Background color
ORANGE = (255, 200, 100)       # Color for player's typing
YELLOW = (255, 255, 0)         # Color for score

# Frame rate
FPS = 60

# Game settings
STARTING_FALL_SPEED = 1    # How fast words fall at the beginning
SPEED_INCREASE = 0.1       # How much faster words fall after each correct word
BOTTOM_LIMIT = 580    # If word reaches this Y position, player loses
TARGET_SCORE = 30      # Player wins if they reach this score

#Game States - diferent phases of the game
STATE_START = "start" #start screen with instructions
STATE_PLAYING = "playing" #active gameplay
STATE_GAME_OVER = "game_over" #game ended win/lose

# List of words the player might need to type
WORD_LIST = ["cat", "dog", "bird", "fish", "frog", "bear", "lion", "wolf", "tiger", "elephant", "giraffe", "zebra", "monkey", "snake", "turtle", "hippo", "rhino", "leopard", "cheetah", "panda", "koala", "polar bear", "grizzly bear", "penguin", "dolphin", "whale", "shark", "octopus", "squid", "lobster", "crab", "snail", "worm", "ant", "bee", "butterfly", "moth", "fly", "mosquito", "tick", "flea", "louse", "bedbug", "cockroach", "ant", "bee", "butterfly", "moth", "fly", "mosquito", "tick", "flea", "louse", "bedbug", "cockroach"]

# ========================================
# GAME SETUP - Initialize game components
# ========================================

# Set up the display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Type Blast")

# Set up the clock for controlling frame rate
clock = pygame.time.Clock()

# Set up fonts for text
game_font = pygame.font.Font(None, 48)        # Font for the falling word
input_font = pygame.font.Font(None, 36)       # Font for what player types
game_over_font = pygame.font.Font(None, 72)   # Big font for GAME OVER
score_font = pygame.font.Font(None, 36)       # Font for score display
win_font = pygame.font.Font(None, 72)         # Big font for YOU WIN
title_font = pygame.font.Font(None, 64)       # Font for title on start screen
instruction_font = pygame.font.Font(None, 32) # Font for instructions

# ========================================
# GAME VARIABLES - Store game state
# ========================================

# Pick a random word from the list to start
target_word = random.choice(WORD_LIST)

# Position of the falling word
word_x = 350  # Horizontal position
word_y = 20   # Vertical position

# What the player has typed so far
player_input = ""  # Starts as empty string

# Game state - what phase of the game we're in
game_state = STATE_START # Start with the start screen
paused = False # Tracks if game is paused

# Game variables
score = 0          # Player's score, starts at zero
player_won = False  # Tracks if the player has won
word_fall_speed = STARTING_FALL_SPEED  # Current fall speed (starts at 1, increases over time)

# ========================================
# GAME FUNCTIONS - Helper functions
# ========================================

# We'll add functions here later

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
        
        # Handle key presses
        if event.type == pygame.KEYDOWN:
            
            # START SCREEN - Press SPACE to begin
            if game_state == STATE_START:
                if event.key == pygame.K_SPACE:
                    # Start the game!
                    game_state = STATE_PLAYING
            
            # PLAYING - Handle gameplay keys
            elif game_state == STATE_PLAYING:
                # Press P to pause/unpause
                if event.key == pygame.K_1:
                    paused = not paused  # Toggle pause (if True becomes False, if False becomes True)
                
                # Only process typing if not paused
                elif not paused:
                    # Check if the key was backspace
                    if event.key == pygame.K_BACKSPACE:
                        # Remove the last character from player_input
                        player_input = player_input[:-1]
                    else:
                        # Add the typed character to player_input
                        player_input = player_input + event.unicode
    
    
    # ----------------------------------------
    # 2. GAME LOGIC
    # ----------------------------------------
    # Update game state (move objects, check collisions, update scores)
    
   # Only update game if we're playing AND not paused
    if game_state == STATE_PLAYING and not paused:
        # Make the word fall down using current speed
        word_y = word_y + word_fall_speed
        
        # Check if word reached the bottom of the screen
        if word_y >= BOTTOM_LIMIT:
            # Player loses! Word reached the bottom
            game_state = STATE_GAME_OVER  # Change to game over state
            player_won = False # Player lost
        
        # Check if player typed the correct word
        if player_input == target_word:
            # Success! The player typed the correct word
            
            # Add 1 point to the score
            score = score + 1
            
            # Increase the fall speed to make it harder!
            word_fall_speed = word_fall_speed + SPEED_INCREASE
            
            # Check if player reached the target score (WIN CONDITION!)
            if score >= TARGET_SCORE:
                # Player wins!
                game_state = STATE_GAME_OVER  # Change to game over state
                player_won = True # Player won!
            else:
                # Haven't won yet, keep playing
                
                # Pick a new random word from the list
                target_word = random.choice(WORD_LIST)
                
                # Reset the word to the top of the screen
                word_y = 20
                
                # Clear the player's input so they can type again
                player_input = ""
    
    
    # ----------------------------------------
    # 3. DRAWING
    # ----------------------------------------
    # Render everything to the screen
    
    # Clear the screen with background color
    screen.fill(DARK_BLUE)
    
    # ===== START SCREEN =====
    if game_state == STATE_START:
        # Draw title
        title_surface = title_font.render("TYPING GAME", True, YELLOW)
        title_width = title_surface.get_width()
        title_x = (SCREEN_WIDTH - title_width) / 2
        screen.blit(title_surface, (title_x, 100))
        
        # Draw instructions
        instructions = [
            "Type the falling words before they reach the bottom!",
            "",
            "Get " + str(TARGET_SCORE) + " words correct to win.",
            "",
            "Press 1 to pause during the game.",
            "",
            "Press SPACE to start!"
        ]
        
        # Draw each instruction line
        y_position = 220  # Starting Y position for instructions
        for line in instructions:
            instruction_surface = instruction_font.render(line, True, WHITE)
            instruction_width = instruction_surface.get_width()
            instruction_x = (SCREEN_WIDTH - instruction_width) / 2
            screen.blit(instruction_surface, (instruction_x, y_position))
            y_position = y_position + 40  # Move down for next line
    
    # ===== PLAYING =====
    elif game_state == STATE_PLAYING:
        # Draw falling word
        word_surface = game_font.render(target_word, True, WHITE)
        screen.blit(word_surface, (word_x, word_y))
        
        # Draw what the player has typed
        input_surface = input_font.render(player_input, True, ORANGE)
        screen.blit(input_surface, (350, 550))
        
        # Draw score
        score_text = "Score: " + str(score) + " / " + str(TARGET_SCORE)
        score_surface = score_font.render(score_text, True, YELLOW)
        screen.blit(score_surface, (10, 10))
        
        # If paused, show PAUSED message
        if paused:
            # Semi-transparent overlay effect (we'll just show text for now)
            paused_surface = game_over_font.render("PAUSED", True, YELLOW)
            paused_width = paused_surface.get_width()
            paused_x = (SCREEN_WIDTH - paused_width) / 2
            screen.blit(paused_surface, (paused_x, 250))
            
            # Show unpause instruction
            unpause_surface = instruction_font.render("Press 1 to continue", True, WHITE)
            unpause_width = unpause_surface.get_width()
            unpause_x = (SCREEN_WIDTH - unpause_width) / 2
            screen.blit(unpause_surface, (unpause_x, 350))
    
    # ===== GAME OVER =====
    elif game_state == STATE_GAME_OVER:
        # Check if player won or lost
        if player_won:
            # Player won! Show victory message
            win_surface = win_font.render("YOU WIN!", True, GREEN)
            text_width = win_surface.get_width()
            text_x = (SCREEN_WIDTH - text_width) / 2
            screen.blit(win_surface, (text_x, 250))
        else:
            # Player lost! Show game over message
            game_over_surface = game_over_font.render("GAME OVER", True, RED)
            text_width = game_over_surface.get_width()
            text_x = (SCREEN_WIDTH - text_width) / 2
            screen.blit(game_over_surface, (text_x, 250))
        
        # Show final score
        final_score_text = "Final Score: " + str(score)
        final_score_surface = score_font.render(final_score_text, True, WHITE)
        final_score_width = final_score_surface.get_width()
        final_score_x = (SCREEN_WIDTH - final_score_width) / 2
        screen.blit(final_score_surface, (final_score_x, 350))
    
    # Update the display to show everything we drew
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