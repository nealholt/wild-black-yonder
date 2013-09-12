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

import menus

from time import sleep

DEBUG = True

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
FIXEDBODY = 3
HEALTH = 4

#The least distance to check for a collision. Might need adjusted if we start using really big objects.
MINSAFEDIST = 1024

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
def loadImage(filename):
	''' '''
	try:
		image = pygame.image.load(filename).convert()
		#colorkey tells pygame what color to make transparent.
		#We assume that the upper left most pixel's color is the color to make transparent.
		colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey)
	except pygame.error:
		image = pygame.image.load("images/default" + ext).convert()
		image.set_colorkey(colors.white)
	return image
#END: copied from stardog utils.py

tangibles = pygame.sprite.Group()
intangibles = pygame.sprite.Group()
#This last group will contain any sprites that will tickle whiskers
whiskerables = pygame.sprite.Group()

#TODO Create a motionless object for reference purposes while testing.
temp = explosion.FixedBody(0, -100, image_name='images/TyDfN_tiny') #little crystal
tangibles.add(temp); whiskerables.add(temp)
print 'Radius of TyDfN_tiny is '+str(temp.radius)
temp = explosion.FixedBody(0, 0, image_name='images/asteroidBigRoundTidied') #largest asteroid
tangibles.add(temp); whiskerables.add(temp)
print 'Radius of asteroidBigRoundTidied is '+str(temp.radius)
temp = explosion.FixedBody(500, 500, image_name='images/asteroidWild2') #medium asteroid
tangibles.add(temp); whiskerables.add(temp)
print 'Radius of asteroidWild2 is '+str(temp.radius)
temp = explosion.FixedBody(500, 0, image_name='images/asteroidTempel') #small asteroid
tangibles.add(temp); whiskerables.add(temp)
print 'Radius of asteroidTempel is '+str(temp.radius)
temp = explosion.FixedBody(-500, -500, image_name='images/Sikhote_small') #goldish metal rock
tangibles.add(temp); whiskerables.add(temp)
print 'Radius of Sikhote_small is '+str(temp.radius)
temp = explosion.FixedBody(-500, 0, image_name='images/bournonite_30percent') #silvery metal rock
tangibles.add(temp); whiskerables.add(temp)
print 'Radius of bournonite_30percent is '+str(temp.radius)

temp = explosion.HealthKit(-100, 0) #health pack
tangibles.add(temp)


player = player.Player('images/ship')
tangibles.add(player)


def setClosestSprites():
	'''Pre:
	Post: For all ships in the whiskerables sprite list, the closest sprite 
	and the distance to that sprite is set. This is used for helping NPC 
	ships avoid collisions.'''
	#Get all the whiskerable sprites in an array
	sprite_list = whiskerables.sprites()
	#TODO I'd like to make use of sorting like I do for collision checking with this, but recently it was gumming up the works, so I'm simplifying it for now.
	#Sort them by their top point as is done when checking for collisions.
	#sprite_list = sorted(sprite_list, \
	#	key=lambda c: c.rect.topleft[1]+c.rect.height,\
	#	reverse=True)
	#For each sprite...
	for i in xrange(len(sprite_list)):
		#Get the next sprite to deal with.
		A = sprite_list[i]
		#only ships can avoid objects.
		if A.is_a != SHIP: #TODO this could be more efficient by keeping another group that is just ships. Of course there is a cost there. It might be worth profiling at some point to see if this is better or another group that is just non-player ships is better.
			continue
		#Reset closest sprite and the distance to that sprite. Sprites 
		#further than this distance will be ignored.
		closest_sprite = None
		least_dist = MINSAFEDIST
		#search for too close sprites
		for j in xrange(len(sprite_list)):
			if j != i:
				B = sprite_list[j]
				dist = A.distanceToDestination(dest=B.getCenter()) - B.radius - A.radius
				if dist < least_dist:
					least_dist = dist
					closest_sprite = B
		'''#TODO this is the old way it was done when the sprite list was sorted, but I was accidentally missing checks on certain sprites so I simplified it for the time being.
		#search forward for too close sprites
		for j in xrange(i+1, len(sprite_list)):
			B = sprite_list[j]
			dist = A.distanceToDestination(dest=B.getCenter()) - B.radius - A.radius
			if dist < least_dist:
				least_dist = dist
				closest_sprite = B
				#break #TODO TESTING
			#TODO TESTING
			#elif abs(A.getX() - B.getX()) > least_dist:
			#	break
		#search backward for too close sprites
		count_back = []
		if i > 0:
			count_back = range(0, i-1)
			count_back.reverse()
		for j in count_back:
			B = sprite_list[j]
			dist = A.distanceToDestination(dest=B.getCenter()) - B.radius - A.radius
			if dist < least_dist:
				least_dist = dist
				closest_sprite = B
				#break #TODO TESTING
			#TODO TESTING
			#elif abs(A.getX() - B.getX()) > least_dist:
			#	break'''
		#Set sprite A's closest sprite and the distance to that sprite.
		#if not closest_sprite is None: print closest_sprite.image_name+' at '+str(least_dist) #TODO TESTING
		A.setClosest(closest_sprite, least_dist)


