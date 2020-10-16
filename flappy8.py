import pygame
from glob import glob
import random
from functions.score import *
from fastcore.test import *


#
# - added sound
# - added font and score on screen
# - save record
#

pygame.init()
pygame.font.init()
size = w, h = 400, 600
screen = pygame.display.set_mode((size), 32, 1)
pygame.display.set_caption("Flappy Py")
# 
game = Score("score.txt")
# ================== MUSIC ===================== #
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)

# ===============================================
jump = pygame.mixer.Sound("sounds/jump.wav")
jump.set_volume(0.5)
hit = pygame.mixer.Sound("sounds/hit.wav")
hit.set_volume(0.3)
# To play a sound use: play(jump)


def play(snd):
    "Plays one of the sounds in the sounds folder using play('name')"
    pygame.mixer.Sound.play(snd)
# ============================================== #

# List of songs for the soundtrack
base = pygame.mixer.music
music = ["sounds/" + f
for f in os.listdir("sounds/")
if f.startswith("base")]

# ================================================= Soundtrack
def load_random_song():
    song = random.choice(music)
    return song

def soundtrack(play="yes", loop=1):
    "This load a base from sounds directory"
    filename = load_random_song()
    if play == "yes":
        base.load(filename)
    elif play == "stop" and filename != None:
        base.stop()
    if loop == 1 and play == "yes":
        base.play(-1)

# ================================================= Soundtrack

font = pygame.font.SysFont("Arial", 16)


def write(text_to_show, color="Coral"):
    'write("Start")'
    text = font.render(text_to_show, 1, pygame.Color(color))
    return text


