# XBone-3
import neat
import pygame
import os
import random

GEN = 0
WIDTH = 600
HEIGHT = 900
WHITE = (225, 225, 225)
RED = (225, 0, 0)
DRAW_LINES = True
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load('imgs\\bird1.png')),
             pygame.transform.scale2x(pygame.image.load('imgs\\bird2.png')),
             pygame.transform.scale2x(pygame.image.load('imgs\\bird3.png'))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load('imgs\\pipe.png'))
BASE_IMG = pygame.transform.scale2x(pygame.image.load('imgs\\base.png'))
BG_IMG = pygame.transform.scale(pygame.image.load('imgs\\bg.png'), (WIDTH, HEIGHT))
pygame.font.init()
STAT_FONT = pygame.font.SysFont('comicsans', 50)

class Bird():
	IMGS = BIRD_IMGS
	MAX_ROTATION = 40
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
		if (displacement < 0 or self.y < self.height + 50) and (self.tilt < self.MAX_ROTATION):
			self.tilt = self.MAX_ROTATION
		elif self.tilt > -90:
			self.tilt -= self.ROTATION_VEL
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
		elif self.img_count <= self.ANIMATION_TIME * 4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0
		elif self.tilt <= -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME * 2
		rotated_image = pygame.transform.rotate(self.img, self.tilt)
		rotated_image_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, round(self.y))).center)
		play_window.blit(rotated_image, rotated_image_rect.topleft)


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
	VELOCITY = 3
	WIDTH = BG_IMG.get_width()
	IMAGE = BG_IMG
	def __init__(self):
		self.y = 0
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VELOCITY
		self.x2 -= self.VELOCITY
		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH
		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, play_window):
		play_window.blit(self.IMAGE, (self.x1, self.y))
		play_window.blit(self.IMAGE, (self.x2, self.y))


def draw_window(play_window, birds, pipes, base, background, score, gen, pipe_index):
	background.draw(play_window)
	for pipe in pipes:
		pipe.draw(play_window)
	score_lable = STAT_FONT.render('score:' + str(score), 1, WHITE)
	play_window.blit(score_lable, (590 - score_lable.get_width(), 10))
	generation_lable = STAT_FONT.render('GEN:' + str(gen - 1), 1, WHITE)
	play_window.blit(generation_lable, (10, 10))
	alive_lable = STAT_FONT.render('Alive:' +str(len(birds)), 1, WHITE)
	play_window.blit(alive_lable, (10, 20 + generation_lable.get_height()))
	for bird in birds:
		if DRAW_LINES:
			try:
				pygame.draw.line(play_window, RED, (round(bird.x) + bird.img.get_width() // 2, round(bird.y) + bird.img.get_height() // 2), (round(pipes[pipe_index].x + pipes[pipe_index].pipe_top_img.get_width() // 2), round(pipes[pipe_index].top_pipe_height + pipes[pipe_index].pipe_top_img.get_height())), 3)
				pygame.draw.line(play_window, RED, (round(bird.x) + bird.img.get_width() // 2, round(bird.y) + bird.img.get_height() // 2), (round(pipes[pipe_index].x + pipes[pipe_index].pipe_top_img.get_width() // 2), round(pipes[pipe_index].bottom_pipe_height)), 3)
			except:
				pass
		bird.draw(play_window)
	base.draw(play_window)
	pygame.display.update()

gen = 0
def game_loop(genomes, config):
	nets = []
	genes = []
	birds = []
	for _, genome in genomes:
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		birds.append(Bird(175, 350))
		genome.fitness = 0
		genes.append(genome)
	pipes = [Pipe(600)]
	score = 0
	global gen
	gen += 1
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
		add_pipe = False
		pipe_index = 0
		if len(birds) > 0:
			if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].pipe_top_img.get_width():
				pipe_index = 1
		else:
			gameover = True
		for x, bird in enumerate(birds):
			genes[x].fitness += 0.1
			bird.move()
			output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom_pipe_height)))
			if output[0] > 0.5:
				bird.jump()
		for pipe in pipes:
			pipe.move()
			for x, bird in enumerate(birds):
				if pipe.collide(bird):
					genes[x].fitness -= 1
					nets.pop(x)
					genes.pop(x)
					birds.pop(x)
			if pipe.x + pipe.pipe_top_img.get_width() < 0:
				pipes.remove(pipe)
			if not pipe.passed and pipe.x < bird.x:
				pipe.passed = True
				add_pipe = True
		if add_pipe:
			score += 1
			for gene in genes:
				gene.fitness += 5
			pipes.append(Pipe(WIDTH))
		for x, bird in enumerate(birds):
			if bird.y + bird.img.get_height() > base.y or bird.y < 0:
				genes[x].fitness -= 1
				nets.pop(x)
				genes.pop(x)
				birds.pop(x)
		background.move()
		base.move()
		draw_window(play_window, birds, pipes, base, background, score, gen, pipe_index)
def run_fitness(config_path):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
	population = neat.Population(config)
	population.add_reporter(neat.StdOutReporter(True))
	statastics = neat.StatisticsReporter()
	population.add_reporter(statastics)
	winner = population.run(game_loop, 50)
if __name__ == '__main__':
    config_path = 'neat-config-feedforward.txt'
    run_fitness(config_path)
