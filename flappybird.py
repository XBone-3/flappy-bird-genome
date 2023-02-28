import pygame
import os
import random

WIDTH = 600
HEIGHT = 900
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load('imgs\\bird1.png')),
             pygame.transform.scale2x(pygame.image.load('imgs\\bird2.png')),
             pygame.transform.scale2x(pygame.image.load('imgs\\bird3.png'))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load('imgs\\pipe.png'))
BASE_IMG = pygame.transform.scale2x(pygame.image.load('imgs\\base.png'))
BG_IMG = pygame.transform.scale(pygame.image.load('imgs\\bg.png'), (600, 900))
pygame.font.init()
STAT_FONT = pygame.font.SysFont('comicsans', 50)

class Bird():
	IMGS = BIRD_IMGS
	MAX_ROTATION = 25
	ROTATION_VEL = 20
	ANIMATION_TIME = 5


	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tilt = 0
		self.img = self.IMGS[0]
		self.img_count = 0
		self.tick_count = 0
		self.velocity = 0
		self.height = self.y


	def move(self):
		self.tick_count += 1
		displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2
		if displacement >= 16:
			displacement = 16
		if displacement <= 0:
			displacement -= 2
		self.y = self.y + displacement
	def draw(self, play_window):
		self.img_count += 1
		if self.img_count <= self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count <= self.ANIMATION_TIME * 2:
			self.img = self.IMGS[1]
		elif self.img_count <= self.ANIMATION_TIME * 3:
			self.img = self.IMGS[2]
		elif self.img_count <= self.ANIMATION_TIME * 4:
			self.img = self.IMGS[1]
		elif self.img_count <= self.ANIMATION_TIME * 5:
			self.img = self.IMGS[0]
			self.img_count = 0
		play_window.blit(self.img, (round(self.x), round(self.y)))


	def jump(self):
		self.velocity = -10.5
		self.height = self.y
		self.tick_count = 0


	def get_mask(self):
		return pygame.mask.from_surface(self.img)


class Pipe():
	GAP = 200
	VELOCITY = 5


	def __init__(self, x):
		self.x = x
		self.pipe_bottom_img = PIPE_IMG
		self.pipe_top_img = pygame.transform.flip(PIPE_IMG, False, True)
		self.height = 0
		self.top_pipe_height = 0 # initial co-ordinate point
		self.bottom_pipe_height = 0 # initial co-ordinate point
		self.passed = False
		self.set_height()


	def set_height(self):
		self.height = random.randint(45, 450)
		self.top_pipe_height = self.height - self.pipe_top_img.get_height()
		self.bottom_pipe_height = self.height + self.GAP


	def move(self):
		self.x = self.x - self.VELOCITY


	def draw(self, play_window):
		play_window.blit(self.pipe_top_img, (self.x, self.top_pipe_height))
		play_window.blit(self.pipe_bottom_img, (self.x, self.bottom_pipe_height))


	def collide(self, bird):
		bird_mask = bird.get_mask()
		top_pipe_mask = pygame.mask.from_surface(self.pipe_top_img)
		bottom_pipe_mask = pygame.mask.from_surface(self.pipe_bottom_img)
		top_pipe_offset = (self.x - bird.x, self.top_pipe_height - round(bird.y))
		bottom_pipe_offset = (self.x - bird.x, self.bottom_pipe_height - round(bird.y))
		top_collide = bird_mask.overlap(top_pipe_mask, top_pipe_offset)
		bottom_collide = bird_mask.overlap(bottom_pipe_mask, bottom_pipe_offset)
		if top_collide or bottom_collide:
			return True
		return False


class Base():
	VELOCITY = 5
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG


	def __init__(self):
		self.y = HEIGHT - 75
		self.x1 = 0
		self.x2 = self.WIDTH


	def draw(self, play_window):
		play_window.blit(self.IMG, (self.x1, self.y))
		play_window.blit(self.IMG, (self.x2, self.y))


	def move(self):
		self.x1 -= self.VELOCITY
		self.x2 -= self.VELOCITY
		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH
		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

class Bg():
	VELOCITY = 2
	WIDTH = BG_IMG.get_width()
	IMAGE = BG_IMG
	def __init__(self):
		self.y = 0
		self.x1 = 0
		self.x2 = self.WIDTH

	def draw(self, play_window):
		play_window.blit(self.IMAGE, (self.x1, self.y))
		play_window.blit(self.IMAGE, (self.x2, self.y))

	def move(self):
		self.x1 -= self.VELOCITY
		self.x2 -= self.VELOCITY
		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH
		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH


def draw_window(play_window, bird, pipes, base, background, score):
	background.draw(play_window)
	for pipe in pipes:
		pipe.draw(play_window)
	score_lable = STAT_FONT.render('score:' + str(score), 1, (225,225,225))
	play_window.blit(score_lable, (590 - score_lable.get_width(), 10))
	bird.draw(play_window)
	base.draw(play_window)
	pygame.display.update()

def gameover_screen(play_window, score, gameover):
	clock = pygame.time.Clock()
	final_score = STAT_FONT.render('Final Score: ' + str(score), 1, (225, 225, 225))
	quit_lable = STAT_FONT.render('to quit press "q"', 1, (225, 225, 225))
	restart_lable = STAT_FONT.render('to restart again press "r"', 5, (225, 225, 225))
	while gameover:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_q]:
			pygame.quit()
			quit()
		elif keys[pygame.K_r]:
			return False
		play_window.blit(BG_IMG, (0,0))
		play_window.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 - final_score.get_height() // 2))
		play_window.blit(quit_lable, (WIDTH // 5, HEIGHT - 100))
		play_window.blit(restart_lable, (WIDTH // 5, HEIGHT - 80 + quit_lable.get_height()))
		pygame.display.update()



def game_loop():
	bird = Bird(175, 300)
	pipes = [Pipe(600)]
	score = 0
	base = Base()
	background = Bg()
	play_window = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('flappy_fall')
	clock = pygame.time.Clock()
	gameover = False
	while not gameover:
		clock.tick(30)
		play_window.fill(0)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			bird.jump()
		add_pipe = False
		for pipe in pipes:
			if pipe.collide(bird):
				gameover = True
				gameover = gameover_screen(play_window, score, gameover)
				score = 0
				bird.y = 350
				pipes.remove(pipe)
				pipes = [Pipe(WIDTH)]
			elif pipe.x + pipe.pipe_top_img.get_width() < 0:
				pipes.remove(pipe)
			if not pipe.passed and pipe.x < bird.x:
				pipe.passed = True
				add_pipe = True
			pipe.move()
		if add_pipe:
			score += 1
			pipes.append(Pipe(600))
		if bird.y + bird.img.get_height() > base.y  or bird.y < 0:
			gameover = True
			gameover = gameover_screen(play_window, score, gameover)
			score = 0
			bird.y = 350
			del pipes
			pipes = [Pipe(WIDTH)]
		bird.move()
		base.move()
		background.move()
		draw_window(play_window, bird, pipes, base, background, score)
if __name__ == '__main__':
    game_loop()
