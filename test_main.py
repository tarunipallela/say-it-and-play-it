import pygame
import sys
import threading
from test_voice import get_voice_command
import time

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voice Controlled Dino Game")
clock = pygame.time.Clock()
gravity = 0.5

# --- Dino setup ---
dino = pygame.Rect(100, HEIGHT - 60, 40, 40)
dino_y_vel = 0
on_ground = True

# --- Game variables ---
command = None
game_running = False
game_over = False
score = 0

# --- Functions ---
def jump():
    global dino_y_vel, on_ground
    if on_ground:
        dino_y_vel = -12
        on_ground = False

def reset_game():
    global dino, dino_y_vel, on_ground, score, game_running, game_over
    dino.y = HEIGHT - 60
    dino_y_vel = 0
    on_ground = True
    score = 0
    game_running = True
    game_over = False
    print("🔄 Game Restarted!")

def start_game():
    global game_running, score
    if not game_running:
        game_running = True
        score = 0
        print("🎮 Game Started!")

def exit_game():
    print("🚪 Exiting the game...")
    pygame.quit()
    sys.exit()

# --- Voice listener thread ---
def listen_voice():
    global command
    while True:
        cmd = get_voice_command()
        if cmd:
            command = cmd

voice_thread = threading.Thread(target=listen_voice, daemon=True)
voice_thread.start()

# --- Main loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()

    # Handle voice commands
    if command:
        if command == 'jump' and game_running and not game_over:
            jump()
        elif command == 'restart':
            reset_game()
        elif command == 'start':
            start_game()
        elif command == 'exit':
            exit_game()
        command = None

    # Game physics
    if game_running and not game_over:
        dino_y_vel += gravity
        dino.y += int(dino_y_vel)
        if dino.y >= HEIGHT - 60:
            dino.y = HEIGHT - 60
            dino_y_vel = 0
            on_ground = True

    # Draw
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 200, 0), dino)
    pygame.display.flip()
    clock.tick(60)
