from pygame import *
from random import randint
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 36)
font3 = font.Font(None, 70)
font4 = font.Font(None, 36)
win = font3.render('YOU WON!', True, (255,215,0))
lose = font3.render('YOU lOSE!', True, (255,215,0))
lost = 0
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
game = True
clock = time.Clock()

FPS = 60
class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(filename), (w,h)) 
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, filename, w, h, x, y, speed):
        super().__init__(filename, w, h, x, y, speed)
        self.health = 81
        self.is_parrying = False
        self.parry_duration = 90
        self.parry_timer = 0
        self.parry_interval = 150
        self.last_parry_time = 500
    def fire(self):
        bullet = Bullet('bullet.png', 13, 18, self.rect.centerx, self.rect.top, 8)
        enemybullets.add(bullet)
    def update(self):
        current_time = time.get_ticks()
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 10
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += 10
       
        if self.is_parrying:
            current_time = time.get_ticks()
            # print(current_time)
            if current_time - self.start_time >= 1:
                self.parry_timer -= 1
                self.start_time = current_time
                # print('.')
                # current_time = pygame.time.get_ticks()
        # if current_time - self.parry_timer > self.parry_interval:
        #     self.parry_timer = current_time
            if self.parry_timer <= 0:
                self.is_parrying = False
                self.last_parry_time = time.get_ticks()


    def parry(self):
        if not self.is_parrying:
            self.is_parrying = True
            self.parry_timer = self.parry_duration
            # self.last_parry_time = time.get_ticks()
           
class UfoBullet(GameSprite):
    def shoot(self):
        current_time = time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval:
            self.last_shot_time = current_time
         
class Ufo(GameSprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__(filename, w, h, speed, x, y)
        self.last_shot_time = time.get_ticks()
        self.shoot_interval = 2000
        self.damage = 20
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.speed = randint(3,4)
            self.rect.x = randint(0, 700 - self.rect.width)
            lost += 1
    def shoot(self):
        global enemybullets
        current_time = time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval:
            self.last_shot_time = current_time
            enemybullet = UfoBullet("bullet.png", 10, 30, 20, self.rect.centerx, self.rect.bottom)
            enemybullets.add(enemybullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

enemybullets = sprite.Group()
player = Player('rocket.png', 65, 65, 50, 420, 3)
ufo1 = Ufo('ufo.png', 70, 40, randint(5,655), 0, randint(1,2))
ufo2 = Ufo('ufo.png', 70, 40, randint(5,655), 0, randint(1,2))
ufo3 = Ufo('ufo.png', 70, 40, randint(5,655), 0, randint(1,2))
ufo4 = Ufo('ufo.png', 70, 40, randint(5,655), 0, randint(1,2))
ufo5 = Ufo('ufo.png', 70, 40, randint(5,655), 0, randint(1,2))
button = GameSprite('кнопка1.png', 265, 250, 225, 140, 0)
kills = 0
monsters = sprite.Group()
monsters.add(ufo1,ufo2,ufo3,ufo4,ufo5)
menu = True
finish = False
while game:
    if menu == True:
        window.blit(background, (0,0))
        button.reset()
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                if button.rect.collidepoint(x,y):
                    menu = False

    if finish == False and menu == False:
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255,255,255))
        text_lose1 = font2.render('Счет:' + str(kills), 1, (255,255,255))
        text_lose2 = font1.render(f'Здоровье: {player.health}', True, (255, 255, 255))
        window.blit(background, (0,0))
        window.blit(background, (0,0))
        window.blit(text_lose, (40,40))
        window.blit(text_lose1, (40,75))
        window.blit(text_lose2, (40,110))

        player.update()
        monsters.draw(window)
        monsters.update()
        enemybullets.draw(window)
        enemybullets.update()
        player.reset()
        sprite_list = sprite.groupcollide(monsters, enemybullets, True, True)
        sl = sprite.spritecollide(player, monsters, True)
        for i in sprite_list:
            kills += 1
            ufo1 = Ufo('ufo.png', 70, 40, randint(5,655), 0, randint(1,2))
            monsters.add(ufo1)
        if kills >= 20:
            fihish = True
            window.blit(background, (0,0))
            window.blit(win, (230,230))
        if lost >= 3 or player.health <= 0:
            fihish = True
            window.blit(background, (0,0))
            window.blit(lose, (230,230))
        
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    player.fire()

                     
                if e.button == 3:
                    # print('jjj')
                    if not player.is_parrying:
                        player.start_time = time.get_ticks()
                        current_time = time.get_ticks()

                        if current_time - player.last_parry_time > player.parry_interval:
                            # player.last_parry_time = current_time
                            print('parry')
                            player.parry()
                    print(f"Player: {player.is_parrying}")

        for enemy in sl:
            ufo1 = Ufo('ufo.png', 70, 40, randint(5,655), 0, randint(3,5))
            monsters.add(ufo1)
            if not player.is_parrying:
                player.health -= enemy.damage  
                # print(f"Player Health: {player.health}")
                # print(f"Player: {player.is_parrying}")
            else:
                print("Attack parried!")

    if finish == True and menu == False:
            for e in event.get():
                if e.type == QUIT:
                    game = False
    clock.tick(FPS)
    display.update()
    