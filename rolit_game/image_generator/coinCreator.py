import pygame
from pygame.locals import *


pygame.init()
window = pygame.display.set_mode([64, 64])

window.fill((255, 255, 255))

original_color = (50, 50, 50)
r = original_color[0]
g = original_color[1]
b = original_color[2]

pygame.draw.circle(window, (r,g,b), (32, 32), 32, 0)
pygame.draw.arc(window, (r - 50, g - 50, b - 50), ((6, 6),(55, 57)), -2.4, 0, 4)
pygame.draw.arc(window, (r + 50, g + 50, b + 50), ((5, 5),(50, 54)), 1, 3, 4)
pygame.display.update()


while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.image.save(window, 'coin_test.png')
			pygame.quit()
