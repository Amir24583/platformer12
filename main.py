import pygame
from pygame.locals import *
import random 
import sys


pygame.init()
vec = pygame.math.Vector2 

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (10, 420))

        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.score = 0 

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0 :
            if hits:
               if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:   
                        hits[0].point = False  
                        self.score += 1
                    self.vel.y = 0
                    self.pos.y = hits[0].rect.top + 1
                     

    def scoreprint(self):    
        print(f"you got {self.score} points") 

    def printY(self):
        print(f"Your at {self.pos.y}")




    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -15

    def move(self):
        self.acc = vec(0,0.5) 

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC 

        self.acc.x += self.vel.x * FRIC    
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos    

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((0,255,0)) 
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10), random.randint(0, HEIGHT-30)))

        self.point = True 


    def move(self):
        pass     




PT1 = platform() 
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))   
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))  
P1 = Player()
platforms = pygame.sprite.Group()
platforms.add(PT1)
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50,100)
        p = platform()
        C = True
        tries = 0

        while C and tries < 3:
            tries += 1
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 0))
            C = check(p, platforms)


        platforms.add(p)
        all_sprites.add(p)
        

def check(platform, platformgroup):
    if pygame.sprite.spritecollideany(platform, platformgroup):
        return True
    else:
        for entity in platformgroup:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 50) and (abs(platform.rect.bottom - entity.rect.top) < 50):
                return True
        C = False


for x in range(random.randint(5, 6)):
    pl = platform()
    platforms.add(pl)
    all_sprites.add(pl)

while True: 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
    if P1.rect.top <= HEIGHT /3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
    if P1.pos.y > 450:
        P1.kill()
        print("GAME OVER")
        pygame.quit()
        sys.exit()
        




    displaysurface.fill((0,0,0))

    P1.printY()
    P1.update()
    P1.scoreprint()
    plat_gen()
    for entity in all_sprites:
        displaysurface.blit(entity.surf,entity.rect)
        entity.move()


   

    pygame.display.update()
    FramePerSec.tick(FPS)
