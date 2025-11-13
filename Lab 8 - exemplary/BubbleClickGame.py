# TURNER_AddictiveGame.py — Bubbles (Target/Click)

"""This is a simple bubble game where the player needs to click on the bubbles to score points.
The game requires use of amouse or mousepad to click on the bubbles.
The player will lose 1 point for each bubble that expires. 
The game is timed and the player needs to score 20 points before the 40 second timer runs out to win the game."""

import pygame
import sys
import random
import math
import wave, struct
from pathlib import Path

# ---------- Config ----------
WIDTH, HEIGHT = 540, 720
FPS = 60

# Session Targets
TARGET_SCORE = 20
SESSION_SECONDS = 40       # session total time

# Colors
WHITE  = (255, 255, 255)
BLACK  = (15, 15, 20)
YELLOW = (250, 215, 80)
CYAN   = (120, 220, 255)
GREY   = (150, 160, 170)
GREEN  = (70, 210, 140)
RED    = (230, 80, 80)

# ---------- Bubble config (base) ----------
BUBBLE_MIN_RADIUS_BASE = 20
BUBBLE_MAX_RADIUS_BASE = 35
BUBBLE_LIFETIME_MS_BASE = 1300

# ---------- Ramp targets ----------
BUBBLE_MIN_RADIUS_END = 16
BUBBLE_MAX_RADIUS_END = 28
BUBBLE_LIFETIME_MS_END = 700

# Respawn gap (time after hit/expire before next bubble is allowed)
SPAWN_GAP_MS_BASE = 400          
SPAWN_GAP_MS_END  = 150

# ---------- Golden bubble config ----------
GOLD_CHANCE = 0.12        # chance that a bubble is golden
GOLD_SCORE  = 3           # +3 points if clicked
GOLD_COLOR  = (255, 225, 120)
GOLD_LIFETIME_FACTOR = 0.70  # golden bubbles live 70% of normal lifetime

# Golden movement (pixels/second)
GOLD_SPEED_MIN = 120
GOLD_SPEED_MAX = 220

# ---------- Pop effect config ----------
POPEFFECT_MS = 250
POPEFFECT_MAX_R_GROW = 24

# ---------- Sound ----------
ASSET_DIR = Path(__file__).parent
CHIME_WAV = ASSET_DIR / "chime.wav"

def generate_chime_if_needed(path: Path, frequency=880.0, duration_ms=140, volume=0.45, samplerate=44100):
    if path.exists():
        return
    nframes = int(samplerate * (duration_ms / 1000.0))
    amp = int(32767 * max(0.0, min(volume, 1.0)))
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        for i in range(nframes):
            t = i / samplerate
            fade = 1.0 - (i / nframes)
            sample = int(amp * fade * math.sin(2 * math.pi * frequency * t))
            wf.writeframes(struct.pack("<h", sample))

# ---------- Text Helpers ----------
def draw_text(surface, text, size, color, x, y, center=True, bold=True):
    font = pygame.font.SysFont("arial", size, bold=bold)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(surf, rect)

