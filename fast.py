from pygame import *
from time import time as timer

mixer.init()

mixer.music.load("music.mp3")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")


img_back = "fon.png"
img_enemy = "rock.png"
img_ast = "tree.png"
img_bullet = "bullet.png"
score = 0
lost = 0
max_lost = 3
goal = 10
life = 3
num_fire = 0
rel_time = False
font.init()
font1 = font.SysFont("Arial",80)
win = font1.render("You win",True,(255,255,255))
lose = font1.render("You lose",True,(120,0,0))
font2 = font.SysFont("Arial",36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x = self.rect.x - self.speed
        if keys[K_RIGHT] and self.rect.x <620:
            self.rect.x = self.rect.x + self.speed


from random import randint
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,620)
            self.rect.y = 0
            lost = lost + 1

win_width = 700
win_height = 500
display.set_caption("Runner")
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load(img_back),(win_width,win_height))
img_hero = "rman.png"
ship = Player(img_hero,5,400,80,100,10)
bullets = sprite.Group()
monsters = sprite.Group()

for i in range(1,3):
    monster = Enemy(img_enemy,randint(-20,620),-100,100,100,randint(5,15))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(img_ast,randint(-20,670),-40,80,140,randint(5,15))
    asteroids.add(asteroid)
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        window.blit(background,(0,0))
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        ship.reset()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                nothing = font2.render(".", 1,(150,0,0))
                window.blit(nothing,(260,460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1 
            monster = Enemy(img_enemy,randint(80,620),-40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life = life - 1
            if life == 0 :
                finish = True
                window.blit(lose,(200,200 ))
        if score >= goal:
            finish = True
            window.blit(win,(200,200))
        text_score = font2.render("" ,1,(0,0,255))
        window.blit(text_score,(10,20))
        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (255,255,0)
        if life == 1:
            life_color = (150,0,0)
        text_life = font2.render("Life: "+str(life),1,life_color)
        window.blit(text_life,(590,20))
        display.update()
    else:
        pass
    time.delay(30)
