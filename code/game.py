#game.py

import pygame
import random as rd
import sys
sys.path.append('code')

import player
import enemy
import explosion

FPS = 30
black = (0,0,0)

class Game:
	""" """
	def __init__(self, screen):
		self.pause = False
		self.debug = False
		self.fps = FPS
		self.screen = screen
		self.top_left = 0, 0
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.mouseControl = True
		self.timer = 0
		self.spritegroup = pygame.sprite.Group()

		self.player = player.Player(self)

		self.spritegroup.add(enemy.Enemy(self,300,300))
		self.spritegroup.add(self.player)
		
		#key polling:
		self.keys = []
		for _i in range (322):
			self.keys.append(False)
		#mouse is [pos, button1, button2, button3,..., button6].
		#new Apple mice think they have 6 buttons.
		self.mouse = [(0, 0), 0, 0, 0, 0, 0, 0]
		#pygame setup:
		self.clock = pygame.time.Clock()


	def run(self):
		"""Runs the game."""
		self.running = True

		#The in-round loop (while player is alive):
		while self.running:
			#event polling:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = 0
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.mouse[event.button] = 1
					self.mouse[0] = event.pos

					x,y = event.pos
					self.player.setDestination(x,y)

					#print x
					#print y

				elif event.type == pygame.MOUSEBUTTONUP:
					self.mouse[event.button] = 0
					self.mouse[0] = event.pos
				elif event.type == pygame.MOUSEMOTION:
					self.mouse[0] = event.pos
				elif event.type == pygame.KEYDOWN:
					self.keys[event.key % 322] = 1

					#TODO TESTING. Is there a better way to do this with bindings?
					#see stardog for ideas
					if event.key == 276: #Pressed left
						pass
					elif event.key == 275: #Pressed right
						pass
					elif event.key == 32: #Pressed space bar
						self.player.shoot()
					elif event.key == 27: #escape key or red button
						self.running = 0

					print "TODO TESTING: key press "+str(event.key)

				elif event.type == pygame.KEYUP:
					self.keys[event.key % 322] = 0
				if self.pause:
					self.menu.handleEvent(event)

			#draw the layers:
			self.screen.fill(black)

			#Check for all collisions. Naively at first.
			sg = self.spritegroup.sprites()
			limit = len(sg)
			#Do it this way to prevent self collision and avoid redundant collision checks.
			for i in range(limit):
				for j in range(i + 1, limit):
					#http://pygame.org/docs/ref/sprite.html#pygame.sprite.spritecollide
					#http://www.pygame.org/docs/tut/SpriteIntro.html
					if pygame.sprite.collide_rect(sg[i], sg[j]) and not sg[i].noClipWith(sg[j]) and not sg[j].noClipWith(sg[i]):
						#print 'COLLISION'
						self.spritegroup.add(explosion.Explosion(self, sg[i].rect.centery,sg[i].rect.centerx))
						sg[i].kill()
						sg[j].kill()
						#add in a new enemy
						self.spritegroup.add(enemy.Enemy(self, rd.randint(10, self.height-20), rd.randint(10, self.width-20)))

			#unpaused:
			#if not self.pause:
			#	#update action:
			#	for trigger in self.spritegroup:
			#		trigger.update()
			#	self.top_left = self.player.x - self.width / 2, \
			#			self.player.y - self.height / 2
			self.spritegroup.update()

			#frame maintainance:
			pygame.display.flip()
			self.clock.tick(FPS)#aim for FPS but adjust vars for self.fps.
			self.fps = max(1, int(self.clock.get_fps()))
			self.timer += 1. / self.fps
		#end round loop (until gameover)
	#end game loop
