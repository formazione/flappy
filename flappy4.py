import pygame
from glob import glob
import random

size = w, h = 400, 600
screen = pygame.display.set_mode((size))
pygame.display.set_caption("Flappy Py")


class Sprite(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        super(Sprite, self).__init__()
        global g

        self.x = x
        self.y = y
        self.frames = [load(f[:-4]) for f in glob(file + "*.png")]
        self.image = self.frames[0]
        self.imagefall = load("fall")
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.cnt = 0
        self.score = 0
        self.mask = pygame.mask.from_surface(self.image)
        g.add(self)

    def update(self):
        global moveup, gameover
        # when moveup animation's faster
        if not moveup:
            self.cnt += .1
        if self.cnt > len(self.frames) - 1:
            self.cnt = 0
        self.image = self.frames[int(self.cnt)]
        if not gameover:
            self.score += 1
        pygame.display.set_caption(str(self.score))
        self.check_collision()

    def check_collision(self):
        global moveup, gameover

        for pipe in pipes:
            if pygame.sprite.collide_mask(pipe, self):
                print("touched")
                gameover = 1




class Bg(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        global g

        super(Bg, self).__init__()
        self.x = x
        self.y = y
        self.image = load(file)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        g.add(self)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, file, x, y, pos=0):
        global g, pipes, lasty

        super(Pipe, self).__init__()

        self.x = x + 300
        self.pos = pos
        self.y = random.randint(300, 400)

        if self.pos == 0:
            self.image = load(file)
            self.rect = pygame.Rect(self.x, self.y, 52, 320)
        else:
            self.image = flip(file)
            self.rect = pygame.Rect(self.x, self.y, 52, 320)
            self.rect.bottom = self.y - random.randint(200, 300)
        pipes.add(self)
        g.add(self)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):

        self.rect.left -= 1
        if self.rect.left < -100:
            self.rect.left = 400
            self.y = random.randint(300, 400)
            if self.pos == 0:
                self.rect.top = self.y
            else:
                self.rect.bottom = self.y - random.randint(200, 300)



class Base(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        global g

        super(Base, self).__init__()
        self.x = x
        self.y = y
        self.image = load(file)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        g.add(self)

    def update(self):
        self.rect.left -= 1
        if self.rect.left < -400:
            self.rect.left = 399


def load(file):
    return pygame.image.load(file + ".png")


def flip(file):
    return pygame.transform.flip(load(file), 0, 1)


def gravity(sprite):
    sprite.rect.top += 1

# =========================== Tutorial 3 - change 1


def start():
    global g, pipes, flappy

    g = pygame.sprite.Group()
    Bg("bg", 0, 0)
    pipes = pygame.sprite.Group()
    Pipe("pipe", 100, 300, 0)
    Pipe("pipe", 200, 300, 0)
    Pipe("pipe", 300, 300, 0)
    Pipe("pipe", 400, 300, 0)
    Pipe("pipe", 500, 300, 0)
    # Upside down
    Pipe("pipe", 100, 0, 1)
    Pipe("pipe", 200, 0, 1)
    Pipe("pipe", 300, 0, 1)
    Pipe("pipe", 400, 0, 1)
    Pipe("pipe", 500, 0, 1)

    Base("base", 400, 570)
    Base("base", 0, 570)
    flappy = Sprite("blue", 50, 300)
    main()


def main():
    global moveup, gameover
    global g, pipes, flappy

    # jump controlo variables:
    # - after you press
    moveup = 0

    # =================== tutorial 4 - change 1
    gameover = 0
    # how high can go
    startcounter = 0
    # How hight flappy jumps
    topjump = 30
    # how speed it jumps
    jumpspeed = 2
    screen.fill((0,0,0))
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    loop = 1
    while loop:

        if moveup:
            flappy.rect.top -= jumpspeed
            startcounter += 1
            # fly faster
            flappy.cnt += .5
            # print(startcounter)
        if startcounter == topjump:
            startcounter = 0
            moveup = 0

        if gameover:
            # cannot fly
            moveup = 0
            # goes down
            flappy.rect.top += 1
            flappy.cnt = 0
            flappy.image = flappy.imagefall


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    moveup = 1
                    startcounter = 1
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_s:
                    start()


        g.draw(screen)
        g.update()
        if not moveup:
            gravity(flappy)
        pygame.display.update()
        clock.tick(120)

    pygame.quit()


start()


