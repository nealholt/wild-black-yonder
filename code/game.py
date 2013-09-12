#game.py

import pygame
import random as rd
import sys
sys.path.append('code')

import player
import explosion
import follower
import colors
import ship

FPS = 30 #frames per second

#"Camera" options
FIXED_VIEW = 0
FIX_ON_PLAYER = 1
FOLLOW_PLAYER = 2

WIDTH = 900
HEIGHT = 700

#set up the display:
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(colors.black)

enemySprites = pygame.sprite.Group()
enemy_ships = []


allSprites = pygame.sprite.Group()
#Note that the player is not amongst allSprites mostly for when the screen
#fixes on or follows the player

#TODO Create a motionless object for reference purposes while testing.
allSprites.add(explosion.FixedBody(0, 0))

playerSprites = pygame.sprite.Group()


class Game:
	""" """
	def __init__(self, camera=FOLLOW_PLAYER):
		self.fps = FPS
		self.top_left = 0, 0
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.centerx = self.width / 2
		self.centery = self.height / 2

		self.offsetx = 0
		self.offsety = 0

		self.timer = 0
		self.camera = camera

		self.textUpdateInterval = 1 #in seconds
		self.nextUpdate = 0

		self.player = player.Player('images/ship')

		if self.camera == FOLLOW_PLAYER:
			self.follower = follower.Follower(0,0)

		self.getOffset = [self.fixedScreen, self.centerOnPlayer, self.followPlayer]

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

			##This will make the player move towards the mouse 
			##without any clicking involved.
			##Set player destination to current mouse coordinates.
			#x,y = pygame.mouse.get_pos()
			#x += self.offsetx
			#y += self.offsety
			#self.player.setDestination((x,y))

			#event polling:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = 0
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.mouse[event.button] = 1
					self.mouse[0] = event.pos
					#Set the destination of the player 
					#to be the mouse location
					x,y = event.pos
					x += self.offsetx
					y += self.offsety
					self.player.setDestination((x,y))
				#elif event.type == pygame.MOUSEBUTTONUP:
				#	self.mouse[event.button] = 0
				#	self.mouse[0] = event.pos
				#elif event.type == pygame.MOUSEMOTION:
				#	self.mouse[0] = event.pos
				elif event.type == pygame.KEYDOWN:
					#self.keys[event.key % 322] = 1

					if event.key == 273: #Pressed up arrow
						#increase speed by one quarter of max up to max.
						self.player.targetSpeed = min(self.player.maxSpeed, self.player.targetSpeed + self.player.maxSpeed/4)
					elif event.key == 274: #Pressed down arrow
						#decrease speed by one quarter of max down to zero.
						self.player.targetSpeed = max(0, self.player.targetSpeed - self.player.maxSpeed/4)
					elif event.key == 276: #Pressed left arrow
						self.player.turnCounterClockwise(delta=30)
					elif event.key == 275: #Pressed right arrow
						self.player.turnClockwise(delta=30)
					elif event.key == 32: #Pressed space bar
						self.player.shoot()
					elif event.key == 27: #escape key or red button
						self.running = 0
					elif event.key == 101: #e key
						#enemy created for testing.
						self.makeNewEnemy()
					elif event.key == 112: #p key
						self.player.parkingBrake()
					elif event.key == 113: #q key
						#Obliterate destination. Change to free flight.
						self.player.killDestination()
					elif event.key == 47: 
						#forward slash (question mark without shift) key 
						#Useful for querying one time info.
						print 'Print player destination: '+\
						str(self.player.destx)+','+\
						str(self.player.desty)

					print "TODO TESTING: key press "+str(event.key)

				#elif event.type == pygame.KEYUP:
				#	self.keys[event.key % 322] = 0

			#remind enemy of player's location
			for e in enemy_ships:
				e.setDestination(self.player.getCenter())
			#remind follower of player's location
			if self.camera == FOLLOW_PLAYER:
				self.follower.setDestination(self.player.getCenter())

			#draw black over the screen
			#TODO as a game effect, it is super neato to temporarily NOT do this.
			screen.fill(colors.black)

			#Check all collisions
			self.collisionChecks()

			#update all sprites
			self.offsetx,self.offsety = self.getOffset[self.camera]()
			allSprites.update((self.offsetx,self.offsety))

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
			allSprites.add(explosion.Explosion(self.player.getY(),self.player.getX()))
			self.player.kill()

		else:
			#Check if player collided with enemy fire
			collisions = pygame.sprite.spritecollide(self.player, enemySprites, False)
			for c in collisions:
				c.kill()
				self.player.takeDamage()

			self.checkEnemyCollisions()

			#Check for all collisions between the two sprite groups.
			#Cancel each other out. Meaning that bullets kill bullets
			collisions = pygame.sprite.groupcollide(enemySprites, playerSprites, True, True)

	def checkEnemyCollisions(self):
		to_destroy = []
		for i in xrange(len(enemy_ships)):
			enemy = enemy_ships[i]
			#Check if enemy collided with player fire
			collisions = pygame.sprite.spritecollide(enemy, playerSprites, False)
			if len(collisions) > 0:
				if not i in to_destroy: to_destroy.append(i)
				for c in collisions:
					c.kill()
			#check if player collided with the enemy
			elif pygame.sprite.collide_rect(self.player, enemy):
				if not i in to_destroy: to_destroy.append(i)
				self.player.takeDamage()
		#Blow up destroyed enemies. They only have one health each.
		for td in to_destroy:
			self.blowUpEnemy(td)

	def blowUpEnemy(self, index):
		ship = enemy_ships.pop(index)
		allSprites.add(explosion.Explosion(ship.getY(),ship.getX()))
		ship.kill()

	def makeNewEnemy(self):
		enemy_ship = ship.Ship()
		allSprites.add(enemy_ship)
		enemy_ships.append(enemy_ship)

	def displayPlayerLoc(self):
#		if self.timer > self.nextUpdate:
		self.nextUpdate += self.textUpdateInterval
		font = pygame.font.Font(None, 36)
		string = "Player X,Y: "+str(self.player.getX())+','+str(self.player.getY())+'. Speed: '+str(self.player.speed)+'. MaxSpeed: '+str(self.player.maxSpeed)
		text = font.render(string, 1, (255, 255, 255)) #white
		textpos = text.get_rect(center=(400,10)) #center text at 400, 10
		screen.blit(text, textpos)


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
		self.follower.drawAt((self.centerx, self.centery)) #TODO temporarily draw for testing purposes.
		self.player.update(offset)
		self.player.draw(offset)
		self.player.drawHealthBarAt(self.player.getX() - offset[0], self.player.getY() - offset[1])
		return offset
