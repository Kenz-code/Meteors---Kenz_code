import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as py
from sys import exit
import random
import time
import pickle
import threading

py.mixer.init()
py.init()

score = 0
lives = 3
screen_sides = 800
WHITE = 255,255,255
BLACK= 0,0,0
YELLOW =255,255,0
FPS = 30

screen = py.display.set_mode((screen_sides,screen_sides))
py.display.set_caption('Meteors')
clock = py.time.Clock()

background = py.image.load('pictures\Background.png')
sshooter = py.image.load('pictures\shooter.png')
shooter = py.transform.scale(sshooter,(60,60))

explosion_sfx = py.mixer.Sound('sfx/Explosion1.wav')
start_sfx = py.mixer.Sound('sfx/SuperHero_original.wav')
music = py.mixer.Sound('sfx/Memoraphile - Spooky Dungeon.wav')
shoot_sfx = py.mixer.Sound('sfx/shoot.wav')
hit_player_sfx = py.mixer.Sound('sfx/sfx_sounds_damage3.wav')
menu_select_sfx = py.mixer.Sound('sfx/sfx_menu_select2.wav')
lose_sfx = py.mixer.Sound('sfx/Jingle_Lose_00.wav')

score_font = py.font.Font("arcadeclassic\ARCADECLASSIC.TTF", 50) 
score_txt = score_font.render('Score ' + str(score), True, WHITE)
lives_txt = score_font.render('Lives ' + str(lives), True, WHITE)

screen.blit(background,(0,100))
screen.blit(score_txt, (10,10))
screen.blit(lives_txt, (10,40))

py.display.update()

class Player(py.sprite.Sprite):
    #get sprite pic
    sshooter = py.image.load('pictures\shooter.png')
    shooter = py.transform.scale(sshooter,(60,60))
    # sprite fot thee palyer
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image = shooter
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.center = (400, 700)
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = py.key.get_pressed()
        if keystate[py.K_a]:
            self.speedx = -1
        if keystate[py.K_d]:
            self.speedx = 1
        self.rect.x += self.speedx
        if self.rect.right > screen_sides:
            self.rect.right = screen_sides
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        shoot_sfx.play()
        shooter_group.add(bullet)
        bullets.add(bullet)

