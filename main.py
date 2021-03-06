#!/usr/bin/env python

"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation, 
follow along in the tutorial.
"""

#Import Modules
import os
import sys
# Added for linux server
# Adds server folders to PYTHONPATH 
# ========================================
basedir = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.append(basedir)
# end of linux part
# ========================================

import pygame
import rabbit
import utils
import pymunk
import math
import random
from pygame.locals import *
from pymunk import Vec2d


if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600

class Game:

	def init_game(self):
		#Initialize Everything
		pygame.init()
		self.screen = pygame.display.set_mode((800,600))
		pygame.display.set_caption('Rainy Bunny by Mick v0.1')
		pygame.mouse.set_visible(0)

		#Create The Backgound
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))

		#Put Text On The Background, Centered
		if pygame.font:
			font = pygame.font.Font(None, 36)
			text = font.render("Rainy Bunny", 1, (10, 10, 10))
			textpos = text.get_rect(centerx=self.background.get_width()/2)
			self.background.blit(text, textpos)

		#Display The Background
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()

		#Prepare Game Objects
		self.clock = pygame.time.Clock()
		#whiff_sound = utils.load_sound('whiff.wav')
		#punch_sound = utils.load_sound('punch.wav')
		self.rabbit_sprite = rabbit.Rabbit()
		#	bird = Bird()
		self.allsprites = pygame.sprite.RenderPlain((self.rabbit_sprite))

		# PHYSICS STUFF
		#pymunk.init_pymunk()
		self.space = pymunk.Space()
		self.space.gravity = (0.0, -900.0)

		line_point1 = Vec2d(30 , flipy(350))        
		line_point2 = Vec2d(600, flipy(350))
		body = pymunk.Body(pymunk.inf, pymunk.inf)
		line= pymunk.Segment(body, line_point1, line_point2, 0.0)
		line.friction = 0.99
		self.space.add_static(line)

		body = line.body
		pv1 = body.position + line.a.rotated(body.angle)
		pv2 = body.position + line.b.rotated(body.angle)
		self.p1 = pv1.x, flipy(pv1.y)
		self.p2 = pv2.x, flipy(pv2.y)
		pygame.draw.lines(self.screen, 0, False, [self.p1,self.p2])

	def do_main_loop(self):
		#Main Loop
		balls = []
		ticks_to_next_ball = 10
		running = True
		while running:
			self.clock.tick(60)

			#Handle Input Events
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					running = False
				# key_to_dir(event.key) != 0 for valid keys
				elif event.type == KEYDOWN and utils.key_to_dir(event.key) != 0:
					self.rabbit_sprite.start_walk(utils.key_to_dir(event.key));
				elif event.type == KEYUP and utils.key_to_dir(event.key) != 0:
					self.rabbit_sprite.stop_walk(utils.key_to_dir(event.key));
				elif event.type == KEYDOWN and event.key == K_SPACE:
					self.rabbit_sprite.start_jump();
			self.allsprites.update()

			#Draw Everything
			self.screen.blit(self.background, (0, 0))
			self.allsprites.draw(self.screen)

###        
			ticks_to_next_ball -= 1
			if ticks_to_next_ball <= 0:
				ticks_to_next_ball = 5
				ball_shape = self.add_ball(self.space)
				balls.append(ball_shape)

			for ball in balls:
				self.draw_ball(self.screen, ball)

			#pygame.draw.lines(self.screen, Color(0,255,0), False, [self.p1,self.p2])


			# Physics step
			self.space.step(1/50.0)

			pygame.display.flip()


	def add_ball(self, space):
		mass = 1
		radius = 2
		inertia = pymunk.moment_for_circle(mass, 0, radius) 
		body = pymunk.Body(mass, inertia)
		x = self.rabbit_sprite.rect.center[0]; #x is bunny center
		x = random.randint(x-25,x+25) #randomize x
		body.position = x, 550 
		shape = pymunk.Circle(body, radius)
		self.space.add(body, shape)
		return shape

	def draw_ball(self, screen, ball):
		p = int(ball.body.position.x), 600-int(ball.body.position.y)
		pygame.draw.circle(screen, Color(0,0,255), p, int(ball.radius), 2)

	def main(self):
		"""this function is called when the program starts.
		   it initializes everything it needs, then runs in
		   a loop until the function returns."""

		self.init_game()

		self.do_main_loop()

	#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': 
	game = Game()
	game.main()
