# Import the pygame library
import pygame

# Initialize pygame - this must be done before using pygame functions
pygame.init()

# Set up the display window
# Creates a window that is 800 pixels wide and 600 pixels tall
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title that appears at the top
pygame.display.set_caption("Frogger Game")

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Define colors using RGB values (Red, Green, Blue) from 0-255
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
GREEN = (106, 153, 78)
DARK_GREEN = (56, 102, 65)
YELLOW = (255, 255, 0)
BRIGHT_YELLOW = (255, 255, 150)
RED = (188, 71, 73)
BLUE = (0, 100, 200)
PURPLE = (150, 0, 150)
ORANGE = (255, 140, 0)
BROWN = (139, 69, 19)
TAN = (242, 232, 207)
PINK = (255, 182, 193)

# Grid settings
grid_size = 50  # Each grid square is 50 pixels
rows = screen_height // grid_size  # Calculate number of rows (12 rows)
cols = screen_width // grid_size  # Calculate number of columns (16 columns)

# Player settings
player_row = 11  # Start at bottom row
player_col = 7   # Start near middle column (column 7 out of 0-15)
player_lives = 3  # Number of lives the player has
player_score = 0  # Player's score (increases when reaching goal)

# Game state
game_over = False  # Tracks if the game has ended
difficulty_multiplier = 1.0  # Multiplier for car speeds (increases with score)

# Car/obstacle settings
# Each lane is a dictionary containing lane info and list of cars
# The "base_speed" is the starting speed that gets multiplied by difficulty_multiplier
lanes = [
    # Row 2 - cars moving right
    {
        "row": 2,
        "direction": 1,  # 1 means moving right, -1 means moving left
        "base_speed": 2,  # Base speed before difficulty multiplier
        "color": RED,
        "cars": [
            {"x": 0, "width": 80},
            {"x": 250, "width": 80},
            {"x": 500, "width": 80}
        ]
    },
    # Row 3 - cars moving left
    {
        "row": 3,
        "direction": -1,
        "base_speed": 3,
        "color": BLUE,
        "cars": [
            {"x": 100, "width": 100},
            {"x": 400, "width": 100},
            {"x": 700, "width": 100}
        ]
    },
    # Row 4 - cars moving right
    {
        "row": 4,
        "direction": 1,
        "base_speed": 2.5,
        "color": PURPLE,
        "cars": [
            {"x": 150, "width": 90},
            {"x": 450, "width": 90}
        ]
    },
    # Row 6 - cars moving left
    {
        "row": 6,
        "direction": -1,
        "base_speed": 3.5,
        "color": ORANGE,
        "cars": [
            {"x": 50, "width": 70},
            {"x": 300, "width": 70},
            {"x": 550, "width": 70}
        ]
    },
    # Row 7 - cars moving right
    {
        "row": 7,
        "direction": 1,
        "base_speed": 2,
        "color": RED,
        "cars": [
            {"x": 200, "width": 85},
            {"x": 500, "width": 85}
        ]
    },
    # Row 8 - cars moving left
    {
        "row": 8,
        "direction": -1,
        "base_speed": 4,
        "color": BLUE,
        "cars": [
            {"x": 0, "width": 95},
            {"x": 350, "width": 95},
            {"x": 650, "width": 95}
        ]
    },
    # Row 9 - cars moving right
    {
        "row": 9,
        "direction": 1,
        "base_speed": 3,
        "color": PURPLE,
        "cars": [
            {"x": 100, "width": 75},
            {"x": 400, "width": 75},
            {"x": 700, "width": 75}
        ]
    }
]

# Game loop control variable
running = True