class Sprite(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        super(Sprite, self).__init__()
        global g

        self.x = x
        self.y = y
        self.frames = [load(f[:-4]) for f in glob(file + "*.png")]
        self.framesup = [rotate(f[:-4], 45) for f in glob(file + "*.png")]
        self.image = self.frames[0]
        self.imagefall = rotate("fall", -45)
        self.imagespeed = load("speed")

        self.rect = pygame.Rect(self.x, self.y, 32, 24)
        self.cnt = 0
        self.score = 0
        self.maxscore = int(game.maxscore)
        self.mask = self.make_mask()
        g.add(self)

    def make_mask(self):
        return pygame.mask.from_surface(self.image)

    def update(self):
        global moveup, gameover
        # when moveup animation's faster
        self.cnt += .1
        if self.cnt > len(self.frames) - 1:
            self.cnt = 0
        if not moveup:
            self.image = self.frames[int(self.cnt)]
        else:
            self.image = self.framesup[int(self.cnt)]
        if not gameover:
            self.score += 1
        self.check_collision()


    def check_collision(self):
        global gameover

        for pipe in pipes:
            if pygame.sprite.collide_mask(pipe, self):
                if gameover == 0:
                    play(hit)
                    if self.score > self.maxscore:
                        game.save_score(self.score)
                gameover = 1





class Bg(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        global g

        super(Bg, self).__init__()
        
        self.x = x
        self.y = y
        self.image = load(file)
        self.rect = pygame.Rect(self.x, self.y, w, h)
        g.add(self)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, file, x, y, pos=0):
        global g, pipes, lasty

        super(Pipe, self).__init__()

        self.x = x + 300
        self.pos = pos
        self.y = random.randint(300, 400)
        self.speed = 1

        if self.pos == 0:
            self.image = load(file)
            self.rect = pygame.Rect(self.x, self.y, 52, 320)
        else:
            self.image = flip(file)
            self.rect = pygame.Rect(self.x, self.y, 52, 320)
            self.rect.bottom = self.y - random.randint(150, 300)
        pipes.add(self)
        g.add(self)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if flappy.score == 1000:
            if self.pos == 0:
                self.image = load("pipe2")
            else:
                self.image = flip("pipe2")

        if flappy.score > 2500:
            if random.random() < .5:
                self.rect.top -= 1
            else:
                self.rect.top += 1
        self.rect.left -= self.speed
        if self.rect.left < -100:
            self.rect.left = 400
            self.y = random.randint(300, 400)
            if self.pos == 0:
                self.rect.top = self.y
            else:
                # DISTANCE AMONG PIPES
                self.rect.bottom = self.y - random.randint(150 - flappy.score // 100, 300 - flappy.score // 100)



class Base(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        global g

        super(Base, self).__init__()
        self.x = x
        self.y = y
        self.image = load(file)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.speed = 1
        g.add(self)

    def update(self):
        self.rect.left -= self.speed
        if self.rect.left < -400:
            self.rect.left = 399


def load(file):
    return pygame.image.load(file + ".png")


def flip(file):
    return pygame.transform.flip(load(file), 0, 1)


def rotate(file, angle):
    return pygame.transform.rotate(load(file), angle)


def gravity(sprite):
    sprite.rect.top += 1

# =========================== Tutorial 3 - change 1


def start():
    global g, pipes, flappy, b1, b2

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

    b1 = Base("base", 400, 570)
    b2 = Base("base", 0, 570)
    flappy = Sprite("blue", 50, 300)
    main()


def main():
    global moveup, gameover
    global g, pipes, flappy, b1, b2

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
    screen.fill((0, 0, 0))
    # ============ p.5
    text = write("Score")
    clock = pygame.time.Clock()
    loop = 1
    speedup = 0

    while loop:

        if flappy.score % 2500 == 0:
            soundtrack()

        if speedup:
            b1.speed = 10
            b2.speed = 10
            for pipe in pipes:
                pipe.speed = 10
                moveup = 1
            flappy.image = flappy.imagespeed
        else:
            b1.speed = 1
            b2.speed = 1
            for pipe in pipes:
                pipe.speed = 1

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
            if flappy.rect.top > 600:
                flappy.kill()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                play(jump)
                moveup = 1
                startcounter = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    play(jump)
                    moveup = 1
                    startcounter = 1
                if event.key == pygame.K_RIGHT:
                    play(jump)
                    speedup = 1
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_m or event.key == pygame.K_s:
                    menu()
            if event.type == pygame.KEYUP:
                moveup = 0
                speedup = 0
            if event.type == pygame.MOUSEBUTTONUP:
                moveup = 0


        g.draw(screen)
        g.update()
        
        screen.blit(flappy.image, (0, 0))
        screen.blit(text, (50, 0))
        screen.blit(write(str(flappy.score), color="White"), (100, 0))
        screen.blit(write(str(flappy.maxscore), color="White"), (150, 0))

        if not moveup:
            gravity(flappy)
        pygame.display.update()
        clock.tick(120)

    pygame.quit()


def menu():

    "This is the menu that waits you to click the s key to start"
    bb = pygame.image.load("bg.png")
    fl = pygame.image.load("bluebird-downflap.png")
    screen.blit(bb, (0, 0))
    screen.blit(fl, (100, 300))
    screen.blit(write("Flappy Pygame"), (10, 0))
    screen.blit(write("Press any Key"), (10, 50))
    screen.blit(write("Press m to come back to this menu"), (10, 80))
    screen.blit(write("Press arrow key up to fly up and arrow key right to fly fast"), (10, 200))
    
    soundtrack()

    loop1 = 1
    while loop1:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                loop1 = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                play(jump)
                moveup = 1
                startcounter = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    play(jump)
                    moveup = 1
                    startcounter = 1
                if event.key == pygame.K_RIGHT:
                    play(jump)
                    speedup = 1
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_m or event.key == pygame.K_s:
                    menu()
            if event.type == pygame.KEYUP:
                moveup = 0
                speedup = 0
            if event.type == pygame.MOUSEBUTTONUP:
                moveup = 0

        g.draw(screen)
        g.update()
        
        screen.blit(flappy.image, (0, 0))
        screen.blit(text, (50, 0))
        screen.blit(write(str(flappy.score), color="White"), (100, 0))
        screen.blit(write(str(flappy.maxscore), color="White"), (150, 0))

        if not moveup:
            gravity(flappy)
        pygame.display.update()
        clock.tick(120)

    pygame.quit()


def menu():

    "This is the menu that waits you to click the s key to start"
    bb = pygame.image.load("bg.png")
    fl = pygame.image.load("bluebird-downflap.png")
    screen.blit(bb, (0, 0))
    screen.blit(fl, (100, 300))
    screen.blit(write("Flappy Pygame"), (10, 0))
    screen.blit(write("Press any Key"), (10, 50))
    screen.blit(write("Press m to come back to this menu"), (10, 80))
    screen.blit(write("Press arrow key up to fly up and arrow key right to fly fast"), (10, 200))
    
    soundtrack()

    loop1 = 1
    while loop1:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                loop1 = 0
            if event.type == pygame.KEYDOWN:
                press_escape = event.key == pygame.K_ESCAPE
                if press_escape:
                    loop1 = 0

                start()
        pygame.display.update()

    pygame.quit()


menu()