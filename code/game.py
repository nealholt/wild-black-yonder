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

#Used by physicalObject to define what each physicalObject is.
BULLET = 0
OTHER = 1
SHIP = 2

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

#step 21: Goal: (Create separate sprite groups: tangible_sprites and intangible_sprite. Remove allSprites. Only check collisions on tangible sprites): delete this next line. Replace EVERY instance of allSprites with tangible_sprites.
allSprites = pygame.sprite.Group()

#step 22: this should be done to intangible_sprites
#TODO Create a motionless object for reference purposes while testing.
allSprites.add(explosion.FixedBody(0, 0))

player = player.Player('images/ship')
allSprites.add(player)


def hitBoxTest(c):
	#shoot a bunch of hit box testers 
	#in towards the player
	h=hbt.HitBoxTester(top=c[1]+50, left=c[0]+50, destination=c)
	allSprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1]+50, left=c[0]-50, destination=c)
	allSprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1]+50, left=c[0], destination=c)
	allSprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1]-50, left=c[0]+50, destination=c)
	allSprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1]-50, left=c[0]-50, destination=c)
	allSprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1]-50, left=c[0], destination=c)
	allSprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1], left=c[0]+50, destination=c)
	allSprites.add(h)
	allSprites.add(h)
	h=hbt.HitBoxTester(top=c[1], left=c[0]-50, destination=c)
	allSprites.add(h)
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
						player.targetSpeed = min(player.maxSpeed,\
									player.targetSpeed +\
									player.maxSpeed/4)
					elif event.key == 274: #Pressed down arrow
						#decrease speed by one quarter of max down to zero.
						player.targetSpeed = max(0,\
							player.targetSpeed -\
							player.maxSpeed/4)
					elif event.key == 27: #escape key or red button
						self.running = 0
					elif event.key == 101: #e key
						#enemy created for testing.
						self.makeNewEnemy()
					elif event.key == 112: #p key
						player.parkingBrake()
					elif event.key == 113: #q key
						#Obliterate destination. Change to free flight.
						player.killDestination()
					elif event.key == 116: #t key
						#shoot a bunch of hit box testers 
						#in towards the player
						print 'Width: '+str(player.image.get_width())+\
						' vs '+str(player.rect.width)
						print 'Height: '+str(player.image.get_height())+\
						' vs '+str(player.rect.height)
						hitBoxTest(player.getCenter())
					elif event.key == 47: 
						#forward slash (question mark without shift) key 
						#Useful for querying one time info.
						print 'Print player destination: '+\
						str(player.destx)+','+\
						str(player.desty)

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
				player.setDestination((x,y))

			#Respond to key holds.
			#Keys that we want to respond to tapping them
			#will be dealt with above.
			if self.keys[276]: #Pressed left arrow
				player.turnCounterClockwise()
			elif self.keys[275]: #Pressed right arrow
				player.turnClockwise()
			#This is not part of the above else if.
			#You can shoot and turn at the same time.
			if self.keys[32]: #Pressed space bar
				#Force shot tells this to shoot even if a target 
				#is not obviously in view. NPC's will not take such wild shots.
				player.shoot(force_shot=True)


			#remind follower of player's location
			if self.camera == FOLLOW_PLAYER:
				self.follower.setDestination(player.getCenter())

			#draw black over the screen
			#TODO as a game effect, it is super neato to temporarily NOT do this.
			screen.fill(colors.black)

			#Check all collisions
			self.collisionHandling()

			#update all sprites
			self.offsetx,self.offsety = self.getOffset[self.camera]()
			allSprites.update((self.offsetx,self.offsety))
			#step 25: also call update on intangible_sprites

			#step 28 (goal:update all the sprites, but only draw the ones that are on the screen.): take draw out of every physical object's update function including: bullet, stuff in explosion, hitBoxTester, ship.
			#step 29: create a new sprite group called on_screen
			#step 30: write a little code in the part of input that accepts the question mark which checks to see if the player is on the screen. You may want to simply create a rectangle that is the screen and see if the player collides with it. Print whether or not the player collides with it and test this with the fixed camera view.
			#step 31: Then do the same thing with the enemy with a different camera view, checking to see that it has the correct behavior.
			#step 32: add a bit of code in the run method that gets all tangibles and intangibles that collide with the screen rect (I think group collide might just return these nicely for you) and call draw on all the stuff in those functions.


			#Display player location for debugging.
			self.displayPlayerLoc()


			#frame maintainance:
			pygame.display.flip()
			self.clock.tick(FPS) #aim for FPS but adjust vars for self.fps.
			self.fps = max(1, int(self.clock.get_fps()))
			self.timer += 1. / self.fps
		#end round loop (until gameover)
	#end game loop


	def collisionHandling(self):
		'''The following function comes from pseudo code from
		 axisAlignedRectangleCollision.txt that has been modified.'''
		#Get a list of all the sprites
		sprite_list = allSprites.sprites()
		#sort the list in descending order based on each 
		#sprite's y coordinate (aka top) plus height.
		#Remember that larger y coordinates indicate further down
		#on the screen.
		#Reverse tells sorted to be descending.
		#rect.topleft[1] gets the y coordinate, top.
		sprite_list = sorted(sprite_list, \
			key=lambda c: c.rect.topleft[1]+c.rect.height,\
			reverse=True)
		#iterate over the sprite list
		for i in xrange(len(sprite_list)):
			A = sprite_list[i]
			for j in xrange(i+1, len(sprite_list)):
				B = sprite_list[j]
				#if A's least y coord (A's top) is > B's
				#largest y coord (B's bottom)
				#then they don't overlap and none of the following
				#sprites overlap A either becuase the list is sorted
				#by bottom y coordinates.
				#We therefore skip the rest of the sprites in the list.
				if A.rect.topleft[1] > B.rect.topleft[1]+B.rect.height:
					break
				else:
					#Otherwise, we need to see if they overlap
					#in the x direction.
					#if A's greatest x coord is < B's least x coord
					#or B's greatest x coord is < A's least x coord
					#then they don't overlap, but one of the following 
					#sprites might still overlap so we move to the
					#next sprite in the list.
					if A.rect.topleft[0]+A.rect.width < B.rect.topleft[0]\
					or B.rect.topleft[0]+B.rect.width < A.rect.topleft[0]:
						pass
					else:
						#they overlap. They should handle 
						#collisions with each other.
						A_died = A.handleCollisionWith(B)
						B.handleCollisionWith(A)
						#If A has died, then don't worry about A
						#colliding with anything else.
						if A_died:
							break


	#step 26: delete the following functions from game.py: collisionChecks and checkEnemyCollisions
	#step 27: test
	def collisionChecks(self):
		if player.isDead():
			allSprites.add(explosion.Explosion(player.getY(),player.getX()))
			#kill removes the calling sprite from all sprite groups
			player.kill()

		else:
			#Check if player collided with enemy fire
			#False tells the function not to autokill collided sprites
			collisions = pygame.sprite.spritecollide(player, allSprites, False)
			for c in collisions:
				#TODO TESTING the following is VERY bad. I think it indicates that custom collision handlers between objects is totally the way to go.
				if c.isHitBoxTester is None:
					#kill removes the calling sprite 
					#from all sprite groups
					c.kill()
					player.takeDamage()
				else:
					c.stopped = True

			self.checkEnemyCollisions()


	def checkEnemyCollisions(self):
		to_destroy = []
		for i in xrange(len(enemy_ships)):
			enemy = enemy_ships[i]
			if len(collisions) > 0:
				for c in collisions:
					#kill removes the calling sprite 
					#from all sprite groups
					c.kill()
					enemy.takeDamage()
				if enemy.isDead() and not i in to_destroy:
					to_destroy.append(i)
			#check if player collided with the enemy
			elif pygame.sprite.collide_rect(player, enemy):
				if not i in to_destroy: to_destroy.append(i)
				player.takeDamage()
		#Blow up destroyed enemies. They only have one health each.
		for td in to_destroy:
			self.blowUpEnemy(td)

	def makeNewEnemy(self):
		enemy_ship = ship.Ship(top=50, left=50, image_name='images/destroyer')
		allSprites.add(enemy_ship)

	def displayPlayerLoc(self):
