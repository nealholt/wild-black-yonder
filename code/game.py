#game.py

import pygame

import sys
sys.path.append('code')

import player

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
		self.systems = []
		self.triggers = []

		self.player = player.Player(self)
		
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
		#print 'run reached in game. exiting now.'; exit(); #TODO TESTING

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
				elif event.type == pygame.MOUSEBUTTONUP:
					self.mouse[event.button] = 0
					self.mouse[0] = event.pos
				elif event.type == pygame.MOUSEMOTION:
					self.mouse[0] = event.pos
				elif event.type == pygame.KEYDOWN:
					self.keys[event.key % 322] = 1

					#TODO TESTING. Is there a better way to do this with bindings?
					if event.key == 276: #Pressed left
						self.player.turnLeft()
					if event.key == 275: #Pressed right
						self.player.turnRight()
					elif event.key == 27: #escape key or red button
						self.running = 0

					print "TODO TESTING: key press "+str(event.key)

				elif event.type == pygame.KEYUP:
					self.keys[event.key % 322] = 0
				if self.pause:
					self.menu.handleEvent(event)
						
			#unpaused:
			#if not self.pause:
			#	#update action:
			#	for trigger in self.triggers:
			#		trigger.update()
			#	self.top_left = self.player.x - self.width / 2, \
			#			self.player.y - self.height / 2

			#draw the layers:
			self.screen.fill(black)
			self.player.draw()
				
			#frame maintainance:
			pygame.display.flip()
			self.clock.tick(FPS)#aim for FPS but adjust vars for self.fps.
			self.fps = max(1, int(self.clock.get_fps()))
			self.timer += 1. / self.fps
		#end round loop (until gameover)
	#end game loop
