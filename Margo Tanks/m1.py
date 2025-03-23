from pygame import *
import sys
import random
from time import sleep 

init()

# Constants
WIDTH, HEIGHT = 960, 720  # Increased the screen size to accommodate a larger map
TILE_SIZE = 32
SCREEN = display.set_mode((WIDTH, HEIGHT))
FPS = 60
CLOCK = time.Clock()
score=0
font.init()
FONT = font.SysFont('Arial', 24)
font2= font.SysFont('Arial', 110)
win=font2.render('YOU WIN', True, (2,245,19)) 
lose=font2.render('YOU LOSE', True,(156,2,2))

# Load images
brick = transform.scale(image.load('brick.png'), (TILE_SIZE, TILE_SIZE))
steel = transform.scale(image.load('steel.png'), (TILE_SIZE, TILE_SIZE))
water = transform.scale(image.load('water.png'), (TILE_SIZE, TILE_SIZE))
empty = transform.scale(image.load('empty.png'), (TILE_SIZE, TILE_SIZE))
enemy_img = [transform.scale(image.load('enemy1.png'), (TILE_SIZE, TILE_SIZE)),
             transform.scale(image.load('enemy2.png'), (TILE_SIZE, TILE_SIZE)),
             transform.scale(image.load('enemy3.png'), (TILE_SIZE, TILE_SIZE))]
player_img = transform.scale(image.load('player_tank.png'), (TILE_SIZE-2, TILE_SIZE-2))
projectile_img = transform.scale(image.load('bullet.png'), (8, 8))

