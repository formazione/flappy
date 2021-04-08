import pygame
import random



particles1 = []
particles2 = []
particles3 = []
def particles_run(particles, pos, color):
    particles.append([
    	[random.randint(0, 300), # it was centered at 150
    	0],
    	[random.randint(0, 20) / 10 - 1, 2],
    	random.randint(4,6)])
    for particle in particles[:]:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.005 # how fast circles shrinks
        particle[1][1] += 0.01 # circles speed
        if particle[2] <= 0:
            particles.remove(particle)
    for particle in particles:
        pygame.draw.circle(
            screen, (color),
        (round(particle[0][0]), round(particle[0][1])),
         round(particle[2]))