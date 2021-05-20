import pygame # עכשיו אפשר להשתמש בפקודות ופונקציות של-pygame
import random as r # עכשין אפשר להשתמש ב-random בעזרת - r, כדי שיתן מספר רנדומלי
pygame.init() # כדי שהכל יעבוד, זה חייב להיות

clock = pygame.time.Clock() # למשתנה  clock מכניסים את דרך לפונקציה Clock, כדי שיהיה יותר כל לקבוע את כמות התמונות בשנייה
FPS = 60 # קובעים למשתנה FPS מספר 60

SCREEN_WEIGHT, SCREEN_HEIGHT = 1000, 1000 # מיידות של החלון
TILE_SIZE = 50 # מידה של דמויות, ממנו עשויה מפת המשחק
DISPLAY = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT)) # למשתנה DISPLAYאנחנו מכניסים דרך לפונקיה set_mode עם המידות השורה 8, כדי שיהיה יותר כל להשתמש
GAME_NAME = "Platformer for the school project" # משתנה עם שם המשחק
pygame.display.set_caption(GAME_NAME) # משנה את שם החלון למשתה שכתבמו בשורה 11

counter = 0 #משתנה להסיפת מטבעות
score = 0 # כמות מטבעות ששחקן הסף
bg_img = pygame.image.load("img/sky.png") # תמונה לאחורה
pygame.font.init() # חייב לכתיבת טקסט על המסך
myfont = pygame.font.SysFont('Aharoni', 60) #משתה עם צורת אותיות וגודל שלהן


class World(): # מחקלה World, כדי לבנות את מפה
    def __init__(self, data): # פונקציה שעובדת רק פעם אחד בתחילת התוכנית
        self.tile_list = [] # רשימה של דמויות

        #מעלה תמונות
        dirt_img = pygame.image.load("img/dirt.png")
        grass_img = pygame.image.load("img/grass.png")

        row_count = 0 #משתנה לשורות
        for row in data: #  לולאה שעוברת דרך משתנה data
            col_count = 0 #משתנה
            for tile in row: # לולאה שעוברת דרך משתנה row
                if tile == 1: # אם tile שווה 1, הוא תוסיף אדמה בלי דשה
                    img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE)) # משנה את הגודל הדמות
                    img_rect = img.get_rect() # שומר את המידה של הדמות
                    img_rect.x = col_count * TILE_SIZE # מחשב את ערך x
                    img_rect.y = row_count * TILE_SIZE # מחשב את ערך y
                    tile = (img, img_rect) # שומר את מידות של הדמות וכו'
                    self.tile_list.append(tile) # מוסיף לרשימה את ה-tile

                if tile == 2: # אם tile שווה 2, הוא תוסיף אדמה בלי דשה
                    img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE)) # משנה את הגודל הדמות
                    img_rect = img.get_rect() # שומר את המידה של הדמות
                    img_rect.x = col_count * TILE_SIZE # מחשב את ערך x
                    img_rect.y = row_count * TILE_SIZE # מחשב את ערך y
                    tile = (img, img_rect) # שומר את מידות של הדמות וכו'
                    self.tile_list.append(tile) # מוסיף לרשימה את ה-tile
                col_count += 1
            row_count += 1

    def draw(self): # פונקציה שמציירת את הדמויות
            for tile in self.tile_list: # לולאה שעוברת דרך כל הדמויות
                DISPLAY.blit(tile[0], tile[1]) # מצייר את דמות

class Player(): # מחקלה Player, כדי ליצר את הדמות של שחקן
    def __init__(self, x, y): # פונקציה שעובדת רק פעם אחד בתחילת התוכנית
        self.images_right = [] # רשימה לתמונות הליכה ימינה
        self.images_left = [] # רשימה לתמונות הליכה שמאלה
        self.index = 0 # אינדקס של תמונה שיוצג
        self.counter = 0 # שעון להחלפת תמונת השחקן
        for num in range(1, 5): #מעלה את כל התמונות
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False) # הופך את הדמות בציר ה-x, כדי שהיא תסתכל שמאלה
            self.images_right.append(img_right) # מוסיף את הדמות לרשיצה images_right
            self.images_left.append(img_left) # מוסיף את הדמות לרשיצה images_left
        self.image = self.images_right[self.index] # מגיר את אך תראה הדמות עכשיו
        self.rect = self.image.get_rect() # שומר את המידה של הדמות
        self.rect.x = x # מגדיר את ערך x
        self.rect.y = y # מגדיר את ערך y
        self.width = self.image.get_width() # מגדיר את
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
    seconds_timer = 60 - round(seconds)
    score_text = myfont.render("Score: " + str(score), False, (0, 0, 0))
    timer_text = myfont.render(" Timer: " + str(seconds_timer), False, (0, 0, 0))
    DISPLAY.blit(score_text, (50, 55))
    if seconds_timer >= 50:
        DISPLAY.blit(mainGoal_text, (290, 55))
        DISPLAY.blit(jump_text, (440, 105))
    if seconds_timer >= 0:
        DISPLAY.blit(timer_text, (40, 105))
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