# New larger map data
map_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 1],
    [1, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 1],
    [1, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 1],
    [1, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 1],
    [1, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 1],
    [1, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 1],
    [1, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Tank class
class Tank(sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__() 
        self.x = x
        self.y = y
        self.image = img
        self.original_img = img  # Store the original image for rotation
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = 5
        self.direction = (0, -1)
        self.projectiles = []
        self.health = 10  # Add health attribute

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))
        for projectile in self.projectiles:
            projectile.draw()

    def move(self, dx, dy, map_data):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if not self.check_collision(new_x, new_y, map_data):
            self.x = new_x
            self.y = new_y
            self.rect.topleft = (self.x, self.y)
            self.direction = (dx, dy)
            self.rotate_tank()

    def check_collision(self, x, y, map_data):
        # Check all four corners and the center points of each side of the tank
        points = [
            (x, y),  # Top-left corner
            (x + TILE_SIZE - 5, y),  # Top-right corner
            (x, y + TILE_SIZE - 5),  # Bottom-left corner
            (x + TILE_SIZE - 5, y + TILE_SIZE - 5),  # Bottom-right corner
            (x + TILE_SIZE // 5, y),  # Top-center
            (x + TILE_SIZE // 5, y + TILE_SIZE - 5),  # Bottom-center
            (x, y + TILE_SIZE // 5),  # Left-center
            (x + TILE_SIZE - 5, y + TILE_SIZE // 5)  # Right-center
        ]
        for point_x, point_y in points:
            col = point_x // TILE_SIZE
            row = point_y // TILE_SIZE
            if col < 0 or col >= len(map_data[0]) or row < 0 or row >= len(map_data):
                return True
            if map_data[row][col] in [1, 2, 3]:
                return True
        return False

    def rotate_tank(self):
        if self.direction == (0, -1):  # Up
            self.image = self.original_img
        elif self.direction == (0, 1):  # Down
            self.image = transform.rotate(self.original_img, 180)
        elif self.direction == (-1, 0):  # Left
            self.image = transform.rotate(self.original_img, 90)
        elif self.direction == (1, 0):  # Right
            self.image = transform.rotate(self.original_img, -90)

    def shoot(self):
        dx, dy = self.direction
        angle = 0
        if self.direction == (0, -1):  # Up (0, -1)
            angle = -90
        elif self.direction == (0, 1):  # Down
            angle = 90
        elif self.direction == (-1, 0):  # Left
            angle = 0
        elif self.direction == (1, 0):  # Right (1, 0)
            angle = 180
        projectile = Projectile(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2, dx, dy, projectile_img, angle)
        self.projectiles.append(projectile)

    def update_projectiles(self, map_data, enemy_group):
        global score
        for projectile in self.projectiles[:]:
            if projectile.update(map_data):
                self.projectiles.remove(projectile)
            else:
                hit_enemy = sprite.spritecollideany(projectile, enemy_group)
                if hit_enemy:
                    self.projectiles.remove(projectile)
                    enemy_group.remove(hit_enemy)
                    score += 250
 
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            print("Game Over")
            SCREEN.blit(lose, (80,60))
            display.update()
            sleep(7)
            quit()

# Projectile class
class Projectile(sprite.Sprite):
    def __init__(self, x, y, dx, dy, img, angle):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.image = transform.rotate(img, angle)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = 10

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))

    def update(self, map_data):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.topleft = (self.x, self.y)
        return self.check_collision(map_data)

    def check_collision(self, map_data):
        col = self.x // TILE_SIZE
        row = self.y // TILE_SIZE
        if col < 0 or col >= len(map_data[0]) or row < 0 or row >= len(map_data):
            return True
        if map_data[row][col] in [1, 2, 3]:
            return True
        return False

# EnemyTank class
class EnemyTank(Tank):
    def __init__(self, x, y, img):
        super().__init__(x, y, img)
        self.move_counter = 0

    def random_move(self, map_data):
        if self.move_counter == 0:
            self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
            self.move_counter = random.randint(20, 50)
        self.move_counter -= 1
        self.move(self.direction[0], self.direction[1], map_data)

    def shoot(self):
        if random.random() < 0.04:  # Random chance to shoot
            super().shoot()

# Draw map function
def draw_map(map_data):
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            if map_data[row][col] == 1:
                SCREEN.blit(brick, (x, y))
            elif map_data[row][col] == 2:
                SCREEN.blit(steel, (x, y))
            elif map_data[row][col] == 3:
                SCREEN.blit(water, (x, y))
            else:
                SCREEN.blit(empty, (x, y))

# Find an empty tile to spawn the tank
def find_empty_tile(map_data, used_tiles):
    empty_tiles = [(col * TILE_SIZE, row * TILE_SIZE) for row in range(len(map_data)) for col in range(len(map_data[row])) if map_data[row][col] == 0 and (col * TILE_SIZE, row * TILE_SIZE) not in used_tiles]
    if empty_tiles:
        return random.choice(empty_tiles)
    return None, None

# Main loop
running = True
used_tiles = set()
spawn_x, spawn_y = find_empty_tile(map_data, used_tiles)
used_tiles.add((spawn_x, spawn_y))
player_tank = Tank(spawn_x, spawn_y, player_img)

enemy_group = sprite.Group()
for _ in range(10):  # Create 5 enemy tanks
    enemy_spawn_x, enemy_spawn_y = find_empty_tile(map_data, used_tiles)
    used_tiles.add((enemy_spawn_x, enemy_spawn_y))
    enemy_tank = EnemyTank(enemy_spawn_x, enemy_spawn_y, random.choice(enemy_img))
    enemy_group.add(enemy_tank)

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player_tank.shoot()

    keys = key.get_pressed()
    if keys[K_LEFT]:
        player_tank.move(-1, 0, map_data)
    if keys[K_RIGHT]:
        player_tank.move(1, 0, map_data)
    if keys[K_UP]:
        player_tank.move(0, -1, map_data)
    if keys[K_DOWN]:
        player_tank.move(0, 1, map_data)

    player_tank.update_projectiles(map_data, enemy_group)
    for enemy_tank in enemy_group:
        enemy_tank.random_move(map_data)
        enemy_tank.shoot()
        for projectile in enemy_tank.projectiles:
            if projectile.update(map_data):
                enemy_tank.projectiles.remove(projectile)
            if sprite.collide_rect(projectile, player_tank):
                player_tank.take_damage()
                enemy_tank.projectiles.remove(projectile)

    SCREEN.fill((0, 0, 0))
    draw_map(map_data)
    player_tank.draw()
    enemy_group.draw(SCREEN)

    # Draw enemy projectiles
    for enemy_tank in enemy_group:
        for projectile in enemy_tank.projectiles:
            projectile.draw()

    # Draw health label
    health_label = FONT.render(f'Health: {player_tank.health}', True, (255, 255, 255))
    SCREEN.blit(health_label, (WIDTH - health_label.get_width() - 10, 10))
    score_label = FONT.render(f'score: {score}', True, (255,255,255))
    SCREEN.blit(score_label, (WIDTH - score_label.get_width() - 10, 40))
    if len(enemy_group) <= 0:
        SCREEN.blit(win, (80,60))  
    display.update()
    CLOCK.tick(FPS)

quit()