def hitBoxTest(c):
	#shoot a bunch of hit box testers 
	#in towards the player
	h=hbt.HitBoxTester(top=c[1]+50, left=c[0]+50, destination=c)
	tangibles.add(h)
	tangibles.add(h)
	h=hbt.HitBoxTester(top=c[1]+50, left=c[0]-50, destination=c)
	tangibles.add(h)
	tangibles.add(h)
	h=hbt.HitBoxTester(top=c[1]+50, left=c[0], destination=c)
	tangibles.add(h)
	tangibles.add(h)
	h=hbt.HitBoxTester(top=c[1]-50, left=c[0]+50, destination=c)
	tangibles.add(h)
	tangibles.add(h)
	h=hbt.HitBoxTester(top=c[1]-50, left=c[0]-50, destination=c)
	tangibles.add(h)
	tangibles.add(h)
	h=hbt.HitBoxTester(top=c[1]-50, left=c[0], destination=c)
	tangibles.add(h)
	tangibles.add(h)
	h=hbt.HitBoxTester(top=c[1], left=c[0]+50, destination=c)
	tangibles.add(h)
	tangibles.add(h)
	h=hbt.HitBoxTester(top=c[1], left=c[0]-50, destination=c)
	tangibles.add(h)
	tangibles.add(h)



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

		self.pause = False

		self.panel = None


	def run(self):
		"""Runs the game."""
		self.running = True

		#The in-round loop (while player is alive):
		while self.running:

			#Skip the rest of this loop until the game is unpaused.
			if self.pause:
				#Check for another s key press to unpause the game.
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN and event.key == 115: #s key
						self.pause = not self.pause
				#Skip the rest of this loop until the game is unpaused.
				continue

			#Display the panel
			if not self.panel is None:
				self.panel.draw()
				#Check for another m key press to remove the panel.
				for event in pygame.event.get():
					#Check for event m key being pressed to remove the menu.
					if event.type == pygame.KEYDOWN and event.key == 109: #m key
						self.panel = None
					#Check for mousebutton event and pass it to the panel
					if event.type == pygame.MOUSEBUTTONDOWN:
						self.panel.handleEvent(event)
				pygame.display.flip()
				#Skip all the rest while displaying the menu.
				#This effectively pauses the game.
				continue

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
					elif event.key == 109: #m key
						self.panel = menus.Panel(left=20,\
							top=20, width=100, height=100)
					elif event.key == 112: #p key
						player.parkingBrake()
					elif event.key == 113: #q key
						#Obliterate destination. Change to free flight.
						player.killDestination()
					elif event.key == 115: #s key
						self.pauseGame(); continue
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

					#Separate if so other keys don't interfere with this.
					if event.key == 32:
						#Pressed space bar
						#Force shot tells this to shoot even if a target 
						#is not obviously in view. NPC's will not take 
						#such wild shots.
						player.shoot(force_shot=True)

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

			#update all sprites:

			#First tell the ships what is closest to them
			#so that they can avoid collisions
			setClosestSprites()
			#Get the offset based on the camera.
			self.offsetx,self.offsety = self.getOffset[self.camera]()
			#Finally update all the sprites
			intangibles.update((self.offsetx,self.offsety))
			tangibles.update((self.offsetx,self.offsety))

			#Display player location for debugging.
			self.displayPlayerLoc()


			#frame maintainance:
			pygame.display.flip()
			self.clock.tick(FPS) #aim for FPS but adjust vars for self.fps.
			self.fps = max(1, int(self.clock.get_fps()))
			self.timer += 1. / self.fps
		#end round loop (until gameover)
	#end game loop


	def pauseGame(self):
		self.pause = not self.pause
		#Write paused in the middle of the screen
		font = pygame.font.Font(None, 128)
		string = 'PAUSED'
		text = font.render(string, 1, colors.white)
		pos = (WIDTH/3, HEIGHT/2)
		textpos = text.get_rect(center=pos)
		screen.blit(text, textpos)
		pygame.display.flip()


	def collisionHandling(self):
		'''The following function comes from pseudo code from
		 axisAlignedRectangleCollision.txt that has been modified.'''
		#Get a list of all the sprites
		sprite_list = tangibles.sprites()
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
					#OLD WAY based on rectangles:
					#if A.rect.topleft[0]+A.rect.width < B.rect.topleft[0]\
					#or B.rect.topleft[0]+B.rect.width < A.rect.topleft[0]:
					#NEW WAY based on circles:
					#If the distance between our centers is larger than are 
					#summed radii, then we have no collided.
					if A.distanceToDestination(dest=B.getCenter()) > A.radius+B.radius:

					#TODO LEFT OFF HERE
					
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


	def makeNewEnemy(self):
		enemy_ship = ship.Ship(top=0, left=-500, image_name='images/destroyer')
		tangibles.add(enemy_ship)
		whiskerables.add(enemy_ship)


	def displayPlayerLoc(self):
#		if self.timer > self.nextUpdate:
		self.nextUpdate += self.textUpdateInterval
		font = pygame.font.Font(None, 36)
		string = "Player X,Y: "+str(player.getX())+','+str(player.getY())+'. Speed: '+str(player.speed)+'. MaxSpeed: '+str(player.maxSpeed)
		text = font.render(string, 1, colors.white)
		textpos = text.get_rect(center=(400,10)) #center text at 400, 10
		screen.blit(text, textpos)


	#Choices for the display follow in 3 functions:

	def fixedScreen(self):
		player.playerUpdate()
		player.draw()
		return 0,0

	def centerOnPlayer(self):
		player.playerUpdate()
		player.drawAt((self.centerx, self.centery))
		return player.getX() - self.centerx, player.getY() - self.centery

	def followPlayer(self):
		self.follower.update()
		offset = self.follower.getX() - self.centerx, \
			self.follower.getY() - self.centery
		self.follower.drawAt((self.centerx, self.centery)) #TODO temporarily draw for testing purposes.
		player.playerUpdate(offset)
		player.draw(offset)

		return offset
