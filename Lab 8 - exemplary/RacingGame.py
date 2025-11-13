import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display window (3 lanes)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrolling Road Game")

# Set up the clock for frame rate
clock = pygame.time.Clock()

# Colors
DARK_GRAY = (55, 55, 55)
GRAY = (90, 90, 90)
WHITE = (230, 230, 230)
YELLOW = (220, 220, 80)
RED = (180, 50, 50)
DARK_BLUE = (50, 80, 140)
GREEN = (70, 130, 70)
BRIGHT_GREEN = (100, 200, 100)  # For collectibles

# Car properties
car_width = 50
car_height = 70
car_x = 0  # Will be set after road centering
car_y = screen_height - 150  # Near bottom of screen
car_speed = 6 # Car speed

# Road properties
road_width = 400
road_left = (screen_width - road_width) // 2  # Center the road
road_right = road_left + road_width

# Lane positions (x-coordinates for center of each lane)
lane_width = road_width // 3
lane_1_x = road_left + lane_width // 2
lane_2_x = road_left + lane_width + lane_width // 2
lane_3_x = road_left + lane_width * 2 + lane_width // 2

# Set player car to start in middle lane
car_x = lane_2_x - car_width // 2

# Road line properties for dashed lines
line_width = 8
line_height = 50
line_gap = 50  # Gap between dashed lines
total_line_segment = line_height + line_gap
scroll_speed = 7

