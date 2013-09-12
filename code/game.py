#game.py

import pygame
import random as rd
import sys
sys.path.append('code')

import player
import enemy
import explosion
import follower

FPS = 30

#"Camera" options
FIXED_VIEW = 0
FIX_ON_PLAYER = 1
FOLLOW_PLAYER = 2

BLACK = (0,0,0)

class Game:
	""" """
	def __init__(self, screen):
		self.fps = FPS
		self.screen = screen
		self.top_left = 0, 0
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.centerx = self.width / 2
		self.centery = self.height / 2

		self.offsetx = 0
		self.offsety = 0

		self.timer = 0
		self.camera = FOLLOW_PLAYER #TODO Change camra view: FIXED_VIEW FIX_ON_PLAYER FOLLOW_PLAYER

		self.textUpdateInterval = 1 #in seconds
		self.nextUpdate = 0

		self.playerSprites = pygame.sprite.Group()
		self.player = player.Player(self)

		self.enemySprites = pygame.sprite.Group()
		self.enemy = enemy.Enemy(self,300,300)

		if self.camera == FOLLOW_PLAYER:
			self.follower = follower.Follower(self,0,0)

		self.getOffset = [self.fixedScreen, self.centerOnPlayer, self.followPlayer]

		self.allSprites = pygame.sprite.Group()
		#Note that the player is not amongst allSprites mostly for when the screen
		#fixes on or follows the player
		self.allSprites.add(self.enemy)

		#Create a motionless object for reference purposes while testing.
		self.allSprites.add(explosion.FixedBody(self, 0, 0))

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

			#Set player destination to current mouse coordinates.
			x,y = pygame.mouse.get_pos()
			x += self.offsetx
			y += self.offsety
			self.player.setDestination(x,y)

			#event polling:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = 0
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.mouse[event.button] = 1
					self.mouse[0] = event.pos
					#Set the destination of the player to be the mouse location clicked.
					x,y = event.pos
					self.player.setDestination(x,y)
				#elif event.type == pygame.MOUSEBUTTONUP:
				#	self.mouse[event.button] = 0
				#	self.mouse[0] = event.pos
				#elif event.type == pygame.MOUSEMOTION:
				#	self.mouse[0] = event.pos
				elif event.type == pygame.KEYDOWN:
					#self.keys[event.key % 322] = 1

					#if event.key == 276: #Pressed left
					#	pass
					#elif event.key == 275: #Pressed right
					#	pass
					#el
					if event.key == 32: #Pressed space bar
						self.player.shoot()
					elif event.key == 27: #escape key or red button
						self.running = 0

					print "TODO TESTING: key press "+str(event.key)

				#elif event.type == pygame.KEYUP:
				#	self.keys[event.key % 322] = 0

			#remind enemy of player's location
			self.enemy.setDestination(self.player.getX(),self.player.getY())
			#remind follower of player's location
			if self.camera == FOLLOW_PLAYER:
				self.follower.setDestination(self.player.getX(),self.player.getY())

			#draw black over the screen
			#TODO as a game effect, it is super neato to temporarily NOT do this.
			self.screen.fill(BLACK)

			#Check all collisions
			self.collisionChecks()

			#update all sprites
			self.offsetx,self.offsety = self.getOffset[self.camera]()
			self.allSprites.update((self.offsetx,self.offsety))

			#Display player location for debugging.
			self.displayPlayerLoc()


			#frame maintainance:
			pygame.display.flip()
			self.clock.tick(FPS) #aim for FPS but adjust vars for self.fps.
			self.fps = max(1, int(self.clock.get_fps()))
			self.timer += 1. / self.fps
		#end round loop (until gameover)
	#end game loop

	def collisionChecks(self):
		if self.player.isDead():
			self.allSprites.add(explosion.Explosion(self, self.player.getY(),self.player.getX()))
			self.player.kill()

		else:
			#Check if enemy collided with player fire
			replacedEnemy = False
			collisions = pygame.sprite.spritecollide(self.enemy, self.playerSprites, False)
			for c in collisions:
				c.kill()
				if not replacedEnemy:
					replacedEnemy = True
					self.replaceEnemy()

			#Check if player collided with enemy fire
			collisions = pygame.sprite.spritecollide(self.player, self.enemySprites, False)
			for c in collisions:
				c.kill()
				self.player.takeDamage()

			#check if player collided with the enemy
			if pygame.sprite.collide_rect(self.player, self.enemy):
				self.replaceEnemy()
				self.player.takeDamage()

			#Check for all collisions between the two sprite groups.
			#Cancel each other out. Meaning that bullets kill bullets
			collisions = pygame.sprite.groupcollide(self.enemySprites, self.playerSprites, True, True)


	def replaceEnemy(self):
		self.allSprites.add(explosion.Explosion(self, self.enemy.getY(),self.enemy.getX()))
		#kill old enemy
		self.enemy.kill()
		#add in a new enemy
		top = rd.randint(10, self.height-20)
		left = rd.randint(10, self.width-20)
		self.enemy = enemy.Enemy(self, top, left)
		self.allSprites.add(self.enemy)

	def displayPlayerLoc(self):
#		if self.timer > self.nextUpdate:
		self.nextUpdate += self.textUpdateInterval
		font = pygame.font.Font(None, 36)
		string = "Player X,Y: "+str(self.player.getX())+','+str(self.player.getY())
		text = font.render(string, 1, (255, 255, 255)) #white
		textpos = text.get_rect(center=(400,10)) #center text at 400, 10
		self.screen.blit(text, textpos)


	#Choices for the display follow in 3 functions:

	def fixedScreen(self):
		offset = 0,0
		self.player.update(offset)
		self.player.draw()
		self.player.drawHealthBarAt(self.player.getX(), self.player.getY())
		return offset

	def centerOnPlayer(self):
		self.player.update((0,0))
		self.player.drawAt((self.centerx, self.centery))
		self.player.drawHealthBarAt(self.centerx, self.centery)
		return self.player.getX() - self.centerx, self.player.getY() - self.centery

	def followPlayer(self):
		self.follower.update()
		offset = self.follower.getX() - self.centerx, \
			self.follower.getY() - self.centery
		self.player.update(offset)
		self.player.draw(offset)
		self.player.drawHealthBarAt(self.player.getX() - offset[0], self.player.getY() - offset[1])
		return offset
