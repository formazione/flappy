import pygame
from glob import glob
import random


size = w, h = 400, 600
screen = pygame.display.set_mode((size), 32, 1)
pygame.display.set_caption("Flappy Py")



class Sprite(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        super(Sprite, self).__init__()
        global flappy, g, pipes

        self.x = x
        self.y = y
        self.frames = [load(f[:-4]) for f in glob(file + "*.png")]
        self.image = self.frames[0]
        self.rect = pygame.Rect(self.x, self.y, 32, 24)
        self.cnt = 0
        g.add(self)

    def update(self):
        self.cnt += .1
        if self.cnt > len(self.frames) - 1:
            self.cnt = 0
        self.image = self.frames[int(self.cnt)]
        self.collision()

    def collision(self):
        global moveup
        global flappy, g, pipes

        for pipe in pipes:
            if self.rect.colliderect(pipe):
                moveup = 1
                # self.gameover()

    def gameover(self):
        print("Game over")


class Bg(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        global flappy, g, pipes

        super(Bg, self).__init__()
        self.x = x
        self.y = y
        self.image = load(file)
        self.rect = pygame.Rect(self.x, self.y, 400, 600)
        g.add(self)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, file, x, y, pos="down"):
        global flappy, g, pipes

        super(Pipe, self).__init__()
        self.x = x + 300
        self.y = 100
        self.pos = pos
        if self.pos == "down":
            self.image = load(file)
        if self.pos == "up":
            self.image = flip(file)
        self.make_rect()
        g.add(self)
        pipes.add(self)

    def make_rect(self):
        self.w, self.h = self.image.get_size()
        if self.pos == "up":
            self.y -= 100
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.random_position()

    def update(self):
        self.rect.left -= 1
        if self.rect.left < -52:
            self.rect.left = 548
            self.random_position()

    def random_position(self):
        self.y = random.randrange(550, 300, -10)
        if self.pos == "down":
            self.rect.top = self.y
        if self.pos == "up":
            self.rect.bottom = self.y - 100


class Base(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        super(Base, self).__init__()
        self.x = x
        self.y = y
        self.image = load(file)
        self.rect = pygame.Rect(self.x, self.y, 400, 41)
        g.add(self)
        pipes.add(self)

    def update(self):
        self.rect.left -= 1
        if self.rect.left < -400:
            self.rect.left = 399



def load(file):
    return pygame.image.load(file + ".png")


def flip(file):
    return pygame.transform.flip(load(file), 0, 1)


def gravity():
    flappy.rect.top += 1


def start():
    global flappy, g, pipes

    g = pygame.sprite.Group()
    pipes = pygame.sprite.Group()
    Bg("bg", 0, 0)
    # pipes down
    [Pipe("pipe", 200 * x, 400) for x in range(3)]
    [Pipe("pipe", 200 * x, 400, "up") for x in range(3)]
    # The basement
    Base("base", 400, 560)
    Base("base", 0, 560)
    # ============= FLAPPY BIRD SPRITE
    flappy = Sprite("blue", 50, 300)
    main()

def main():
    global moveup, flappy, g, pipes

    # jump controlo variables:
    # - after you press
    moveup = 0
    # how high can go
    startcounter = 0
    # How hight flappy jumps
    topjump = 40
    # how speed it jumps
    jumpspeed = 2

    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    loop = 1
    while loop:

        if moveup:
            flappy.rect.top -= jumpspeed
            startcounter += 1
            print(startcounter)
        if startcounter == topjump:
            startcounter = 0
            moveup = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_UP:
                    moveup = 1
                    startcounter = 1
                if event.key == pygame.K_s:
                    start()

        g.draw(screen)
        g.update()
        if not moveup:
            gravity()
        pygame.display.update()
        clock.tick(120)

    pygame.quit()


start()

