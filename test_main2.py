import pygame
import sys
import random
from test_voice import VoiceListener

pygame.init()

# ================= WINDOW =================
WIDTH, HEIGHT = 900, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Say It & Play It")
clock = pygame.time.Clock()

# ================= COLORS =================
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (90,90,90)
BLUE = (40,120,255)
RED = (220,60,60)

# ================= GAME CONFIG =================
GROUND_Y = HEIGHT - 90
GRAVITY = 0.6
JUMP_FORCE = -16
BEAST_MODE_SCORE = 200

# ================= GAME STATE =================
game_started = False
game_paused = False
game_over = False
beast_mode = False
score = 0

# ================= LOAD ASSETS =================
dino_run = [
    pygame.transform.scale(pygame.image.load("assets/Dino_Run01.png"), (60,60)),
    pygame.transform.scale(pygame.image.load("assets/Dino_Run02.png"), (60,60))
]

dino_start = pygame.transform.scale(
    pygame.image.load("assets/DinoStart.png"), (60,60)
)

bird_imgs = [
    pygame.transform.scale(pygame.image.load("assets/Bird_01.png"), (70,50)),
    pygame.transform.scale(pygame.image.load("assets/Bird_02.png"), (70,50))
]

cactus_imgs = [
    pygame.transform.scale(pygame.image.load("assets/SmallCactus1.png"), (35,50)),
    pygame.transform.scale(pygame.image.load("assets/Cactus_Large_Single.png"), (40,70))
]

ground = pygame.transform.scale(
    pygame.image.load("assets/Ground.png"), (WIDTH,20)
)

ground_x1, ground_x2 = 0, WIDTH

# ================= DINO =================
DINO_GROUND = GROUND_Y + 20
dino = pygame.Rect(100, DINO_GROUND, 40, 50)
dino_vel = 0

# ================= OBSTACLE =================
obstacle_rect = None
obstacle_type = None
last_spawn = pygame.time.get_ticks()

# ================= ANIMATION =================
frame = 0
frame_timer = 0
bird_frame = 0

# ================= FONTS =================
title_font = pygame.font.SysFont("timesnewroman",46)
command_font = pygame.font.SysFont("timesnewroman",24)
small_font = pygame.font.SysFont("timesnewroman",22)
beast_font = pygame.font.SysFont("timesnewroman",28)

# ================= VOICE =================
voice = VoiceListener(("start","jump","pause","resume","reset","exit"))
voice.start()

# ================= DASHBOARD =================
def draw_dashboard():

    screen.fill(WHITE)

    title = title_font.render("Say It & Play It", True, BLACK)
    screen.blit(title,(WIDTH//2 - title.get_width()//2,40))

    subtitle = small_font.render("Voice Controlled Dino Game",True,GRAY)
    screen.blit(subtitle,(WIDTH//2 - subtitle.get_width()//2,95))

    commands = [
        "START  → Start the game",
        "JUMP   → Dino jumps",
        "PAUSE  → Pause the game",
        "RESUME → Continue game",
        "RESET  → Restart game",
        "EXIT   → Quit game"
    ]

    start_y = 150
    spacing = 34

    for i,cmd in enumerate(commands):

        txt = command_font.render(cmd,True,BLACK)

        screen.blit(
            txt,
            (WIDTH//2 - txt.get_width()//2 , start_y + i*spacing)
        )

    hint = small_font.render("Say 'START' to begin",True,BLUE)

    screen.blit(
        hint,
        (WIDTH//2 - hint.get_width()//2 , HEIGHT-25)
    )

# ================= MAIN LOOP =================
while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            voice.stop()
            pygame.quit()
            sys.exit()

    cmd = voice.get_command()

# ================= VOICE COMMANDS =================

    if cmd == "start":
        game_started = True
        game_over = False

    elif cmd == "jump" and game_started and not game_paused and not game_over:
        if dino.y >= DINO_GROUND - 1:
            dino_vel = JUMP_FORCE

    elif cmd == "pause":
        game_paused = True

    elif cmd == "resume":
        game_paused = False

    elif cmd == "reset":
        score = 0
        obstacle_rect = None
        dino.y = DINO_GROUND
        dino_vel = 0
        beast_mode = False
        game_over = False

    elif cmd == "exit":
        voice.stop()
        pygame.quit()
        sys.exit()

# ================= GAME UPDATE =================

    if game_started and not game_paused and not game_over:

        dino_vel += GRAVITY
        dino.y += dino_vel

        if dino.y > DINO_GROUND:
            dino.y = DINO_GROUND
            dino_vel = 0

        now = pygame.time.get_ticks()

        if obstacle_rect is None and now - last_spawn > 1800:

            if random.choice([True,False]):
                obstacle_type = "bird"
                obstacle_rect = pygame.Rect(WIDTH,HEIGHT-110,70,50)
            else:
                obstacle_type = "cactus"
                obstacle_rect = pygame.Rect(WIDTH,HEIGHT-70,40,70)

            last_spawn = now

        if obstacle_rect:
            obstacle_rect.x -= 8

            if obstacle_rect.right < 0:

                obstacle_rect = None

                if beast_mode:
                    score += 200
                else:
                    score += 100

        if obstacle_rect and dino.colliderect(obstacle_rect):
            game_over = True

# ================= BEAST MODE =================

        if score >= BEAST_MODE_SCORE:
            beast_mode = True

# ================= ANIMATION =================

        frame_timer += 1
        if frame_timer % 10 == 0:
            frame = (frame + 1) % 2
            bird_frame = (bird_frame + 1) % 2

        ground_x1 -= 8
        ground_x2 -= 8

        if ground_x1 <= -WIDTH:
            ground_x1 = WIDTH
        if ground_x2 <= -WIDTH:
            ground_x2 = WIDTH

# ================= DRAW =================

    if beast_mode:
        screen.fill(BLACK)
        text_color = WHITE

        beast_text = beast_font.render("BEAST MODE",True,RED)
        screen.blit(beast_text,(WIDTH//2 - beast_text.get_width()//2,10))

    else:
        screen.fill(WHITE)
        text_color = BLACK

    screen.blit(ground,(ground_x1,HEIGHT-30))
    screen.blit(ground,(ground_x2,HEIGHT-30))

# ================= STATES =================

    if not game_started:
        draw_dashboard()

    elif game_paused:
        txt = command_font.render("Game Paused - Say RESUME",True,text_color)
        screen.blit(txt,(WIDTH//2 - txt.get_width()//2,HEIGHT//2))

    elif game_over:

        txt = command_font.render("Game Over - Say RESET or EXIT",True,RED)

        screen.blit(
            txt,
            (WIDTH//2 - txt.get_width()//2, HEIGHT//2)
        )

    else:

        screen.blit(dino_run[frame],dino)

        if obstacle_rect:

            if obstacle_type == "bird":
                screen.blit(bird_imgs[bird_frame],obstacle_rect)
            else:
                screen.blit(cactus_imgs[0],obstacle_rect)

        score_text = small_font.render(f"Score : {score}",True,text_color)
        screen.blit(score_text,(20,20))

    pygame.display.flip()