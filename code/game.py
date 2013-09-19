import pygame

#It's necessary to do the next part before anyone imports displayUtilities now that we are pre-loading images.
pygame.init()
import globalvars
#set up the display:
globalvars.screen = pygame.display.set_mode((globalvars.WIDTH, globalvars.HEIGHT))

import random as rd
import sys
sys.path.append('code')
import player as playerObj
import colors
import testFunctions as test
import menus
from geometry import distance, angleFromPosition, translate, rotateAngle
from misc import writeTextToScreen
import datetime #Use for testing efficiency

#instantiate sprite groups
globalvars.tangibles = pygame.sprite.Group()
globalvars.intangibles = []
#This last group will contain any sprites that will tickle whiskers
globalvars.whiskerables = pygame.sprite.Group()

#Player must be created before scenario is called.
globalvars.player = playerObj.Player('ship')


def updateDust(offset):
	'''For each dust particle,
	If the dust is too far from the player then move it to a location
	offscreen, but in the direction that the player is moving.
	Otherwise, just draw the dust with the update function.'''
	limit = globalvars.WIDTH
	for i in xrange(len(globalvars.dust)):
		dist = distance(globalvars.dust[i].rect.center, globalvars.player.rect.center)
		if dist > limit:
			magnitude = rd.randint(globalvars.WIDTH/2, globalvars.WIDTH)
			rotation = rd.randint(-70, 70)
			globalvars.dust[i].rect.center = translate(globalvars.player.rect.center,\
				rotateAngle(globalvars.player.theta, rotation),\
				magnitude)
		elif dist < globalvars.WIDTH:
			globalvars.dust[i].update()
			globalvars.dust[i].draw(offset)


