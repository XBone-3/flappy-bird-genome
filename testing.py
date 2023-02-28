import pygame
import random
import cnfg
import time
import sys
pygame.init()
tic = 0
win = pygame.display.set_mode((cnfg.SCREEN_WIDTH, cnfg.SCREEN_HEIGHT))
pygame.display.set_caption('flappy bird')
bird_img = pygame.image.load(cnfg.BIRD[0])
bird_rect = bird_img.get_rect()
bird_rect.x = 100
bird_rect.y = 100
clock = pygame.time.Clock()
vel = -10.5
while True:
	clock.tick(60)
	win.fill(0)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	tic += 1
	disp = vel * tic + 1.5 * tic ** 2
	bird_rect.y += int(disp)
	win.blit(bird_img, (bird_rect.x, bird_rect.y))
	pygame.display.update()

