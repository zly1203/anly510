
import pygame
import sys
import random
import time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐶 Puppy Dash: Bone or Poop")

# Load and scale assets
dog_img = pygame.image.load("dog.png")
dog_img = pygame.transform.scale(dog_img, (80, 80))

bone_img = pygame.image.load("bone.png")
bone_img = pygame.transform.scale(bone_img, (36, 36))

poop_img = pygame.image.load("poop.png")
poop_img = pygame.transform.scale(poop_img, (32, 30))  # even smaller poop

# Colors
PASTEL_BG = (255, 245, 235)
GROUND_COLOR = (220, 240, 220)
TEXT_COLOR = (50, 50, 50)

# Font
font = pygame.font.SysFont("arialrounded", 28)

# Game variables
dog_x = 100
dog_y = 260
dog_y_velocity = 0
gravity = 1
jump_strength = -15
on_ground = True

bone_x = WIDTH
bone_y = 180

poop_x = WIDTH + 400
poop_y = 310  # lower for easier jump

score = 0
game_over = False
start_time = time.time()
speed = 5  # starting obstacle speed

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill(PASTEL_BG)
    pygame.draw.rect(screen, GROUND_COLOR, (0, 340, WIDTH, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE and on_ground:
                dog_y_velocity = jump_strength
                on_ground = False

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                # Reset
                dog_y = 260
                dog_y_velocity = 0
                on_ground = True
                bone_x = WIDTH
                poop_x = WIDTH + 400
                score = 0
                start_time = time.time()
                speed = 5
                game_over = False

    if not game_over:
        elapsed = time.time() - start_time

        # Increase difficulty after 30s
        if elapsed > 30:
            speed = 7
        if elapsed > 45:
            speed = 9

        # Jump physics
        dog_y_velocity += gravity
        dog_y += dog_y_velocity
        if dog_y >= 260:
            dog_y = 260
            on_ground = True
            dog_y_velocity = 0

        # Move objects
        bone_x -= speed
        poop_x -= speed

        if bone_x < -36:
            bone_x = WIDTH + random.randint(100, 400)
            bone_y = random.randint(140, 200)

        if poop_x < -32:
            poop_x = WIDTH + random.randint(300, 600)

        # Collision logic
        dog_rect = pygame.Rect(dog_x, dog_y, 80, 80)
        bone_rect = pygame.Rect(bone_x, bone_y, 36, 36)
        poop_rect = pygame.Rect(poop_x, poop_y, 32, 30)

        if dog_rect.colliderect(bone_rect):
            score += 1
            bone_x = WIDTH + random.randint(100, 300)

        if dog_rect.colliderect(poop_rect):
            game_over = True

        # End game after 60 seconds
        if elapsed >= 60:
            game_over = True

    # Draw sprites
    screen.blit(dog_img, (dog_x, dog_y))
    screen.blit(bone_img, (bone_x, bone_y))
    screen.blit(poop_img, (poop_x, poop_y))

    # UI: Score and Timer
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 20))

    time_left = max(0, 60 - int(time.time() - start_time))
    timer_text = font.render(f"Time Left: {time_left}s", True, TEXT_COLOR)
    screen.blit(timer_text, (600, 20))

    if game_over:
        msg = "Time's up!" if time_left == 0 else "Oops! You hit poop!"
        end_text = font.render(f"{msg} Press R to restart", True, TEXT_COLOR)
        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
