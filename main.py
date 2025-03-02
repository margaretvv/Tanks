from pygame import *
from random import randint

back=(50,4,59)

img_bullet = "bullet.png"
img_hero = "tank.png"
img_enemy1 = "enemy1.png"
img_enemy2 = "enemy2.png"
img_enemy3 = "enemy3.png"
img_base = "base.png"
img_base_destroyed = "base_destroyed.png"

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.player_image = player_image

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500

display.set_caption("Tanks")
window = display.set_mode((win_width, win_height))

class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x<win_width-80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y>5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y<win_width-80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, randint(1,40), randint(1,40))
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            if self.player_image != img_asteroid:
                lost += 1
bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()

def lvl1():
    global run 
    player = Player(img_hero, 5, win_height - 100, 10, 80, 100)
    enemy1 = Enemy(img_enemy1, randint(80, win_width - 80), -40, randint(1,5), 50, 50)
    enemy2 = Enemy(img_enemy2, randint(80, win_width - 80), -40, randint(1,5), 50, 50)
    enemy3 = Enemy(img_enemy3, randint(80, win_width - 80), -40, randint(1,5), 50, 50)
    bullets = sprite.Group()
    enemies = sprite.Group()

finish = False
run = True

while run: 
    for e in event.get():
        if e.type == quit:
            run = False
    if not finish: 
        window.blit(back(0,0))



        display.update()
        