#		if self.timer > self.nextUpdate:
		self.nextUpdate += self.textUpdateInterval
		font = pygame.font.Font(None, 36)
		string = "Player X,Y: "+str(player.getX())+','+str(player.getY())+'. Speed: '+str(player.speed)+'. MaxSpeed: '+str(player.maxSpeed)
		text = font.render(string, 1, (255, 255, 255)) #white
		textpos = text.get_rect(center=(400,10)) #center text at 400, 10
		screen.blit(text, textpos)


	#Choices for the display follow in 3 functions:

	def fixedScreen(self):
		player.playerUpdate()
		player.draw()
		player.drawHealthBarAt(player.getCenter())
		return 0,0

	def centerOnPlayer(self):
		player.playerUpdate()
		player.drawAt((self.centerx, self.centery))
		player.drawHealthBarAt((self.centerx, self.centery))
		return player.getX() - self.centerx, player.getY() - self.centery

	def followPlayer(self):
		self.follower.update()
		offset = self.follower.getX() - self.centerx, \
			self.follower.getY() - self.centery
		self.follower.drawAt((self.centerx, self.centery)) #TODO temporarily draw for testing purposes.
		player.playerUpdate(offset)
		player.draw(offset)

		
		pos = player.rect.centerx - offset[0], player.rect.centery - offset[1]
		player.drawHealthBarAt(pos) #player.getX() - offset[0], player.getY() - offset[1])
		return offset
