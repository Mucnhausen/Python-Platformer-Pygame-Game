import pygame
from pygame.locals import *
import random as r
import time
pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WEIGHT, SCREEN_HEIGHT = 1000, 1000
TILE_SIZE = 50
DISPLAY = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
GAME_NAME = "Platformer for the school project"
pygame.display.set_caption(GAME_NAME)

coins_num = 2
counter = 0
score = 0
bg_img = pygame.image.load("img/sky.png")
pygame.font.init()
myfont = pygame.font.SysFont('Aharoni', 60)


class World():
    def __init__(self, data):
        self.tile_list = []

        #tmunot
        dirt_img = pygame.image.load("img/dirt.png")
        grass_img = pygame.image.load("img/grass.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 2:
                    img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
            for tile in self.tile_list:
                DISPLAY.blit(tile[0], tile[1])
                pygame.draw.rect(DISPLAY, (255, 255,255), tile[1], 2)

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 5

        # get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and key[pygame.K_LEFT]:
            dx = 0
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if (key[pygame.K_LEFT] or key[pygame.K_a]) == False and (key[pygame.K_RIGHT] or key[pygame.K_d]) == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]



        # handle animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for collision
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0



        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            dy = 0

        # draw player onto screen
        DISPLAY.blit(self.image, self.rect)
        pygame.draw.rect(DISPLAY, (255, 255, 255), self.rect, 2)

class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.coins_speed = 1
        self.image = pygame.image.load("img/coin.png")
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):
        #w self.coins_num += 0.00001
        self.rect.y += self.coins_speed
        if self.rect.y == SCREEN_HEIGHT:
            self.kill()
            print(coins_group)



world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 1, 1, 1],
    [1, 1, 2, 2, 2, 0, 0, 2, 1, 1, 1, 2, 0, 0, 0, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
world = World(world_data)
player = Player(100, SCREEN_HEIGHT - 130)

seconds_timer = 0
coins_group = pygame.sprite.Group()
level = 1
start_ticks=pygame.time.get_ticks()
game_time = 60

run = True
while run:
    #שעון
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    gameOVER_timer = (pygame.time.get_ticks() - start_ticks) / 1000

    #טקסטים
    gameOver_text = myfont.render("GAME OVER", False, (0, 0, 0))
    closeWindow_text = myfont.render(str(score) + " :התפסה התא", False, (0, 0, 0))
    mainGoal_text = myfont.render("תועבטמ רתויש לככ סופתל ךירצ" , False, (0, 0, 0))
    jump_text = myfont.render("ףוס ןיא דע ץופקל רשפא" , False, (0, 0, 0))

    clock.tick(FPS)
    DISPLAY.blit(bg_img, (0, 0))
    world.draw()
    coin = Coins(r.randint(TILE_SIZE, SCREEN_WEIGHT - TILE_SIZE - 20), r.randint(-10000, -100))
    if counter >= 0 and counter <= 300:
        counter += 1
        for i in range(1, 50):
            coins_group.add(coin)

    coins_group.draw(DISPLAY)
    if pygame.sprite.spritecollide(player, coins_group, True) and seconds_timer > 0:
        score += 1
        coins_group.add(coin)
    coins_group.update()
    print(coins_group)
    print(counter)
    seconds_timer = 60 - round(seconds)
    score_text = myfont.render("Score: " + str(score), False, (0, 0, 0))
    timer_text = myfont.render(" Timer: " + str(seconds_timer), False, (0, 0, 0))
    DISPLAY.blit(score_text, (50, 55))
    if seconds_timer >= 50:
        DISPLAY.blit(mainGoal_text, (290, 55))
        DISPLAY.blit(jump_text, (440, 105))
    if seconds_timer >= 0:
        DISPLAY.blit(timer_text, (40, 105))
    print(score)
    if seconds > game_time:
        DISPLAY.blit(gameOver_text, (350, 450))
        DISPLAY.blit(closeWindow_text, (350, 500))
        seconds_timer = 0
        if seconds >= game_time + 5:
            quit()
    player.update()
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

