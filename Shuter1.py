from pygame import*
from random import*
mixer.init()#підключаємо музтку в пайгейм
sound = mixer.Sound("fon.ogg")#завантажуєм пісню
lose = mixer.Sound("lost.ogg")
win = mixer.Sound("win.ogg")

mixer.music.load("fon.ogg")#завантажуємо фонову музику
mixer.music.set_volume(0.5)#визначаємо гучність
mixer.music.play()#вмикаємо звук

w = 900 
h = 600 
clock = time.Clock()
window = display.set_mode((w, h))
bullets = sprite.Group()#група куль
background = transform.scale(image.load("kosmos.jpg"), (w, h))
lost = 0
score = 0

font.init()
font1 = font.Font(None, 50)
win = font1.render("YOU WIN!", True, (232, 251, 200))
lose = font1.render("YOU LOST!", True, (232, 251, 200))
score_text = font1.render(str(score), True,(250,250,250))




class Player(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(100,100))
        self.speed = player_speed
        self.rect = self.image.get_rect()#створити хітбокс
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Hero(Player):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self .speed
        if keys[K_d] and self.rect.x < 850:
            self.rect.x += self.speed
    def fire(self):
        b = Bullet("bullet.png", self.rect.centerx, self.rect.top, 5)
        bullets.add(b)

class Enemy(Player):
    def update(self):
        self.rect.y = self.rect.y + self.speed
        global lost
        if self.rect.y > h:
            self.rect.x = randint(80,520)
            self.rect.y = 0
            lost += 1

class Bullet(Player):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

hero = Hero("rocket.png",300,500,5)

enemies = sprite.Group()
#створення групи монстрів
for i in range (3):
    monster = Enemy("enem.png", randint(50,850), -50, randint(1,1))
    enemies.add(monster)


display.set_caption("Shooter")
game = True
finish = False
FPS = 80

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
    if finish != True:
        score_text = font1.render("Score:"+str(score), True,(220,20,60)) #створюємо текст рахунок і кількість очок на екрані
        window.blit(background, (0,0))
        window.blit(score_text, (0,100))
        enemies.update()
        bullets.update()
        hero.update()
        hero.reset()
        enemies.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(enemies,bullets,True,True)
        for c in collides:
            score = score + 1
            monster = Enemy("enem.png", randint(50,850), -50, randint(1,2))
            enemies.add(monster)
        if sprite.spritecollide(hero, enemies, False) or lost>=5:
            finish = True
            mixer.music.load("lost.ogg")
            mixer.music.set_volume(0.5)
            mixer.music.play()
            window.blit(lose, (350,100))
        if score>=10:
            window.blit(win, (350,100))
            finish = True
            
        
    
    display.update()
    clock.tick(FPS)
     


    