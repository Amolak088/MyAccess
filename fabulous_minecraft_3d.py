import pygame, math, sys

pygame.init()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ---------------- CAMERA ----------------
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 480
MAX_DEPTH = 1000
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
SCALE = WIDTH // NUM_RAYS
SENSITIVITY = 0.002

# ---------------- COLORS ----------------
SKY = (90, 180, 255)
GROUND = (50, 160, 70)
WALL = (130, 100, 60)

# ---------------- MAP ----------------
TILE = 64
world_map = [
    "111111111111111",
    "1.....T.......1",
    "1..1111....A...1",
    "1.....T.......1",
    "1...A.....T....1",
    "1..............1",
    "111111111111111",
]

# ---------------- PLAYER ----------------
px, py = 300, 300
pa = 0
speed = 4
radius = 20

# ---------------- OBJECTS ----------------
objects = [
    {"x": 500, "y": 350, "color": (255, 150, 150), "size": 120},  # Pig
    {"x": 650, "y": 420, "color": (130, 130, 130), "size": 140},  # Cow
    {"x": 720, "y": 300, "color": (240, 240, 240), "size": 130},  # Sheep
    {"x": 420, "y": 200, "color": (40, 120, 40), "size": 200},   # Tree
]

# ---------------- FUNCTIONS ----------------
def collision(nx, ny):
    mx, my = int(nx // TILE), int(ny // TILE)
    return world_map[my][mx] != "."

def raycast():
    start_angle = pa - HALF_FOV
    for ray in range(NUM_RAYS):
        angle = start_angle + ray * DELTA_ANGLE
        sin_a, cos_a = math.sin(angle), math.cos(angle)

        for depth in range(1, MAX_DEPTH, 4):
            x = px + depth * cos_a
            y = py + depth * sin_a
            mx, my = int(x // TILE), int(y // TILE)

            if world_map[my][mx] != ".":
                depth *= math.cos(pa - angle)
                h = DIST / (depth + 0.0001)
                shade = max(50, 255 / (1 + depth * 0.01))
                color = (
                    WALL[0] * shade / 255,
                    WALL[1] * shade / 255,
                    WALL[2] * shade / 255
                )
                pygame.draw.rect(
                    screen, color,
                    (ray * SCALE, HEIGHT // 2 - h // 2, SCALE, h)
                )
                break

def draw_objects():
    for obj in sorted(objects, key=lambda o: -((o["x"]-px)**2 + (o["y"]-py)**2)):
        dx, dy = obj["x"] - px, obj["y"] - py
        dist = math.hypot(dx, dy)
        angle = math.atan2(dy, dx) - pa

        if -HALF_FOV < angle < HALF_FOV and dist > 30:
            size = obj["size"] / dist * 200
            x = WIDTH // 2 + math.tan(angle) * DIST
            y = HEIGHT // 2 - size // 2
            shade = max(50, 255 / (1 + dist * 0.02))
            color = tuple(c * shade / 255 for c in obj["color"])
            pygame.draw.rect(screen, color, (x, y, size, size))

# ---------------- GAME LOOP ----------------
while True:
    screen.fill(SKY)
    pygame.draw.rect(screen, GROUND, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pa += event.rel[0] * SENSITIVITY

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_w]:
        dx += math.cos(pa) * speed
        dy += math.sin(pa) * speed
    if keys[pygame.K_s]:
        dx -= math.cos(pa) * speed
        dy -= math.sin(pa) * speed
    if keys[pygame.K_a]:
        dx += math.sin(pa) * speed
        dy -= math.cos(pa) * speed
    if keys[pygame.K_d]:
        dx -= math.sin(pa) * speed
        dy += math.cos(pa) * speed
    if keys[pygame.K_ESCAPE]:
        pygame.quit(); sys.exit()

    if not collision(px + dx, py):
        px += dx
    if not collision(px, py + dy):
        py += dy

    raycast()
    draw_objects()

    pygame.display.flip()
    clock.tick(60)