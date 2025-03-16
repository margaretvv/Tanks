import pygame

# Ініціалізація Pygame
pygame.init()
map_data = [
    [1, 1, 0, 0, 2, 2, 0, 0, 1, 1],
    [1, 0, 0, 3, 3, 3, 3, 0, 0, 1],
    [0, 0, 1, 0, 2, 2, 0, 1, 0, 0],
    [0, 3, 0, 0, 1, 1, 0, 0, 3, 0],
    [2, 2, 1, 0, 0, 0, 0, 1, 2, 2],
    [0, 3, 0, 1, 1, 1, 1, 0, 3, 0],
    [0, 0, 1, 0, 2, 2, 0, 1, 0, 0],
    [1, 0, 0, 3, 3, 3, 3, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1]
]

# Розміри екрана та блоку
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 32

# Створюємо вікно
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Завантажуємо спрайти
brick = pygame.transform.scale(pygame.image.load('brick.png'),(TILE_SIZE, TILE_SIZE))
steel = pygame.transform.scale(pygame.image.load('steel.png'),(TILE_SIZE, TILE_SIZE))
water = pygame.transform.scale(pygame.image.load('water.png'),(TILE_SIZE, TILE_SIZE))
empty = pygame.transform.scale(pygame.image.load('empty.png'),(TILE_SIZE, TILE_SIZE))
player_img = pygame.transform.scale(pygame.image.load('player_tank.png'),(TILE_SIZE, TILE_SIZE))
#empty = pygame.Surface((TILE_SIZE, TILE_SIZE))  # Порожній блок
#empty.fill((0, 0, 0))  # Чорний колір для порожнього блоку
def draw_map():
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            
            if map_data[row][col] == 1:
                screen.blit(brick, (x, y))
            elif map_data[row][col] == 2:
                screen.blit(steel, (x, y))
            elif map_data[row][col] == 3:
                screen.blit(water, (x, y))
            else:
                screen.blit(empty, (x, y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Відображаємо карту
    draw_map()

    # Оновлюємо екран
    pygame.display.flip()

pygame.quit()