def run():
	"""Runs the game."""
	fps = globalvars.FPS
	offsetx = 0
	offsety = 0
	offset = offsetx, offsety

	#key polling:
	#Use this to keep track of which keys are up and which 
	#are down at any given point in time.
	keys = []
	for _i in range (322):
		keys.append(False)
	#mouse is [pos, button1, button2, button3,..., button6].
	#new Apple mice think they have 6 buttons.
	#Use this to keep track of which mouse buttons are up and which 
	#are down at any given point in time.
	#Also the tuple, mouse[0], is the current location of the mouse.
	mouse = [(0, 0), 0, 0, 0, 0, 0, 0]

	#pygame setup:
	clock = pygame.time.Clock()

	pause = False

	running = True

	#The in-round loop (while player is alive):
	while running:
		#Used for calculating actual frames per second in
		#order to determine when we are dropping frames
		#so that efficiency improvements can be made.
		start_time = datetime.datetime.now()
		#frame maintainance:
		pygame.display.flip()
		#aim for globalvars.FPS frames per second.
		clock.tick(globalvars.FPS) 
		fps = max(1, int(clock.get_fps()))

		#Skip the rest of this loop until the game is unpaused.
		if pause:
			#Write paused in the middle of the screen
			writeTextToScreen(string='PAUSED', font_size=128,\
				pos=(globalvars.WIDTH/3, globalvars.HEIGHT/2))
			#Check for another s key press to unpause the game.
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == 115: #s key
					pause = not pause
			#Skip the rest of this loop until the game is unpaused.
			continue

		#Display the panel
		if not globalvars.panel is None:
			globalvars.panel.draw()
			#Check for another m key press to remove the panel.
			for event in pygame.event.get():
				#Check for event m key being pressed to
				#remove the menu.
				if event.type == pygame.KEYDOWN and \
				event.key == 109: #m key
					globalvars.panel = None
					break
				#Panel event handeling can make the panel itself None so we have 
				#to check if the panel has become None for every event. If the
				#panel has become None we break and ignore further input events.
				elif globalvars.panel is None:
					break
				#Pass all other events to the panel
				else:
					globalvars.panel.handleEvent(event)
			#Skip all the rest while displaying the menu.
			#This effectively pauses the game.
			continue

		#event polling:
		#See what buttons may or may not have been pushed.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse[event.button] = 1
				mouse[0] = event.pos
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse[event.button] = 0
			#elif event.type == pygame.MOUSEMOTION:
			#	mouse[0] = event.pos
			elif event.type == pygame.KEYDOWN:
				keys[event.key % 322] = 1
				#print "TODO TESTING: key press "+str(event.key)

				#Respond to key taps.
				#Keys that we want to respond to holding them down
				#will be dealt with below.
				if event.key == 273: #Pressed up arrow
					#increase speed by a fraction of max up to max.
					globalvars.player.targetSpeed = min(\
						globalvars.player.maxSpeed,\
						globalvars.player.targetSpeed +\
						globalvars.player.maxSpeed*\
						globalvars.player.speedIncrements)
				elif event.key == 274: #Pressed down arrow
					#decrease speed by a fraction of 
					#max down to zero.
					globalvars.player.targetSpeed = max(0,\
						globalvars.player.targetSpeed -\
						globalvars.player.maxSpeed*\
						globalvars.player.speedIncrements)
				elif event.key == 27: #escape key or red button
					running = False
				elif event.key == 109: #m key
					#If player is dead, access the restart panel, not the testing panel.
					if globalvars.player.isDead():
						globalvars.panel = menus.getRestartPanel()
					else:
						globalvars.panel = menus.getTestingPanel()
					continue
				elif event.key == 110: #n key
					globalvars.panel = menus.getGalaxyPanel()
					continue
				elif event.key == 112: #p key
					globalvars.player.parkingBrake()
				elif event.key == 113: #q key
					#Obliterate destination.
					#Change to free flight.
					globalvars.player.killDestination()
				elif event.key == 115: #s key
					pause = not pause; continue
				elif event.key == 116: #t key
					#shoot a bunch of hit box testers 
					#in towards the player
					print 'Width: '+\
					    str(globalvars.player.image.get_width())+\
					' vs '+str(globalvars.player.rect.width)
					print 'Height: '+\
					    str(globalvars.player.image.get_height())+\
					' vs '+str(globalvars.player.rect.height)
					test.hitBoxTest(globalvars.player.rect.center)
				elif event.key == 121: #y key
					#Profile lots of methods, but not game.run()
					profileEverything(offset)
				elif event.key == 117: #u key
					#game.run()
					import cProfile
					print 'Profiling game.run(). Press escape to quit.'
					cProfile.runctx('run()', globals(),locals(), 'profiling/game.run.profile')
					print 'Done profiling run.'
					exit()
				elif event.key == 47:
					#forward slash (question mark
					#without shift) key.
					#Useful for querying one time info.
					print 'Print player destination: '+\
					str(globalvars.player.destx)+','+\
					str(globalvars.player.desty)

				#Separate if so other keys don't interfere
				#with this.
				if event.key == 32:
					#Pressed space bar
					#Force shot tells this to shoot
					#even if a target 
					#is not obviously in view. NPC's
					#will not take such wild shots.
					globalvars.player.shoot(force_shot=True)

			elif event.type == pygame.KEYUP:
				#Keep track of which keys are no longer
				#being pushed.
				keys[event.key % 322] = 0

		##This will make the player move towards the mouse 
		##without any clicking involved.
		##Set player destination to current mouse coordinates.
		if mouse[1]:
			x,y = pygame.mouse.get_pos()
			x += offsetx
			y += offsety
			globalvars.player.setDestination((x,y))

		#Respond to key holds.
		#Keys that we want to respond to tapping them
		#will be dealt with above.
		if keys[276]: #Pressed left arrow
			globalvars.player.turnCounterClockwise()
		elif keys[275]: #Pressed right arrow
			globalvars.player.turnClockwise()
		#This is not part of the above else if.
		#You can shoot and turn at the same time.
		if keys[32]: #Pressed space bar
			#Force shot tells this to shoot even if a target 
			#is not obviously in view. NPC's will not take such wild shots.
			globalvars.player.shoot(force_shot=True)


		#draw BGCOLOR over the screen
		#TODO as a game effect, it is super neato to temporarily NOT do this.
		if globalvars.BGIMAGE is None:
			globalvars.screen.fill(globalvars.BGCOLOR)
		else:
			globalvars.screen.blit(globalvars.BGIMAGE, (0,0))

		#Check all collisions
		collisionHandling()

		#If arena is non-zero, then make sure player and all 
		#whiskerables are within it
		if globalvars.arena > 0:
			#The inner concentric ring bounces the player back 
			#towards center (don't actually bounce, just change 
			#angle directly towards center. The outer 
			#concentric ring, defined by distance from center 
			#plus object radius will bounce asteroids in a 
			#semi random direction towards the center-ish area.

			#Make sure player is within arena.
			#If not, change player's heading to be towards 0,0
			if distance(globalvars.player.rect.center, (0.,0.)) > globalvars.arena:
				globalvars.player.theta = angleFromPosition(\
					globalvars.player.rect.center, (0.,0.))
				globalvars.player.updateImageAngle()
			#Check each whiskerable and if it is more than 
			#arena + diameter from center, then change its 
			#angle to point somewhere within the arena too.
			for w in globalvars.whiskerables:
				if distance(w.rect.center, (0.,0.)) > \
				globalvars.arena + w.collisionradius:
					#Whiskerables reflect randomly
					#off arena boundaries towards a
					#point somewhere within 3/4 the
					#center of the arena.
					limit = 3*globalvars.arena/4
					x = rd.randint(-limit, limit)
					y = rd.randint(-limit, limit)
					if not w.direction is None:
						#Asteroids distinguish between their orientation,
						#theta, and direction of movement, direction.
						#Thus we want direction changed, not theta.
						w.direction = angleFromPosition(\
							w.rect.center, (x,y))
					else:
						w.theta = angleFromPosition(w.rect.center, (x,y))

		#update all sprites:

		#First tell the ships what is closest to them
		#so that they can avoid collisions
		setClosestSprites()
		#Get the offset based on the player location.
		offsetx = globalvars.player.rect.centerx - globalvars.CENTERX
		offsety = globalvars.player.rect.centery - globalvars.CENTERY
		offset = offsetx, offsety
		#Finally update all the sprites
		for x in globalvars.intangibles:
			#Returning true from update indicates that the intangible died.
			if x.update(): globalvars.intangibles.remove(x)
		globalvars.tangibles.update()

		#Draw all the things that are on the screen
		#Draw intangibles
		drawThoseOnScreen(globalvars.intangibles, offset)
		#Update and draw the dust
		updateDust(offset)
		#Draw tangibles
		drawThoseOnScreen(globalvars.tangibles.sprites(), offset)
		#Draw player last so the background isn't drawn overtop of the player.
		globalvars.player.playerUpdate()
		if not globalvars.player.isDead():
			globalvars.player.drawAt((globalvars.CENTERX, globalvars.CENTERY))
		else:
			#Make player death kick the player back to a menu where player 
			#can choose to restart. Display a death screen then. Reset the 
			#scenario and everything else.
			#Countdown before kicking player back to menu
			globalvars.deathcountdown -= 1
			if globalvars.deathcountdown < 0:
				globalvars.panel = menus.getRestartPanel()

		globalvars.hud_helper.update(offset)

		#Calculate how long we took in the above loop to estimate the number of frames per second
		#Alert user if fraps drops below half the desired threshold.
		time_lapse = datetime.datetime.now() - start_time
		if float(time_lapse.microseconds)/1000000. > (2.0/globalvars.FPS):
			print 'Warning: frames dropping.'
			print 'Goal frames per second is '+str(globalvars.FPS)+'. Current is '+str(1./(float(time_lapse.microseconds)/1000000.))[:2] #Cut off decimal because I don't care.
	#end round loop (until gameover)
