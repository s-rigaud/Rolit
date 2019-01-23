import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode([700, 700])

window.fill((70, 70, 70))


pygame.draw.arc(window, (0, 0, 0), ((-250, -250), (1150, 1150)), -1.5, 0, 180)


# to 8 for 8*8 / to 5 for 5*5
[pygame.draw.circle(window, (30, 30, 30), (16 + 32 + 85*i, 16 + 32 + 85*y), 37, 0) for i in range(8) for y in range(8)]
[pygame.draw.circle(window, (227, 216, 176), (16 + 32 + 85*i, 16 + 32 + 85*y), 32, 0) for i in range(8) for y in range(8)]
pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.image.save(window, 'board_test.png')
            pygame.quit()
