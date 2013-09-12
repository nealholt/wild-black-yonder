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
import hitBoxTester as hbt

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


#copied from stardog utils.py
#setup images
#if there is extended image support, load .gifs, otherwise load .bmps.
#.bmps do not support transparency, so there might be black clipping.
ext = ".bmp"
if pygame.image.get_extended():
	ext = ".gif"

#START: copied from stardog utils.py
def loadImage(filename, colorkey=colors.black):
	try:
		image = pygame.image.load(filename).convert()
		image.set_colorkey(colorkey)
	except pygame.error:
		image = pygame.image.load("images/default" + ext).convert()
		image.set_colorkey(colors.white)
	return image
#END: copied from stardog utils.py


enemySprites = pygame.sprite.Group()
enemy_ships = []


allSprites = pygame.sprite.Group()
#Note that the player is not amongst allSprites mostly for when the screen
#fixes on or follows the player

#TODO Create a motionless object for reference purposes while testing.
allSprites.add(explosion.FixedBody(0, 0))

playerSprites = pygame.sprite.Group()


def hitBoxTest(c):
	#shoot a bunch of hit box testers 
	#in towards the player
	h=hbt.HitBoxTester(top=c[1]+50, left=c[0]+50, destination=c)
	enemySprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1]+50, left=c[0]-50, destination=c)
	enemySprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1]+50, left=c[0], destination=c)
	enemySprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1]-50, left=c[0]+50, destination=c)
	enemySprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1]-50, left=c[0]-50, destination=c)
	enemySprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1]-50, left=c[0], destination=c)
	enemySprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1], left=c[0]+50, destination=c)
	enemySprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1], left=c[0]-50, destination=c)
	enemySprites.add(h)
	allSprites.add(h)



class Game:
	""" """
	def __init__(self, camera=FIX_ON_PLAYER):
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
		#Use this to keep track of which keys are up and which 
		#are down at any given point in time.
		self.keys = []
		for _i in range (322):
			self.keys.append(False)
		#mouse is [pos, button1, button2, button3,..., button6].
		#new Apple mice think they have 6 buttons.
		#Use this to keep track of which mouse buttons are up and which 
		#are down at any given point in time.
		#Also the tuple, self.mouse[0], is the current location of the mouse.
		self.mouse = [(0, 0), 0, 0, 0, 0, 0, 0]
		#pygame setup:
		self.clock = pygame.time.Clock()


	def run(self):
		"""Runs the game."""
		self.running = True

		#The in-round loop (while player is alive):
		while self.running:
			#event polling:
			#See what buttons may or may not have been pushed.
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = 0
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.mouse[event.button] = 1
					self.mouse[0] = event.pos
				elif event.type == pygame.MOUSEBUTTONUP:
					self.mouse[event.button] = 0
				#elif event.type == pygame.MOUSEMOTION:
				#	self.mouse[0] = event.pos
				elif event.type == pygame.KEYDOWN:
					self.keys[event.key % 322] = 1
					print "TODO TESTING: key press "+str(event.key)

					#Respond to key taps.
					#Keys that we want to respond to holding them down
					#will be dealt with below.
					if event.key == 273: #Pressed up arrow
						#increase speed by one quarter of max up to max.
						self.player.targetSpeed = min(self.player.maxSpeed,\
									self.player.targetSpeed +\
									self.player.maxSpeed/4)
					elif event.key == 274: #Pressed down arrow
						#decrease speed by one quarter of max down to zero.
						self.player.targetSpeed = max(0,\
							self.player.targetSpeed -\
							self.player.maxSpeed/4)
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
					elif event.key == 116: #t key
						#shoot a bunch of hit box testers 
						#in towards the player
						print 'Width: '+str(self.player.image.get_width())+\
						' vs '+str(self.player.rect.width)
						print 'Height: '+str(self.player.image.get_height())+\
						' vs '+str(self.player.rect.height)
						hitBoxTest(self.player.getCenter())
					elif event.key == 47: 
						#forward slash (question mark without shift) key 
						#Useful for querying one time info.
						print 'Print player destination: '+\
						str(self.player.destx)+','+\
						str(self.player.desty)

				elif event.type == pygame.KEYUP:
					#Keep track of which keys are no longer being pushed.
					self.keys[event.key % 322] = 0

			##This will make the player move towards the mouse 
			##without any clicking involved.
			##Set player destination to current mouse coordinates.
			if self.mouse[1]:
				x,y = pygame.mouse.get_pos()
				x += self.offsetx
				y += self.offsety
				self.player.setDestination((x,y))

			#Respond to key holds.
			#Keys that we want to respond to tapping them
			#will be dealt with above.
			if self.keys[276]: #Pressed left arrow
				self.player.turnCounterClockwise()
			elif self.keys[275]: #Pressed right arrow
				self.player.turnClockwise()
			#This is not part of the above else if.
			#You can shoot and turn at the same time.
			if self.keys[32]: #Pressed space bar
				self.player.shoot()


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
			#False tells the function not to autokill collided sprites
			collisions = pygame.sprite.spritecollide(self.player, enemySprites, False)
			for c in collisions:
				#TODO TESTING the following is VERY bad. I think it indicates that custom collision handlers between objects is totally the way to go.
				if c.isHitBoxTester is None:
					c.kill()
					self.player.takeDamage()
				else:
					c.stopped = True

			self.checkEnemyCollisions()

			#Check for all collisions between the two sprite groups.
			#Cancel each other out. Meaning that bullets kill bullets
			#The true, true here will tell members of both groups to instantly kill each other.
			#TODO I don't really like this. It seems too blunt.
			collisions = pygame.sprite.groupcollide(enemySprites, playerSprites,\
								True, True)

	def checkEnemyCollisions(self):
		to_destroy = []
		for i in xrange(len(enemy_ships)):
			enemy = enemy_ships[i]
			#Check if enemy collided with player fire
			#False tells the function not to autokill collided sprites
			collisions = pygame.sprite.spritecollide(enemy, 
					playerSprites, False)
			if len(collisions) > 0:
				for c in collisions:
					c.kill()
					enemy.takeDamage()
				if enemy.isDead() and not i in to_destroy:
					to_destroy.append(i)
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
		enemy_ship = ship.Ship(top=50, left=50, image_name='images/destroyer')
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
		self.player.update()
		self.player.draw()
		self.player.drawHealthBarAt(self.player.getCenter())
		return 0,0

	def centerOnPlayer(self):
		self.player.update()
		self.player.drawAt((self.centerx, self.centery))
		self.player.drawHealthBarAt((self.centerx, self.centery))
		return self.player.getX() - self.centerx, self.player.getY() - self.centery

	def followPlayer(self):
		self.follower.update()
		offset = self.follower.getX() - self.centerx, \
			self.follower.getY() - self.centery
		self.follower.drawAt((self.centerx, self.centery)) #TODO temporarily draw for testing purposes.
		self.player.update(offset)
		self.player.draw(offset)

		
		pos = self.player.rect.centerx - offset[0], self.player.rect.centery - offset[1]
		self.player.drawHealthBarAt(pos) #self.player.getX() - offset[0], self.player.getY() - offset[1])
		return offset