#end game loop



def drawThoseOnScreen(sprite_list, offset):
	'''Takes a list of pygame sprites and the top left coordinates of the screen 
	and draws only those sprites that are visible on screen.
	I tested (see "y key" above) with and without checking whether or not each
	sprite is on the screen before drawing it and I found checking to be more
	efficient in multiple scenarios. The gain is less than I expected and
	a major inefficiency in python seems to be function calls, making me wonder 
	how important it is to wrap this into the run method, but I'm going to avoid 
	that for now.'''
	#draw_count = 0 #TESTING
	left, top = offset
	for sp in sprite_list:
		'''If the sprite is on the screen, then draw it.
		rect.right < left #Then not on screen
		rect.bottom < top #Then not on screen
		rect.top > top + globalvars.HEIGHT #Then not on screen
		rect.left > left + globalvars.WIDTH #Then not on screen'''
		if not( sp.rect.right < left or \
		sp.rect.bottom < top or \
		sp.rect.top > top + globalvars.HEIGHT or \
		sp.rect.left > left + globalvars.WIDTH ):
			sp.draw(offset)
			#draw_count += 1 #TESTING
	#print str(draw_count)+' objects on screen.' #TESTING

def drawThoseOnScreen2(sprite_list, offset):
	'''Presumably slower version of the above method used for testing.'''
	left, top = offset
	for sp in sprite_list: sp.draw(offset)



