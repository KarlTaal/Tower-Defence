import pygame
import ctypes
import random
import time

pygame.init()

FPS = 60
clock = pygame.time.Clock()


#VÕTAB ARVUTI EKRAANI MÕÕTME JA LOOB MÄNGU EKRAANI SUURUSE 
ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
mängu_screen = pygame.display.set_mode(true_res,pygame.FULLSCREEN)

#Kogu ekraani suurused
x_global = int(true_res[0])  #1920
y_global = int(true_res[1])  #1080


#MÄNGU NIMI
pygame.display.set_caption("TOWER DEFENCE")

#LAEB PILDID JA MUUDAB NEED SOBIVAKS SUURUSEKS
taust = pygame.image.load("images/taust.png")
taust = pygame.transform.scale(taust, (x_global, y_global))

vasak_torn = pygame.image.load("images/vasak_torn.png")
vasak_torn = pygame.transform.scale(vasak_torn, (int(0.15 * y_global), int(0.15 * x_global)))

parem_torn = pygame.image.load("images/parem_torn.png")
parem_torn = pygame.transform.scale(parem_torn, (int(0.15 * y_global), int(0.15 * x_global)))

mehikese_pildid = [pygame.image.load("images/mehike/mehike1.png"), pygame.image.load("images/mehike/mehike2.png"), pygame.image.load("images/mehike/mehike3.png"),\
pygame.image.load("images/mehike/mehike4.png"), pygame.image.load("images/mehike/mehike5.png"), pygame.image.load("images/mehike/mehike6.png"),\
pygame.image.load("images/mehike/mehike7.png"), pygame.image.load("images/mehike/mehike8.png")]
mehike_walkRight = []
mehike_walkLeft = []
for mehike in mehikese_pildid:
    mehike_walkRight.append(pygame.transform.scale(mehike, (int(0.07 * x_global), int(0.13 * y_global))))
for mehike in mehike_walkRight:
    mehike_walkLeft.append(pygame.transform.flip(mehike, True, False))


class Player2(pygame.sprite.Sprite):
    def __init__(self, position, mehike_walkLeft):
        super(Player2, self).__init__()
        size = (int(0.07 * x_global), int(0.13 * y_global))
        self.rect = pygame.Rect(position, size)
        self.images = mehike_walkLeft
        self.index = 0
        self.image = mehike_walkLeft[self.index]
        self.velocity = pygame.math.Vector2(0, 0)
        self.animation_time = 0.1
        self.current_time = 0

    def update_time_dependent(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update(self, dt):
        self.update_time_dependent(dt)
        self.rect.x -= 5
def player2():
    player2 = Player2(position=(x_global - int(0.07 * x_global) , y_global * 0.76), mehike_walkLeft=mehike_walkLeft)
    player_list2.add(player2)


class Player(pygame.sprite.Sprite):
    def __init__(self, position, mehike_walkRight):
        super(Player, self).__init__()
        size = (int(0.07 * x_global), int(0.13 * y_global))
        self.rect = pygame.Rect(position, size)
        self.mehike_walkRight = mehike_walkRight
        self.index = 0
        self.image = mehike_walkRight[self.index]
        self.velocity = pygame.math.Vector2(0, 0)
        self.animation_time = 0.1
        self.current_time = 0

    def update_time_dependent(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.mehike_walkRight)
            self.image = self.mehike_walkRight[self.index]

    def update(self, dt):
        self.update_time_dependent(dt)
        self.rect.x += 5
def player():
    player = Player(position=(0, y_global * 0.76), mehike_walkRight=mehike_walkRight)
    player_list.add(player)


def kokkupuude():
    player_hit_list = pygame.sprite.groupcollide(player_list, player_list2, False, False, collided=None)
    for i in player_hit_list:
        suvaline = random.randint(0,2)
        if suvaline == 0:
            player_list.remove(i)
        elif suvaline == 1:
            player_list2.remove(player_hit_list[i])



def draw():

    mängu_screen.blit(taust, (0, 0))
    player_list.update(dt)
    player_list2.update(dt)
    player_list.draw(mängu_screen)
    player_list2.draw(mängu_screen)
    mängu_screen.blit(vasak_torn, (0, 0.635 * y_global))
    mängu_screen.blit(parem_torn, (x_global - int(0.15 * y_global), 0.635 * y_global))
    pygame.display.update()







player_list2 = pygame.sprite.Group()
player_list = pygame.sprite.Group()
a = True
while a:
    dt = clock.tick(FPS) / 1000

    kokkupuude()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            a = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player()
            if event.key == pygame.K_s:
                player2()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                a = False


    draw()

pygame.quit()