# Main game loop - this runs continuously until the game ends
while running:
    
    # Event handling - check for user input
    for event in pygame.event.get():
        # Check if user clicked the X button to close window
        if event.type == pygame.QUIT:
            running = False  # This will end the game loop
        
        # Check for keyboard presses (KEYDOWN means key was just pressed, not held)
        if event.type == pygame.KEYDOWN:
            # Only process movement if game is not over
            if not game_over:
                # Check which key was pressed and move accordingly
                if event.key == pygame.K_UP:
                    # Move up one row (decrease row number)
                    player_row = player_row - 1
                    # Keep player from going off top of screen
                    if player_row < 0:
                        player_row = 0
                
                elif event.key == pygame.K_DOWN:
                    # Move down one row (increase row number)
                    player_row = player_row + 1
                    # Keep player from going off bottom of screen
                    if player_row >= rows:
                        player_row = rows - 1
                
                elif event.key == pygame.K_LEFT:
                    # Move left one column (decrease column number)
                    player_col = player_col - 1
                    # Keep player from going off left edge
                    if player_col < 0:
                        player_col = 0
                
                elif event.key == pygame.K_RIGHT:
                    # Move right one column (increase column number)
                    player_col = player_col + 1
                    # Keep player from going off right edge
                    if player_col >= cols:
                        player_col = cols - 1
            
            # Allow restart when game is over
            else:
                # Press R to restart the game
                if event.key == pygame.K_r:
                    # Reset all game variables to starting values
                    game_over = False
                    player_lives = 3
                    player_score = 0
                    player_row = 11
                    player_col = 7
                    difficulty_multiplier = 1.0  # Reset difficulty
    
    # Only update game logic if game is not over
    if not game_over:
        # Check if player reached the goal (row 0)
        if player_row == 0:
            # Player reached the goal!
            player_score = player_score + 100  # Add 100 points to score
            
            # Increase difficulty every time player scores
            # Add 0.1 to the multiplier (10% speed increase)
            difficulty_multiplier = difficulty_multiplier + 0.1
            
            # Reset player to starting position
            player_row = 11
            player_col = 7
        
        # Update car positions - move all cars in all lanes
        for lane in lanes:
            # Loop through each car in this lane
            for car in lane["cars"]:
                # Calculate current speed using base_speed * difficulty_multiplier
                current_speed = lane["base_speed"] * difficulty_multiplier
                
                # Move car based on direction and current speed
                # direction is 1 (right) or -1 (left)
                car["x"] = car["x"] + (lane["direction"] * current_speed)
                
                # Wrap car around screen when it goes off edge
                if lane["direction"] == 1:  # Moving right
                    # If car goes completely off right side, wrap to left
                    if car["x"] > screen_width:
                        car["x"] = -car["width"]
                else:  # Moving left (direction == -1)
                    # If car goes completely off left side, wrap to right
                    if car["x"] + car["width"] < 0:
                        car["x"] = screen_width
        
        # Check for collisions between player and cars
        # Calculate player's pixel position and hitbox
        player_pixel_x = player_col * grid_size
        player_pixel_y = player_row * grid_size
        player_hitbox_width = grid_size
        player_hitbox_height = grid_size
        
        # Loop through all lanes to check for collisions
        for lane in lanes:
            # Only check collision if player is in this lane's row
            if player_row == lane["row"]:
                # Get car's y position in pixels
                car_y = lane["row"] * grid_size + 10
                car_height = 30
                
                # Check collision with each car in this lane
                for car in lane["cars"]:
                    car_x = car["x"]
                    car_width = car["width"]
                    
                    # Rectangle collision detection
                    # Check if rectangles overlap on both x and y axes
                    x_overlap = (player_pixel_x < car_x + car_width and 
                               player_pixel_x + player_hitbox_width > car_x)
                    y_overlap = (player_pixel_y < car_y + car_height and
                               player_pixel_y + player_hitbox_height > car_y)
                    
                    # If both x and y overlap, there's a collision
                    if x_overlap and y_overlap:
                        # Collision detected! Reset player and reduce lives
                        player_lives = player_lives - 1
                        
                        # Check if player has run out of lives
                        if player_lives <= 0:
                            game_over = True  # End the game
                        else:
                            # Reset player to starting position
                            player_row = 11
                            player_col = 7
                        
                        # Break out of car loop since we already hit something
                        break
    
    # Fill the screen with a background color
    screen.fill(BLACK)
    
    # Draw the lanes from top to bottom
    # Row 0 - Goal zone at the top (dark green)
    pygame.draw.rect(screen, DARK_GREEN, (0, 0, screen_width, grid_size))
    
    # Row 1 - Safe zone (green grass)
    pygame.draw.rect(screen, GREEN, (0, grid_size * 1, screen_width, grid_size))
    
    # Rows 2-4 - Road lanes (gray)
    pygame.draw.rect(screen, GRAY, (0, grid_size * 2, screen_width, grid_size))
    pygame.draw.rect(screen, GRAY, (0, grid_size * 3, screen_width, grid_size))
    pygame.draw.rect(screen, GRAY, (0, grid_size * 4, screen_width, grid_size))
    
    # Row 5 - Safe zone (green grass)
    pygame.draw.rect(screen, GREEN, (0, grid_size * 5, screen_width, grid_size))
    
    # Rows 6-9 - More road lanes (gray)
    pygame.draw.rect(screen, GRAY, (0, grid_size * 6, screen_width, grid_size))
    pygame.draw.rect(screen, GRAY, (0, grid_size * 7, screen_width, grid_size))
    pygame.draw.rect(screen, GRAY, (0, grid_size * 8, screen_width, grid_size))
    pygame.draw.rect(screen, GRAY, (0, grid_size * 9, screen_width, grid_size))
    
    # Row 10 - Safe zone (green grass)
    pygame.draw.rect(screen, GREEN, (0, grid_size * 10, screen_width, grid_size))
    
    # Row 11 - Start zone at the bottom (green grass)
    pygame.draw.rect(screen, GREEN, (0, grid_size * 11, screen_width, grid_size))
    
    # Draw grid lines to show the grid structure (optional - helps visualize)
    for row in range(rows + 1):
        # Draw horizontal line at each row boundary
        pygame.draw.line(screen, GRAY, (0, row * grid_size), (screen_width, row * grid_size), 1)
    
    for col in range(cols + 1):
        # Draw vertical line at each column boundary
        pygame.draw.line(screen, GRAY, (col * grid_size, 0), (col * grid_size, screen_height), 1)
    
    # Draw all cars
    for lane in lanes:
        # Get the y position for this lane (centered vertically in the row)
        car_y = lane["row"] * grid_size + 10  # 10 pixels from top of row
        car_height = 30  # Height of car rectangles
        
        # Draw each car in this lane
        for car in lane["cars"]:
            # Draw the main car body
            pygame.draw.rect(screen, lane["color"], 
                           (car["x"], car_y, car["width"], car_height))
            
            # Draw windows on the car (darker rectangle)
            window_color = (0, 0, 0)
            pygame.draw.rect(screen, window_color,
                           (car["x"] + 10, car_y + 5, car["width"] - 20, 10))
    
    # Convert player grid position to pixel position
    # Add grid_size // 2 to center the gnome in the grid square
    player_x = player_col * grid_size + grid_size // 2
    player_y = player_row * grid_size + grid_size // 2
    
    # Draw the gnome player
    # Gnome body - brown oval/ellipse
    body_width = 28
    body_height = 30
    pygame.draw.ellipse(screen, BROWN, 
                       (player_x - body_width // 2, 
                        player_y - 5, 
                        body_width, 
                        body_height))
    
    # Gnome head - tan/beige circle
    head_radius = 12
    pygame.draw.circle(screen, TAN, (player_x, player_y - 10), head_radius)
    
    # Gnome hat - red triangle/cone shape
    # Draw a polygon (triangle) for the pointy hat
    hat_points = [
        (player_x - 15, player_y - 10),  # Left base of hat
        (player_x + 15, player_y - 10),  # Right base of hat
        (player_x, player_y - 35)        # Top point of hat
    ]
    pygame.draw.polygon(screen, RED, hat_points)
    
    # Gnome nose - small pink circle
    pygame.draw.circle(screen, PINK, (player_x, player_y - 8), 3)
    
    # Gnome beard - white triangular shape
    beard_points = [
        (player_x - 10, player_y - 5),   # Left top of beard
        (player_x + 10, player_y - 5),   # Right top of beard
        (player_x, player_y + 8)         # Bottom point of beard
    ]
    pygame.draw.polygon(screen, WHITE, beard_points)
    
    # Create font for displaying text
    font = pygame.font.Font(None, 36)  # None uses default font, 36 is size
    
    # Draw lives display in top-left corner
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    
    # Draw score display in top-right corner
    score_text = font.render(f"Score: {player_score}", True, WHITE)
    # Get the width of the text to position it from the right edge
    score_text_width = score_text.get_width()
    screen.blit(score_text, (screen_width - score_text_width - 10, 10))
    
    # If game is over, display game over message
    if game_over:
        # Create larger font for game over message
        big_font = pygame.font.Font(None, 72)
        small_font = pygame.font.Font(None, 48)
        
        # Render "GAME OVER" text
        game_over_text = big_font.render("GAME OVER", True, RED)
        # Center the text horizontally and vertically
        text_x = (screen_width - game_over_text.get_width()) // 2
        text_y = (screen_height - game_over_text.get_height()) // 2 - 50
        screen.blit(game_over_text, (text_x, text_y))
        
        # Render final score text
        final_score_text = small_font.render(f"Final Score: {player_score}", True, WHITE)
        score_x = (screen_width - final_score_text.get_width()) // 2
        score_y = text_y + 80
        screen.blit(final_score_text, (score_x, score_y))
        
        # Render restart instruction text
        restart_text = small_font.render("Press R to Restart", True, WHITE)
        restart_x = (screen_width - restart_text.get_width()) // 2
        restart_y = score_y + 60
        screen.blit(restart_text, (restart_x, restart_y))
    
    # Update the display to show any changes
    pygame.display.flip()
    
    # Control frame rate - runs at 60 frames per second
    clock.tick(60)

# Clean up and close pygame properly
pygame.quit()
