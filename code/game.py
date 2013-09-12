#game.py
import pygame
import random as rd
import sys
sys.path.append('code')
import behaviors
import player
import scenarios
import colors
import ship
import testFunctions as test
from displayUtilities import writeTextToScreen, displayShipLoc
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

BGCOLOR = colors.black

#instantiate sprite groups
tangibles = pygame.sprite.Group()
intangibles = pygame.sprite.Group()
#This last group will contain any sprites that will tickle whiskers
whiskerables = pygame.sprite.Group()

#set up the display:
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#Player must be created before scenario is called.
player = player.Player('images/ship')


class Game:
	""" """
	def __init__(self):
		self.fps = FPS
		self.top_left = 0, 0
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.centerx = self.width / 2
		self.centery = self.height / 2

		self.offsetx = 0
		self.offsety = 0

		self.timer = 0 #TODO this isn't being used, but could be.

		self.follower = None
		self.camera = FIX_ON_PLAYER

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
			#frame maintainance:
			pygame.display.flip()
			self.clock.tick(FPS) #aim for FPS but adjust vars for self.fps.
			self.fps = max(1, int(self.clock.get_fps()))
			self.timer += 1. / self.fps

			#Skip the rest of this loop until the game is unpaused.
			if self.pause:
				#Write paused in the middle of the screen
				writeTextToScreen(string='PAUSED', font_size=128,\
					pos=(WIDTH/3, HEIGHT/2))
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
						break
					#Pass all other events to the panel
					else:
						self.panel.handleEvent(event)
				#Skip all the rest while displaying the menu.
				#This effectively pauses the game.
				continue

			#event polling:
			#See what buttons may or may not have been pushed.
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
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
						self.running = False
					elif event.key == 101: #e key
						#enemy created for testing.
						scenarios.makeNewEnemy(x=-500, y=0)
					elif event.key == 109: #m key
						self.panel = menus.getTestingPanel()
						continue
					elif event.key == 112: #p key
						player.parkingBrake()
					elif event.key == 113: #q key
						#Obliterate destination. Change to free flight.
						player.killDestination()
					elif event.key == 115: #s key
						self.pause = not self.pause; continue
					elif event.key == 116: #t key
						#shoot a bunch of hit box testers 
						#in towards the player
						print 'Width: '+str(player.image.get_width())+\
						' vs '+str(player.rect.width)
						print 'Height: '+str(player.image.get_height())+\
						' vs '+str(player.rect.height)
						test.hitBoxTest(player.rect.center)
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
				self.follower.setDestination(player.rect.center)

			#draw black over the screen
			#TODO as a game effect, it is super neato to temporarily NOT do this.
			screen.fill(BGCOLOR)

			#Check all collisions
			behaviors.collisionHandling()

			#update all sprites:

			#First tell the ships what is closest to them
			#so that they can avoid collisions
			behaviors.setClosestSprites()
			#Get the offset based on the camera.
			self.offsetx,self.offsety = self.getOffset[self.camera]()
			#Finally update all the sprites
			intangibles.update((self.offsetx,self.offsety))
			tangibles.update((self.offsetx,self.offsety))

			#Display player location for debugging.
			displayShipLoc(player)
		#end round loop (until gameover)
	#end game loop


	def setCamera(self, camera):
		self.camera = camera
		if self.camera == FOLLOW_PLAYER:
			self.follower = follower.Follower(0,0)


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


#Create a game object. Currently only used by scenarios.py. I wonder if this indicates that there is a better way? TODO
game_obj = Game()

