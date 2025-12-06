import pygame
import sys
from test_voice import VoiceListener

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voice Controlled Dino Game with Obstacles")
clock = pygame.time.Clock()
gravity = 0.5

# --- LOAD ASSETS ---
dino_img = pygame.image.load("assets/DinoStart.png").convert_alpha()
dino_img = pygame.transform.scale(dino_img, (60, 60))
cactus_img = pygame.image.load("assets/SmallCactus1.png").convert_alpha()
cactus_img = pygame.transform.scale(cactus_img, (30, 50))

# --- GAME VARIABLES ---
dino = pygame.Rect(100, HEIGHT - 80, 60, 60)
dino_y_vel = 0
on_ground = True

obstacle_width, obstacle_height = 30, 50
obstacles = []
obstacle_spawn_delay = 2500  # milliseconds
last_spawn_time = pygame.time.get_ticks()

game_started = False
game_over = False
score = 0
font = pygame.font.SysFont(None, 36)

# --- FUNCTIONS ---
def jump():
    global dino_y_vel, on_ground
    if on_ground and not game_over:
        dino_y_vel = -13
        on_ground = False

def reset_game():
    """Restart game state completely."""
    global obstacles, game_over, dino_y_vel, dino, score, on_ground, last_spawn_time, game_started
    obstacles.clear()
    game_over = False
    dino.y = HEIGHT - 80
    dino_y_vel = 0
    on_ground = True
    score = 0
    last_spawn_time = pygame.time.get_ticks()
    game_started = True
    print("🔄 Game Reset!")

# --- VOICE LISTENER ---
voice_listener = VoiceListener()
voice_listener.start()

# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            voice_listener.stop()
            pygame.quit()
            sys.exit()

    cmd = voice_listener.get_command()

    # --- VOICE COMMAND LOGIC ---
    if cmd == 'start':
        game_started = True
        game_over = False
        print("🎮 Game Started!")
    elif cmd == 'jump' and game_started and not game_over:
        jump()
    elif cmd == 'reset':
        reset_game()
    elif cmd == 'exit':
        print("🚪 Exiting the game...")
        voice_listener.stop()
        pygame.quit()
        sys.exit()

    # --- GAMEPLAY LOGIC ---
    if game_started and not game_over:
        current_time = pygame.time.get_ticks()

        # Spawn obstacles
        if current_time - last_spawn_time > obstacle_spawn_delay:
            obstacles.append(pygame.Rect(WIDTH, HEIGHT - 80, obstacle_width, obstacle_height))
            last_spawn_time = current_time

        # Move obstacles
        for obs in obstacles:
            obs.x -= 7
        obstacles = [obs for obs in obstacles if obs.x + obstacle_width > 0]

        # Jump & gravity
        dino_y_vel += gravity
        dino.y += int(dino_y_vel)
        if dino.y >= HEIGHT - 80:
            dino.y = HEIGHT - 80
            dino_y_vel = 0
            on_ground = True

        # Collision detection
        for obs in obstacles:
            if dino.colliderect(obs):
                game_over = True
                break

        score += 1

    # --- DRAWING SECTION ---
    screen.fill((255, 255, 255))  # white background

    if not game_started:
        # Waiting screen before saying "start"
        title_font = pygame.font.SysFont(None, 48)
        text = title_font.render("Say 'Start' to Begin the Game", True, (50, 50, 50))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    elif game_over:
        over_text = font.render("Game Over! Say 'Reset' or 'Exit'", True, (255, 0, 0))
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 30))
    else:
        # Draw dino and obstacles
        screen.blit(dino_img, (dino.x, dino.y))


        for obs in obstacles:
            screen.blit(cactus_img, (obs.x, obs.y))

        # Draw score
        score_text = font.render(f"Score: {score}", True, (50, 50, 50))
        screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