class Astroid(py.sprite.Sprite):
    def __init__(self, speed):
        astroids=[]
        aastroid1=py.image.load('pictures\metoers\spaceMeteors_001.png')
        aastroid2=py.image.load('pictures\metoers\spaceMeteors_002.png')
        aastroid3=py.image.load('pictures\metoers\spaceMeteors_003.png')
        aastroid4=py.image.load('pictures\metoers\spaceMeteors_004.png')
        
        astroid1 = py.transform.scale(aastroid1,(70,70))
        astroid2 = py.transform.scale(aastroid2,(70,70))
        astroid3 = py.transform.scale(aastroid3,(70,70))
        astroid4 = py.transform.scale(aastroid4,(70,70))
        
        astroids.append(astroid1)
        astroids.append(astroid2)
        astroids.append(astroid3)
        astroids.append(astroid4)
        py.sprite.Sprite.__init__(self)
        self.image = random.choice(astroids)
        self.rect = self.image.get_rect()
        self.radius = 30
        self.rect.x = random.randrange(screen_sides - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.choice(speed)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_sides + 10:
            self.rect.y =random.randrange(-100, -40)

class Astroid2(py.sprite.Sprite):
    def __init__(self, speed):
        astroids=[]
        aastroid1=py.image.load('pictures\metoers\spaceMeteors_001.png')
        aastroid2=py.image.load('pictures\metoers\spaceMeteors_002.png')
        aastroid3=py.image.load('pictures\metoers\spaceMeteors_003.png')
        aastroid4=py.image.load('pictures\metoers\spaceMeteors_004.png')
        
        astroid1 = py.transform.scale(aastroid1,(30,30))
        astroid2 = py.transform.scale(aastroid2,(30,30))
        astroid3 = py.transform.scale(aastroid3,(30,30))
        astroid4 = py.transform.scale(aastroid4,(30,30))
        
        astroids.append(astroid1)
        astroids.append(astroid2)
        astroids.append(astroid3)
        astroids.append(astroid4)
        py.sprite.Sprite.__init__(self)
        self.image = random.choice(astroids)
        self.rect = self.image.get_rect()
        self.radius = 14
        self.rect.x = random.randrange(screen_sides - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.choice(speed)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_sides + 10:
            self.rect.y =random.randrange(-100, -40)

class Bullet(py.sprite.Sprite):
    def __init__(self, x ,y):
        py.sprite.Sprite.__init__(self)
        bbullet_img = py.image.load('pictures/laserGreen.png')
        bullet_img = py.transform.scale(bbullet_img,(5,10))
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(py.sprite.Sprite):
    def __init__(self, x,y):
        py.sprite.Sprite.__init__(self)
        self.image = explosion_ani[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.frame = 0
        self.last_update = py.time.get_ticks()
        self.frame_rate = 30

    def update(self):
        now = py.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame ==len(explosion_ani):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_ani[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def add(a):
    global score
    global high_score
    score += a
    if score > high_score:
        high_score = int(score)
    rect_reset = py.Rect((1,300),(1,39))
    py.draw.rect(screen, BLACK, ((1,300),(1,39)))
    py.display.update()

def start_screen():
    global score
    background = py.image.load('pictures\Background.png')
    font = py.font.Font("arcadeclassic\ARCADECLASSIC.TTF", 75)
    big_font = py.font.Font("arcadeclassic\ARCADECLASSIC.TTF", 150)
    txt = font.render('Press Space', True, WHITE)
    big_txt = big_font.render('Meteors', True, WHITE)

    py.mixer.stop()
    start_sfx.play()
    screen.blit(background, (0,100))
    screen.blit(big_txt, (120, 200))
    screen.blit(txt, (190, 500))
    py.display.update()
    yo = True
    while yo:
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    py.mixer.stop()
                    menu_select_sfx.play()
                    yo = False
                    time.sleep(1)
                    music.play(-1)

def del_life():
    global lives
    if lives == 0:
        dead_screen()
        py.mixer.stop()
        py.mixer.music.stop()
        lose_sfx.play()
        time.sleep(3)
        py.quit()
        exit()
    lives -= 1
    rect_reset = py.Rect((1,300),(39,70))
    py.draw.rect(screen, BLACK, ((1,300),(1,39)))
    py.display.update()

def save_score():
    global score
    global high_score
    if score == high_score:
        high_score = int(score)
        print(high_score)
        pickle.dump(high_score, open('high_score.dat', 'wb'))
    elif score != high_score:
        pass
    else:
        pass

def open_score():
    global score
    global high_score
    high_score = pickle.load(open('high_score.dat', 'rb'))
    return high_score

def end_screen():
    picture = py.image.load('pictures/end_screen.png')
    screen.blit(picture, (0,0))
    py.display.update()
    win_sfx = py.mixer.Sound('sfx/Jingle_Win_00.wav')
    py.mixer.stop()
    py.mixer.music.stop()
    win_sfx.play()
    save_score()
    time.sleep(3)

def dead_screen():
    picture = py.image.load('pictures/dead_screen.png')
    screen.blit(picture, (0,0))
    py.display.update()


shooter_group = py.sprite.Group()
enemy_group = py.sprite.Group()
bullets = py.sprite.Group()
astroids_group = py.sprite.Group()
astroids_group2 = py.sprite.Group()

player = Player()
shooter_group.add(player)

levelspeedeasy = [1,2]
levelspeedmedium = [2]
levelspeedhard = [2,3]

explosion_ani = []
for j in range(6):
    filename = '{}.png'.format(j)
    iimg = py.image.load('pictures/explosions/{}'.format(filename)).convert()
    img = py.transform.scale(iimg,(70,70))
    img.set_colorkey(BLACK)
    explosion_ani.append(img)
    

open_score()
global high_score
start_screen()
#make stages/main loop
def easy():
    for i in range(5):
        a = Astroid(levelspeedeasy)
        enemy_group.add(a)
        astroids_group.add(a)

    for t in range(3):
        a = Astroid2(levelspeedeasy)
        enemy_group.add(a)
        astroids_group2.add(a)
    global high_score
    background = py.image.load('pictures\Background.png')
    score_font = py.font.Font("arcadeclassic\ARCADECLASSIC.TTF", 50)
    score_txt = score_font.render('Score ' + str(score), True, WHITE)
    lives_txt = score_font.render('Lives ' + str(lives), True, WHITE)
    high_score_txt = score_font.render('High Score ' + str(high_score), True, WHITE)
    stage1 = True
    clock.tick(FPS)
    while stage1:
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                stage1 = False
                exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    player.shoot()
        #if bullet it astroid
        hits = py.sprite.groupcollide(astroids_group, bullets, True, True)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            a = Astroid(levelspeedeasy)
            enemy_group.add(a)
            astroids_group.add(a)
            enemy_group.add(e)
            explosion_sfx.play()
            add(100)

        hits = py.sprite.groupcollide(astroids_group2, bullets, True, True)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            a = Astroid2(levelspeedeasy)
            enemy_group.add(a)
            astroids_group2.add(a)
            enemy_group.add(e)
            explosion_sfx.play()
            add(200)

        #if astroids hit player
        hits = py.sprite.spritecollide(player, astroids_group, True, py.sprite.collide_circle)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            enemy_group.add(e)
            hit_player_sfx.play()
            del_life()

        hits = py.sprite.spritecollide(player, astroids_group2, True, py.sprite.collide_circle)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            enemy_group.add(e)
            hit_player_sfx.play()
            del_life()

        if my_timer == 0:
            astroids_group.empty()
            astroids_group2.empty()
            enemy_group.empty()
            break

        #update
        screen.fill(BLACK)
        score_txt = score_font.render('Score ' + str(score), True, WHITE)
        lives_txt = score_font.render('Lives ' + str(lives), True, WHITE)
        high_score_txt = score_font.render('High Score ' + str(high_score), True, WHITE)
        screen.blit(background,(0,100))
        screen.blit(score_txt, (10,10))
        screen.blit(lives_txt, (10,40))
        screen.blit(high_score_txt, (350,10))
        shooter_group.update()
        enemy_group.update()
        
        #draw / render
        shooter_group.draw(screen)
        enemy_group.draw(screen)
         
        #flip
        py.display.flip()
        


def medium():
    for i in range(4):
        a = Astroid(levelspeedmedium)
        enemy_group.add(a)
        astroids_group.add(a)

    for t in range(5):
        a = Astroid2(levelspeedmedium)
        enemy_group.add(a)
        astroids_group2.add(a)
    global high_score
    background = py.image.load('pictures\Background.png')
    score_font = py.font.Font("arcadeclassic\ARCADECLASSIC.TTF", 50)
    score_txt = score_font.render('Score ' + str(score), True, WHITE)
    lives_txt = score_font.render('Lives ' + str(lives), True, WHITE)
    high_score_txt = score_font.render('High Score ' + str(high_score), True, WHITE)
    medium_txt = score_font.render('Medium', True, WHITE)
    stage1 = True
    clock.tick(FPS)
    screen.blit(medium_txt, (350,350))
    py.display.update()
    time.sleep(1)
    while stage1:
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                stage1 = False
                exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    player.shoot()
        #if bullet it astroid
        hits = py.sprite.groupcollide(astroids_group, bullets, True, True)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            a = Astroid(levelspeedmedium)
            enemy_group.add(a)
            astroids_group.add(a)
            enemy_group.add(e)
            explosion_sfx.play()
            add(150)

        hits = py.sprite.groupcollide(astroids_group2, bullets, True, True)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            a = Astroid2(levelspeedmedium)
            enemy_group.add(a)
            astroids_group2.add(a)
            enemy_group.add(e)
            explosion_sfx.play()
            add(250)

        #if astroids hit player
        hits = py.sprite.spritecollide(player, astroids_group, True, py.sprite.collide_circle)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            enemy_group.add(e)
            hit_player_sfx.play()
            del_life()

        hits = py.sprite.spritecollide(player, astroids_group2, True, py.sprite.collide_circle)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            enemy_group.add(e)
            hit_player_sfx.play()
            del_life()

        if my_timer == 0:
            astroids_group.empty()
            astroids_group2.empty()
            enemy_group.empty()
            break

        #update
        screen.fill(BLACK)
        score_txt = score_font.render('Score ' + str(score), True, WHITE)
        lives_txt = score_font.render('Lives ' + str(lives), True, WHITE)
        high_score_txt = score_font.render('High Score ' + str(high_score), True, WHITE)
        screen.blit(background,(0,100))
        screen.blit(score_txt, (10,10))
        screen.blit(lives_txt, (10,40))
        screen.blit(high_score_txt, (350,10))
        shooter_group.update()
        enemy_group.update()
        
        #draw / render
        shooter_group.draw(screen)
        enemy_group.draw(screen)
         
        #flip
        py.display.flip()


def hard():
    for i in range(2):
        a = Astroid(levelspeedeasy)
        enemy_group.add(a)
        astroids_group.add(a)

    for t in range(7):
        a = Astroid2(levelspeedeasy)
        enemy_group.add(a)
        astroids_group2.add(a)
    global high_score
    background = py.image.load('pictures\Background.png')
    score_font = py.font.Font("arcadeclassic\ARCADECLASSIC.TTF", 50)
    score_txt = score_font.render('Score ' + str(score), True, WHITE)
    lives_txt = score_font.render('Lives ' + str(lives), True, WHITE)
    high_score_txt = score_font.render('High Score ' + str(high_score), True, WHITE)
    hard_txt = score_font.render('Hard', True, WHITE)
    stage1 = True
    clock.tick(FPS)
    screen.blit(hard_txt, (350,350))
    py.display.update()
    time.sleep(1)
    while stage1:
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                stage1 = False
                exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    player.shoot()
        #if bullet it astroid
        hits = py.sprite.groupcollide(astroids_group, bullets, True, True)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            a = Astroid(levelspeedeasy)
            enemy_group.add(a)
            astroids_group.add(a)
            enemy_group.add(e)
            explosion_sfx.play()
            add(250)

        hits = py.sprite.groupcollide(astroids_group2, bullets, True, True)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            a = Astroid2(levelspeedeasy)
            enemy_group.add(a)
            astroids_group2.add(a)
            enemy_group.add(e)
            explosion_sfx.play()
            add(300)

        #if astroids hit player
        hits = py.sprite.spritecollide(player, astroids_group, True, py.sprite.collide_circle)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            enemy_group.add(e)
            hit_player_sfx.play()
            del_life()

        hits = py.sprite.spritecollide(player, astroids_group2, True, py.sprite.collide_circle)
        for hit in hits:
            e = Explosion(hit.rect.centerx, hit.rect.centery)
            enemy_group.add(e)
            hit_player_sfx.play()
            del_life()
        if my_timer == 0:
            astroids_group.empty()
            astroids_group2.empty()
            enemy_group.empty()
            break

        #update
        screen.fill(BLACK)
        score_txt = score_font.render('Score ' + str(score), True, WHITE)
        lives_txt = score_font.render('Lives ' + str(lives), True, WHITE)
        high_score_txt = score_font.render('High Score ' + str(high_score), True, WHITE)
        screen.blit(background,(0,100))
        screen.blit(score_txt, (10,10))
        screen.blit(lives_txt, (10,40))
        screen.blit(high_score_txt, (350,10))
        shooter_group.update()
        enemy_group.update()
        
        #draw / render
        shooter_group.draw(screen)
        enemy_group.draw(screen)
         
        #flip
        py.display.flip()

def timer():
    global my_timer

    my_timer= 20

    for x in range(20):
        my_timer -= 1 
        time.sleep(1)

    print('Round finished')

timer_thread = threading.Thread(target = timer)
timer_thread.start()

while my_timer > 0:
    easy()
    if my_timer == 0:
        break

timer_thread2 = threading.Thread(target = timer)
timer_thread2.start()

while my_timer > 0:
    medium()
    if my_timer == 0:
        break

timer_thread3 = threading.Thread(target = timer)
timer_thread3.start()

while my_timer > 0:
    hard()
    if my_timer == 0:
        end_screen()
        exit()
        break