# ---------- Math Helpers ----------
def lerp(a, b, t):
    """Linear interpolation between a and b for t in [0,1]."""
    return a + (b - a) * max(0.0, min(1.0, t))

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# ---------- Bubble Object ----------
class Bubble:
    def __init__(self, width, height, min_r, max_r, lifetime_ms, color, value, vx=0.0, vy=0.0):
        self.radius = random.randint(int(min_r), int(max_r))
        margin = self.radius + 8
        self.x = random.randint(margin, width - margin)
        self.y = random.randint(100 + margin, height - margin)
        self.born_at = pygame.time.get_ticks()
        self.lifetime_ms = int(lifetime_ms)
        self.color = color
        self.value = int(value)
        self.vx = float(vx)
        self.vy = float(vy)

    def is_hit(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        return (dx * dx + dy * dy) <= (self.radius * self.radius)

    def is_expired(self, now_ms):
        return (now_ms - self.born_at) >= self.lifetime_ms

    def move_and_bounce(self, dt_ms, width, height):
        if self.vx == 0.0 and self.vy == 0.0:
            return  # stationary bubbles do not move
        dt = dt_ms / 1000.0
        self.x += self.vx * dt
        self.y += self.vy * dt

        margin = self.radius + 8
        left, right = margin, width - margin
        top, bottom = 100 + margin, height - margin  # keep out of HUD

        if self.x < left:
            self.x = left
            self.vx *= -1
        elif self.x > right:
            self.x = right
            self.vx *= -1

        if self.y < top:
            self.y = top
            self.vy *= -1
        elif self.y > bottom:
            self.y = bottom
            self.vy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius, width=3)
        highlight_r = max(3, self.radius // 4)
        pygame.draw.circle(
            surface, (200, 240, 255),
            (int(self.x) - self.radius // 3, int(self.y) - self.radius // 3),
            highlight_r, width=2
        )

# ---------- PopEffect Object ----------
class PopEffect:
    def __init__(self, x, y, base_radius, color):
        self.x = x
        self.y = y
        self.base_r = base_radius
        self.color = color
        self.born = pygame.time.get_ticks()

    def alive(self, now_ms):
        return (now_ms - self.born) < POPEFFECT_MS

    def draw(self, surface, now_ms):
        age = now_ms - self.born
        t = min(1.0, max(0.0, age / POPEFFECT_MS))
        r = int(self.base_r + t * POPEFFECT_MAX_R_GROW)
        alpha_outline = int(255 * (1.0 - t))
        alpha_fill = int(90 * (1.0 - t))
        ring = pygame.Surface((r * 2 + 6, r * 2 + 6), pygame.SRCALPHA)
        center = (r + 3, r + 3)
        pygame.draw.circle(ring, (*self.color, alpha_fill), center, max(1, r - 3))
        pygame.draw.circle(ring, (*self.color, alpha_outline), center, r, width=5)
        surface.blit(ring, (self.x - r - 3, self.y - r - 3))

def spawn_bubble(time_left, session_seconds):
    """Spawn a bubble whose size/lifetime are based on current difficulty; sometimes golden."""
    progress = 1.0 - clamp(time_left / float(session_seconds), 0.0, 1.0)
    min_r = lerp(BUBBLE_MIN_RADIUS_BASE, BUBBLE_MIN_RADIUS_END, progress)
    max_r = lerp(BUBBLE_MAX_RADIUS_BASE, BUBBLE_MAX_RADIUS_END, progress)
    lifetime_ms = lerp(BUBBLE_LIFETIME_MS_BASE, BUBBLE_LIFETIME_MS_END, progress)

    if random.random() < GOLD_CHANCE:
        color = GOLD_COLOR
        value = GOLD_SCORE
        lifetime_ms *= GOLD_LIFETIME_FACTOR
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(GOLD_SPEED_MIN, GOLD_SPEED_MAX)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
    else:
        color = CYAN
        value = 1
        vx = 0.0
        vy = 0.0

    return Bubble(WIDTH, HEIGHT, min_r, max_r, lifetime_ms, color, value, vx, vy)

def current_spawn_gap_ms(time_left, session_seconds):
    """Compute spawn gap ramp."""
    progress = 1.0 - clamp(time_left / float(session_seconds), 0.0, 1.0)
    return int(lerp(SPAWN_GAP_MS_BASE, SPAWN_GAP_MS_END, progress))

# ---------- Main ----------
def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bubbles — Target/Click")
    clock = pygame.time.Clock()

    generate_chime_if_needed(CHIME_WAV)
    chime = pygame.mixer.Sound(str(CHIME_WAV))

    mode = "START"  # START, PLAYING, PAUSED, GAME_OVER
    score = 0
    time_left = float(SESSION_SECONDS)
    won = False

    bubble = None
    next_spawn_at = 0
    effects = []

    running = True
    while running:
        dt_ms = clock.tick(FPS)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if mode == "START":
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    mode = "PLAYING"
                    score = 0
                    time_left = float(SESSION_SECONDS)
                    won = False
                    bubble = spawn_bubble(time_left, SESSION_SECONDS)
                    next_spawn_at = 0
                    effects = []

            elif mode == "PLAYING":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    mode = "PAUSED"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if bubble is not None and bubble.is_hit(event.pos):
                        score += bubble.value
                        chime.play()
                        effects.append(PopEffect(int(bubble.x), int(bubble.y), bubble.radius, bubble.color))
                        bubble = None
                        now = pygame.time.get_ticks()
                        next_spawn_at = now + current_spawn_gap_ms(time_left, SESSION_SECONDS)

            elif mode == "PAUSED":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    mode = "PLAYING"

            elif mode == "GAME_OVER":
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    mode = "START"

        # Update
        if mode == "PLAYING":
            now = pygame.time.get_ticks()

            time_left -= dt_ms / 1000.0
            if time_left < 0:
                time_left = 0

            if bubble is None and now >= next_spawn_at:
                bubble = spawn_bubble(time_left, SESSION_SECONDS)

            # Golden bubbles move; normal bubbles stay still
            if bubble is not None:
                bubble.move_and_bounce(dt_ms, WIDTH, HEIGHT)

            if bubble is not None and bubble.is_expired(now):
                score -= 1
                bubble = None
                next_spawn_at = now + current_spawn_gap_ms(time_left, SESSION_SECONDS)

            if score >= TARGET_SCORE:
                won = True
                mode = "GAME_OVER"
            elif time_left <= 0 and score < TARGET_SCORE:
                won = False
                mode = "GAME_OVER"

            effects = [e for e in effects if e.alive(now)]

        # Draw
        screen.fill(BLACK)

        if mode == "START":
            draw_text(screen, "BUBBLES", 56, CYAN, WIDTH // 2, 120)
            draw_text(screen, "How to Play", 28, WHITE, WIDTH // 2, 200)
            draw_text(screen, "Click bubbles to score points.", 22, WHITE, WIDTH // 2, 240)
            draw_text(screen, "Bubbles that expire cost -1 point.", 22, WHITE, WIDTH // 2, 270)
            draw_text(screen, f"Win by reaching {TARGET_SCORE} points", 22, WHITE, WIDTH // 2, 300)
            draw_text(screen, f"before the {SESSION_SECONDS}s timer ends.", 22, WHITE, WIDTH // 2, 330)
            draw_text(screen, "Press SPACE or ENTER to start", 22, GREEN, WIDTH // 2, 390)
            draw_text(screen, "Press P to pause anytime", 18, GREY, WIDTH // 2, 430)

        elif mode == "PLAYING":
            draw_text(screen, f"Score: {score}", 22, WHITE, 12, 10, center=False, bold=False)
            secs = max(0, int(math.ceil(time_left)))
            draw_text(screen, f"Time: {secs:02d}s", 22, WHITE, WIDTH - 120, 10, center=False, bold=False)

            if bubble is not None:
                bubble.draw(screen)

            now = pygame.time.get_ticks()
            for e in effects:
                e.draw(screen, now)

        elif mode == "PAUSED":
            draw_text(screen, f"Score: {score}", 22, WHITE, 12, 10, center=False, bold=False)
            secs = max(0, int(math.ceil(time_left)))
            draw_text(screen, f"Time: {secs:02d}s", 22, WHITE, WIDTH - 120, 10, center=False, bold=False)

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            draw_text(screen, "PAUSED", 48, YELLOW, WIDTH // 2, HEIGHT // 2 - 20)
            draw_text(screen, "Press P to resume", 22, WHITE, WIDTH // 2, HEIGHT // 2 + 25)

        elif mode == "GAME_OVER":
            title = "YOU WIN!" if won else "GAME OVER"
            color = GREEN if won else CYAN
            draw_text(screen, title, 48, color, WIDTH // 2, 160)
            draw_text(screen, f"Score: {score}", 26, WHITE, WIDTH // 2, 210)
            draw_text(screen, f"Target: {TARGET_SCORE}  |  Time: {SESSION_SECONDS}s", 22, GREY, WIDTH // 2, 250)
            draw_text(screen, "SPACE/ENTER: back to Start", 22, GREEN, WIDTH // 2, 320)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
