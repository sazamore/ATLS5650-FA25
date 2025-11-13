# I M P O R T S
import pygame
import random
import math

# B A S I C  C O N F I G
WIDTH, HEIGHT = 800, 600
FPS = 60

BG_COLOR      = (24, 24, 32)     # background
CIRCLE_COLOR  = (230, 200, 80)   # normal circles
TARGET_COLOR  = (100, 255, 150)  # the one you MUST click
HEART_COLOR   = (255, 100, 100)  # lives indicator
DEAD_HEART    = (60, 60, 70)     # lost lives

TARGET_RADIUS = 40
LUCKY_RADIUS  = 60               # bigger target on lucky stages
NONOVERLAP_MARGIN = 4            # spacing to avoid overlaps

# T I M E R
START_TIME_S = 10.0
BONUS_TIME_PER_STAGE = 0.75       # time added for every accurate click

# L I V E S
MAX_LIVES = 3

# H E L P E R S

def rand_pos():
    """Return a random (x,y) fully on-screen for one circle."""
    x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
    y = random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS)
    return x, y

def non_overlapping_position(existing, attempts=200):
    """Find a non-overlapping (x,y) given existing circle centers."""
    min_dist = 2 * TARGET_RADIUS + NONOVERLAP_MARGIN
    min_d2   = min_dist * min_dist
    for _ in range(attempts):
        x, y = rand_pos()
        ok = True
        for (ox, oy) in existing:
            dx, dy = x - ox, y - oy
            if dx*dx + dy*dy < min_d2:
                ok = False
                break
        if ok:
            return x, y
    return rand_pos()

def build_stage(n):
    """
    Build a stage with n circles:
      - positions: list of (x,y)
      - target_index: index of the one that must be clicked
    """
    positions = []
    for _ in range(n):
        positions.append(non_overlapping_position(positions))
    target_index = random.randrange(n)
    return positions, target_index

def is_lucky_stage():
    """20% chance for a lucky stage with bigger target."""
    return random.random() < 0.2

def is_milestone(stage):
    """Check if stage is a milestone (5, 10, 25, 50, 100, etc.)."""
    milestones = [5, 10, 25, 50, 100, 200, 500]
    return stage in milestones

def hit_index(mx, my, positions, radius):
    """Return the index of the circle under (mx,my), or -1 if none."""
    r2 = radius * radius
    for i, (cx, cy) in enumerate(positions):
        dx, dy = mx - cx, my - cy
        if dx*dx + dy*dy <= r2:
            return i
    return -1

# P Y G A M E  S E T U P
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("One-Right-Circle — Stage Mode")
clock = pygame.time.Clock()

font      = pygame.font.Font(None, 48)
smallfont = pygame.font.Font(None, 32)

# G A M E  S T A T E
running = True
game_over = False

stage = 1                              # shows the number of circles
positions, target_idx = build_stage(stage)
lucky = is_lucky_stage()               # is current stage lucky?
current_radius = LUCKY_RADIUS if lucky else TARGET_RADIUS

lives = MAX_LIVES                      # player starts with 3 lives
milestone_flash = 0                    # countdown timer for milestone celebration

time_left_s = START_TIME_S
last_ms = pygame.time.get_ticks()


# M A I N  L O O P
while running:
    # Timer updated
    now = pygame.time.get_ticks()
    dt = (now - last_ms) / 1000.0
    last_ms = now

    if not game_over:
        time_left_s -= dt
        if time_left_s <= 0:
            time_left_s = 0
            game_over = True

    # Count down milestone flash effect
    if milestone_flash > 0:
        milestone_flash -= 1

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = pygame.mouse.get_pos()
            idx = hit_index(mx, my, positions, current_radius)

            if idx == -1 or idx != target_idx:
                # Wrong click or miss - lose a life
                lives -= 1
                if lives <= 0:
                    game_over = True
            else:
                # Correct click - advance stage
                time_left_s += BONUS_TIME_PER_STAGE
                stage += 1
                
                # Check for milestone celebration
                if is_milestone(stage):
                    milestone_flash = 60  # Flash for 60 frames (1 second)
                    print(f"★★★ MILESTONE: Stage {stage}! ★★★")
                
                # Build next stage and check if lucky
                positions, target_idx = build_stage(stage)
                lucky = is_lucky_stage()
                current_radius = LUCKY_RADIUS if lucky else TARGET_RADIUS

    # Draw
    screen.fill(BG_COLOR)

    if not game_over:
        # Draw all circles
        for i, (cx, cy) in enumerate(positions):
            color = TARGET_COLOR if i == target_idx else CIRCLE_COLOR
            pygame.draw.circle(screen, color, (cx, cy), current_radius)
    else:
        # Gray out circles on game over
        for (cx, cy) in positions:
            pygame.draw.circle(screen, (80,80,90), (cx, cy), current_radius)

    # Draw milestone celebration flash
    if milestone_flash > 0:
        # Pulsing overlay effect for milestone
        alpha = int(100 * (milestone_flash / 60.0))  # Fade out over time
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 215, 0, alpha))  # Gold color
        screen.blit(overlay, (0, 0))
        
        # Display milestone text
        milestone_txt = font.render(f"★ STAGE {stage} ★", True, (255, 255, 255))
        screen.blit(milestone_txt, (WIDTH//2 - milestone_txt.get_width()//2, HEIGHT//2 - 30))

    # HUD - Time
    time_txt = font.render(f"Time: {time_left_s:4.1f}s", True, (210, 220, 255))
    stage_txt = smallfont.render(f"Stage: {stage}", True, (210, 220, 240))
    screen.blit(time_txt, (16, 12))
    screen.blit(stage_txt, (16, 12 + time_txt.get_height() + 6))

    # HUD - Lives (hearts in top right)
    heart_size = 12  # Radius of heart circles
    heart_spacing = 30
    heart_start_x = WIDTH - 120
    heart_y = 30
    for i in range(MAX_LIVES):
        color = HEART_COLOR if i < lives else DEAD_HEART
        pygame.draw.circle(screen, color, (heart_start_x + i * heart_spacing, heart_y), heart_size)

    # HUD - Lucky stage indicator
    if lucky and not game_over:
        lucky_txt = smallfont.render("LUCKY! (Bigger target)", True, (255, 215, 0))
        screen.blit(lucky_txt, (WIDTH//2 - lucky_txt.get_width()//2, 16))

    if not game_over:
        tip = smallfont.render("Click the GREEN circle. Wrong clicks lose a life.", True, (170, 180, 200))
        screen.blit(tip, (16, HEIGHT - 36))
    else:
        # Game over overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))
        over = font.render("GAME OVER", True, (255, 220, 220))
        final = smallfont.render(f"Final Stage: {stage}", True, (200, 200, 200))
        screen.blit(over, (WIDTH//2 - over.get_width()//2, HEIGHT//2 - 40))
        screen.blit(final, (WIDTH//2 - final.get_width()//2, HEIGHT//2 + 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()