# Create lane lines with proper initial spacing
num_segments = (screen_height // total_line_segment) + 2

# Left divider lines
left_divider_lines = []
for i in range(num_segments):
    left_divider_lines.append(i * total_line_segment)

# Right divider lines
right_divider_lines = []
for i in range(num_segments):
    right_divider_lines.append(i * total_line_segment)

# Obstacle car properties
obstacle_cars = []
obstacle_speed = 7
spawn_timer = 0
spawn_delay = 60  # Frames between spawning new obstacles

# Collectible properties
collectibles = []  # List to store collectibles
collectible_width = 20
collectible_height = 20
collectible_speed = 7
collectible_spawn_timer = 0
min_collectible_spawn_delay = 2 * 60  # 2 seconds at 60 FPS
max_collectible_spawn_delay = 5 * 60  # 5 seconds at 60 FPS
current_collectible_spawn_delay = random.randint(min_collectible_spawn_delay, max_collectible_spawn_delay)
points_per_collectible = 0 # Adjustable points for collectibles

# POINT SYSTEM
score = 0
score_timer = 0
points_per_second = 1
frames_per_score = 60

# FUEL SYSTEM
max_fuel = 100
fuel = max_fuel
fuel_drain_rate = 0.06  # Fuel lost per frame (adjustable for difficulty)
fuel_per_collectible = 20  # Fuel gained from each gas can
fuel_fill_active = False  # Is fuel currently filling?
fuel_fill_amount = 0  # Amount of fuel to fill
fuel_fill_rate = 1.0  # How fast the fuel fills per frame

# Game state
game_started = False
game_over = False
waiting_for_restart = False
game_over_reason = ""  # Track why game ended

# Function to reset the game
def reset_game():
    global car_x, car_y, obstacle_cars, collectibles, game_over, waiting_for_restart, spawn_timer, score, score_timer, collectible_spawn_timer, current_collectible_spawn_delay, fuel, game_over_reason
    car_x = lane_2_x - car_width // 2
    car_y = screen_height - 150
    obstacle_cars = []
    collectibles = []  # Reset collectibles
    game_over = False
    waiting_for_restart = False
    spawn_timer = 0
    score = 0
    score_timer = 0
    collectible_spawn_timer = 0  # Reset collectible timer
    current_collectible_spawn_delay = random.randint(min_collectible_spawn_delay, max_collectible_spawn_delay)  # Reset random delay
    fuel = max_fuel  # Reset fuel
    game_over_reason = ""  # Reset reason

# Function to spawn a new obstacle car
def spawn_obstacle():
    lane_choice = random.choice([lane_1_x, lane_2_x, lane_3_x])
    obstacle = [lane_choice - car_width // 2, -car_height - 20, car_width, car_height]
    obstacle_cars.append(obstacle)

# Function to spawn a new collectible
def spawn_collectible():
    lane_choice = random.choice([lane_1_x, lane_2_x, lane_3_x])
    collectible = [lane_choice - collectible_width // 2, -collectible_height - 20, collectible_width, collectible_height]
    collectibles.append(collectible)

# Function to check collision between two rectangles
def check_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
        return True
    return False

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if not game_started and not game_over:
                # Start the game on any key press from start screen
                game_started = True
            elif waiting_for_restart:
                if event.key == pygame.K_y:
                    reset_game()
                    game_started = True
                elif event.key == pygame.K_n:
                    running = False
    
    if game_started and not game_over:
        # Get keyboard input for car movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x -= car_speed
        if keys[pygame.K_RIGHT]:
            car_x += car_speed
        if keys[pygame.K_UP]:
            car_y -= car_speed
        if keys[pygame.K_DOWN]:
            car_y += car_speed
        
        # Keep car within road boundaries
        if car_x < road_left:
            car_x = road_left
        if car_x > road_right - car_width:
            car_x = road_right - car_width
        if car_y < 0:
            car_y = 0
        if car_y > screen_height - car_height:
            car_y = screen_height - car_height
        
        # Update divider lines
        for i in range(len(left_divider_lines)):
            left_divider_lines[i] += scroll_speed
            if left_divider_lines[i] > screen_height:
                min_y = min(left_divider_lines)
                left_divider_lines[i] = min_y - total_line_segment
        
        for i in range(len(right_divider_lines)):
            right_divider_lines[i] += scroll_speed
            if right_divider_lines[i] > screen_height:
                min_y = min(right_divider_lines)
                right_divider_lines[i] = min_y - total_line_segment
        
        # Spawn new obstacle cars
        spawn_timer += 1
        if spawn_timer > spawn_delay:
            spawn_obstacle()
            spawn_timer = 0
        
        # Spawn new collectibles
        collectible_spawn_timer += 1
        if collectible_spawn_timer > current_collectible_spawn_delay:
            spawn_collectible()
            collectible_spawn_timer = 0
            current_collectible_spawn_delay = random.randint(min_collectible_spawn_delay, max_collectible_spawn_delay)
        
        # Update score based on time
        score_timer += 1
        if score_timer >= frames_per_score:
            score += points_per_second
            score_timer = 0

        
        # Drain fuel
        fuel -= fuel_drain_rate
        if fuel <= 0:
            fuel = 0
            game_over = True
            game_over_reason = "fuel"
            waiting_for_restart = True
        
        # Update obstacle car positions
        cars_to_remove = []
        for i, obstacle in enumerate(obstacle_cars):
            obstacle[1] += obstacle_speed
            if obstacle[1] > screen_height:
                cars_to_remove.append(i)
        
        for i in reversed(cars_to_remove):
            del obstacle_cars[i]
        
        # Update collectible positions and check for collection
        collectibles_to_remove = []
        for i, collectible in enumerate(collectibles):
            collectible[1] += collectible_speed
            # Check for collision with player
            if check_collision(car_x, car_y, car_width, car_height, 
                             collectible[0], collectible[1], collectible[2], collectible[3]):
                score += points_per_collectible
                fuel += fuel_per_collectible
                if fuel > max_fuel:
                    fuel = max_fuel
                collectibles_to_remove.append(i)
            # Remove if off-screen
            elif collectible[1] > screen_height:
                collectibles_to_remove.append(i)
        
        for i in reversed(collectibles_to_remove):
            del collectibles[i]
        
        # Check for collisions with obstacle cars
        for obstacle in obstacle_cars:
            if check_collision(car_x, car_y, car_width, car_height, 
                             obstacle[0], obstacle[1], obstacle[2], obstacle[3]):
                game_over = True
                game_over_reason = "crash"
                waiting_for_restart = True
    
    # Draw everything
    screen.fill(GREEN)
    
    # Draw start screen
    if not game_started and not game_over:
        # Draw a static road in the background
        pygame.draw.rect(screen, DARK_GRAY, (road_left, 0, road_width, screen_height))
        pygame.draw.rect(screen, WHITE, (road_left, 0, 6, screen_height))
        pygame.draw.rect(screen, WHITE, (road_right - 6, 0, 6, screen_height))
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw title
        font_title = pygame.font.Font(None, 84)
        title_text = font_title.render("ROAD RUNNER", True, YELLOW)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 140))
        screen.blit(title_text, title_rect)
        
        # Draw instructions
        font_instructions = pygame.font.Font(None, 42)
        
        instruction1 = font_instructions.render("AVOID THE CARS!", True, WHITE)
        instruction1_rect = instruction1.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
        screen.blit(instruction1, instruction1_rect)
        
        instruction2 = font_instructions.render("Collect green gas cans to stay alive!", True, BRIGHT_GREEN)
        instruction2_rect = instruction2.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
        screen.blit(instruction2, instruction2_rect)
        
        instruction4 = font_instructions.render("Arrow keys to move", True, WHITE)
        instruction4_rect = instruction4.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(instruction4, instruction4_rect)
        
        # Draw press any key message
        font_small = pygame.font.Font(None, 32)
        press_text = font_small.render("Press any key to start", True, YELLOW)
        press_rect = press_text.get_rect(center=(screen_width // 2, screen_height // 2 + 160))
        screen.blit(press_text, press_rect)
    
    else:
        # Draw game screen
        pygame.draw.rect(screen, DARK_GRAY, (road_left, 0, road_width, screen_height))
        
        # Draw lane dividers
        divider_1_x = road_left + lane_width
        for line_y in left_divider_lines:
            if -line_height <= line_y <= screen_height:
                pygame.draw.rect(screen, YELLOW, (divider_1_x - line_width // 2, line_y, line_width, line_height))
        
        divider_2_x = road_left + lane_width * 2
        for line_y in right_divider_lines:
            if -line_height <= line_y <= screen_height:
                pygame.draw.rect(screen, YELLOW, (divider_2_x - line_width // 2, line_y, line_width, line_height))
        
        # Draw edge lines
        pygame.draw.rect(screen, WHITE, (road_left, 0, 6, screen_height))
        pygame.draw.rect(screen, WHITE, (road_right - 6, 0, 6, screen_height))
        
        # Draw obstacle cars
        for obstacle in obstacle_cars:
            pygame.draw.rect(screen, DARK_BLUE, (obstacle[0], obstacle[1], obstacle[2], obstacle[3]))
            pygame.draw.rect(screen, (70, 90, 120), (obstacle[0] + 10, obstacle[1] + 15, obstacle[2] - 20, 20))
        
        # Draw collectibles
        for collectible in collectibles:
            pygame.draw.rect(screen, BRIGHT_GREEN, (collectible[0], collectible[1], collectible[2], collectible[3]))
        
        # Draw player car
        pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))
        pygame.draw.rect(screen, (180, 80, 80), (car_x + 10, car_y + 15, car_width - 20, 20))
        
        # Draw score
        font_score = pygame.font.Font(None, 48)
        score_text = font_score.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        # Draw fuel gauge
        gauge_x = screen_width - 220
        gauge_y = 20
        gauge_width = 200
        gauge_height = 30
        
        # Gauge background (empty)
        pygame.draw.rect(screen, DARK_GRAY, (gauge_x, gauge_y, gauge_width, gauge_height))
        
        # Gauge fill (fuel level)
        fuel_percentage = fuel / max_fuel
        fill_width = int(gauge_width * fuel_percentage)
        
        # Color changes based on fuel level
        if fuel_percentage > 0.5:
            fuel_color = BRIGHT_GREEN
        elif fuel_percentage > 0.25:
            fuel_color = YELLOW
        else:
            fuel_color = RED
        
        pygame.draw.rect(screen, fuel_color, (gauge_x, gauge_y, fill_width, gauge_height))
        
        # Gauge border
        pygame.draw.rect(screen, WHITE, (gauge_x, gauge_y, gauge_width, gauge_height), 3)
        
        # Fuel label
        font_fuel = pygame.font.Font(None, 28)
        fuel_text = font_fuel.render("FUEL", True, WHITE)
        screen.blit(fuel_text, (gauge_x + 5, gauge_y + 5))
        
        # Draw game over message
        if game_over and waiting_for_restart:
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            font_large = pygame.font.Font(None, 74)
            text = font_large.render("GAME OVER", True, WHITE)
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 120))
            screen.blit(text, text_rect)
            
            # Display specific reason for game over
            font_reason = pygame.font.Font(None, 52)
            if game_over_reason == "crash":
                reason_text = font_reason.render("You crashed!", True, RED)
            elif game_over_reason == "fuel":
                reason_text = font_reason.render("You ran out of fuel!", True, YELLOW)
            else:
                reason_text = font_reason.render("", True, WHITE)
            reason_rect = reason_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            screen.blit(reason_text, reason_rect)
            
            font_score_final = pygame.font.Font(None, 52)
            final_score_text = font_score_final.render(f"Final Score: {score}", True, YELLOW)
            final_score_rect = final_score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
            screen.blit(final_score_text, final_score_rect)
            
            font_small = pygame.font.Font(None, 36)
            restart_text = font_small.render("Restart? Y/N", True, WHITE)
            restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 90))
            screen.blit(restart_text, restart_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()