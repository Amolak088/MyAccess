import pygame
import math
import sys

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 800, 600
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 200
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
SCALE = WIDTH // NUM_RAYS

# ---------------- SCREEN ----------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Minecraft 3D")
clock = pygame.time.Clock()

# ---------------- COLORS ----------------
SKY = (100, 180, 255)
GROUND = (60, 60, 60)
BLOCK = (150, 100, 50)

# ---------------- MAP ----------------
TILE = 50
world_map = [
    "111111111111",
    "1..........1",
    "1..1111....1",
    "1..........1",
    "1....11....1",
    "1..........1",
    "111111111111",
]

map_width = len(world_map[0]) * TILE
map_height = len(world_map) * TILE

# ---------------- PLAYER ----------------
player_x = 150
player_y = 150
player_angle = 0
player_speed = 3

# ---------------- RAYCAST ----------------
def raycast():
    start_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        angle = start_angle + ray * DELTA_ANGLE
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        for depth in range(1, MAX_DEPTH, 2):
            x = player_x + depth * cos_a
            y = player_y + depth * sin_a

            map_x = int(x // TILE)
            map_y = int(y // TILE)

            if world_map[map_y][map_x] == "1":
                depth *= math.cos(player_angle - angle)
                height = DIST / (depth + 0.0001)
                color = (BLOCK[0] / (1 + depth * 0.01),
                         BLOCK[1] / (1 + depth * 0.01),
                         BLOCK[2] / (1 + depth * 0.01))

                pygame.draw.rect(
                    screen,
                    color,
                    (ray * SCALE, HEIGHT // 2 - height // 2, SCALE, height)
                )
                break

# ---------------- GAME LOOP ----------------
while True:
    screen.fill(SKY)
    pygame.draw.rect(screen, GROUND, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    if keys[pygame.K_w]:
        player_x += math.cos(player_angle) * player_speed
        player_y += math.sin(player_angle) * player_speed
    if keys[pygame.K_s]:
        player_x -= math.cos(player_angle) * player_speed
        player_y -= math.sin(player_angle) * player_speed
    if keys[pygame.K_a]:
        player_angle -= 0.05
    if keys[pygame.K_d]:
        player_angle += 0.05

    raycast()
    pygame.display.flip()
    clock.tick(60)