#The following were yanked out of behaviors.py and behaviors.py was removed because behaviors.py and game.py were mutually importing which can lead to errors. In any case, behaviors was only imported by game.py.

def setClosestSprites():
	'''Pre:
	Post: For all ships in the whiskerables sprite list, the closest sprite 
	and the distance to that sprite is set. This is used for helping NPC 
	ships avoid collisions.'''
	#Get all the whiskerable sprites in an array
	sprite_list = globalvars.whiskerables.sprites()
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
		if A.is_a != globalvars.SHIP: #TODO this could be more efficient by keeping another group that is just ships. Of course there is a cost there. It might be worth profiling at some point to see if this is better or another group that is just non-player ships is better.
			continue
		#Reset closest sprite and the distance to that sprite. Sprites 
		#further than this distance will be ignored.
		closest_sprite = None
		least_dist = globalvars.MINSAFEDIST
		#search for too close sprites
		for j in xrange(len(sprite_list)):
			if j != i:
				B = sprite_list[j]
				dist = distance(A.rect.center, B.rect.center) - B.collisionradius - A.collisionradius
				if dist < least_dist:
					least_dist = dist
					closest_sprite = B
		#Set sprite A's closest sprite and the distance to that sprite.
		#if not closest_sprite is None: print closest_sprite.image_name+' at '+str(least_dist) #TODO TESTING
		A.setClosest(closest_sprite, least_dist)


def collisionHandling():
	'''The following function comes from pseudo code from
	 axisAlignedRectangleCollision.txt that has been modified.'''
	#Get a list of all the sprites
	sprite_list = globalvars.tangibles.sprites()
	#sort the list in descending order based on each 
	#sprite's y coordinate (aka top) plus height.
	#Remember that larger y coordinates indicate further down
	#on the screen.
	#Reverse tells sorted to be descending.
	#rect.topleft[1] gets the y coordinate, top.
	sprite_list = sorted(sprite_list, \
		key=lambda c: c.rect.bottom,\
		reverse=True)
	#TODO I'm a bit concerned that I just sorted by bottom when now some things can have custom hit boxes (mainly the capital ship).
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
			if A.rect.top > B.rect.bottom:
				break
			else:
				#Otherwise, we need to see if they overlap
				#in the x direction.
				#if A's greatest x coord is < B's least x coord
				#or B's greatest x coord is < A's least x coord
				#then they don't overlap, but one of the following 
				#sprites might still overlap so we move to the
				#next sprite in the list.
				if A.inCollision(B):
					#they overlap. They should handle 
					#collisions with each other.
					A_died = A.handleCollisionWith(B)
					B.handleCollisionWith(A)
					#If A has died, then don't worry about A
					#colliding with anything else.
					if A_died: break


def profileEverything(offset):
	import cProfile
	cProfile.runctx('for _ in range(10000): drawThoseOnScreen(globalvars.tangibles.sprites(), offset)', globals(),locals(), 'profiling/drawTangibles.profile')
	cProfile.runctx('for _ in range(10000): drawThoseOnScreen2(globalvars.tangibles.sprites(), offset)', globals(),locals(), 'profiling/drawTangibles2.profile')
	cProfile.runctx('for _ in range(10000): updateDust(offset)', globals(),locals(), 'profiling/updateDust.profile')
	cProfile.runctx('for _ in range(10000): collisionHandling()', globals(),locals(), 'profiling/collisionHandling.profile')
	cProfile.runctx('for _ in range(10000): setClosestSprites()', globals(),locals(), 'profiling/setClosestSprites.profile')
	cProfile.runctx('for _ in range(10000): drawThoseOnScreen(globalvars.intangibles, offset)', globals(),locals(), 'profiling/drawIntangibles.profile')
	cProfile.runctx('for _ in range(10000): globalvars.tangibles.update()', globals(),locals(), 'profiling/updateTangibles.profile')
	cProfile.runctx('for _ in range(10000): globalvars.hud_helper.update(offset)', globals(),locals(), 'profiling/updateHudHelper.profile')

	#Profile some of the scenario functions.
	menus.scenarios.profile()

