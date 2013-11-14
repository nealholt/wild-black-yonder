import pygame.sprite
import pygame.display
import objInstances
import colors
import random as rd
from geometry import getCoordsNearLoc, translate, distance, angleFromPosition
import ship
import capitalShip
import displayUtilities
import globalvars
import math
import player
import hudHelpers


def wipeOldScenario():
	globalvars.tangibles.empty()
	globalvars.intangibles_bottom.empty()
	globalvars.intangibles_top.empty()
	globalvars.whiskerables.empty()
	globalvars.BGCOLOR = colors.black
	globalvars.BGIMAGE = None
	globalvars.score_keeper = None
	#Add the player back in.
	globalvars.tangibles.add(globalvars.player)
	globalvars.player.setHealthBar()
	#Immediately clear the panel
	globalvars.menu.main_panel = None
	#Reset the arena
	globalvars.arena = 0


def makeNewEnemy(x=0, y=0, weaponType='mk1'):
	enemy_ship = ship.Ship(centerx=x, centery=y, image_name='destroyer')
	enemy_ship.setWeapon(weaponType)
	globalvars.tangibles.add(enemy_ship)
	globalvars.whiskerables.add(enemy_ship)


def resetDust():
	#Kill all the old dust.
	for d in globalvars.intangibles_bottom:
		if d.is_a == globalvars.DUST:
			d.kill()
	for d in globalvars.intangibles_top:
		if d.is_a == globalvars.DUST:
			d.kill()
	#Make 50 dust particles scattered around the player.
	for _ in range(50):
		size = rd.randint(1,4)
		x,y = getCoordsNearLoc(globalvars.player.rect.center, 50, 
				globalvars.WIDTH, globalvars.WIDTH)
		temp = objInstances.Dust(x=x, y=y, width=size, height=size,\
				 color=colors.white)
		globalvars.intangibles_bottom.add(temp)


def resetDustOnTop():
	#Kill all the old dust.
	for d in globalvars.intangibles_bottom:
		if d.is_a == globalvars.DUST:
			d.kill()
	for d in globalvars.intangibles_top:
		if d.is_a == globalvars.DUST:
			d.kill()
	#Make 50 dust particles scattered around the player.
	for _ in range(50):
		size = rd.randint(1,4)
		x,y = getCoordsNearLoc(globalvars.player.rect.center, 50, 
				globalvars.WIDTH, globalvars.WIDTH)
		temp = objInstances.Dust(x=x, y=y, width=size, height=size,\
				 color=colors.white)
		globalvars.intangibles_top.add(temp)


def asteroids(seed=0):
	''' '''
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDustOnTop()
	#Display player location and speed info with the following:
	globalvars.intangibles_top.add(displayUtilities.ShipStatsText())

	rocks = ['bigrock','medrock','smallrock','gold','silver']
	#Reset the player's location to 0,0 and his speed to zero
	globalvars.player.loc = (0.0, 0.0)
	globalvars.player.speed = 0.0
	globalvars.player.targetSpeed = 0.0
	#Define an arena 2000 pixels across for the player and all the asteroids
	#to bounce around inside
	globalvars.arena = 1000 #1000 pixel radius centered at zero, zero.
	#Make the background color blue so that we can draw a black circle 
	#to show where the arena is located.
	globalvars.BGCOLOR = colors.blue
	#Draw a black circle and put it in intangibles to show the limits 
	#of the arena
	temp = objInstances.FixedCircle(x=0, y=0, radius=globalvars.arena, color=colors.black)
	globalvars.intangibles_bottom.add(temp)
	#Make 10 rocks centered around, but not on the player
	for _ in range(10):
		#Select a rock type
		rock = rocks[rd.randint(0, len(rocks)-1)]
		#Get the coordinates of the rock
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(globalvars.player.rect.center, mindist, maxdist, maxdist)
		#Make the rock
		temp = objInstances.Asteroid(x=x, y=y, image_name=rock)
		globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)

	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY,
		text='Watch out for asteroids while you',
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.intangibles_top.add(announcement)
	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52,
		text='blow them up to collect gems.',
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.intangibles_top.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.screen.fill(globalvars.BGCOLOR)
	pygame.display.flip()



def gemWild(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDustOnTop();
	#Reset the player's location to 0,0 and his speed to zero
	globalvars.player.loc = (0.0, 0.0)
	globalvars.player.speed = 0.0
	globalvars.player.targetSpeed = 0.0
	#Define an arena 2000 pixels across for the player and all the asteroids
	#to bounce around inside
	globalvars.arena = 1000 #1000 pixel radius centered at zero, zero.
	#Make the background color blue so that we can draw a black circle 
	#to show where the arena is located.
	globalvars.BGCOLOR = colors.blue
	#Draw a black circle and put it in intangibles to show the limits 
	#of the arena
	temp = objInstances.FixedCircle(x=0, y=0, radius=globalvars.arena, color=colors.black)
	globalvars.intangibles_bottom.add(temp)

	#Make 50 crystals centered around, but not on the player
	for _ in range(50):
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(globalvars.player.rect.center, mindist, maxdist, maxdist)
		temp = objInstances.Gem(x=x, y=y)
		globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)

	time_limit = 30 #time limit in seconds
	#Display timer and score count with the following:
	globalvars.score_keeper = displayUtilities.TimeLimitDisplay(time_limit=time_limit)
	globalvars.intangibles_top.add(globalvars.score_keeper)

	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text='Collect as many gems as you can in '+str(time_limit)+' seconds.',
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.intangibles_top.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.screen.fill(globalvars.BGCOLOR)
	pygame.display.flip()



def race(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	'''Race (infinite space) - player is given a destination and the clock 
	starts ticking. Space is populated pseudo randomly (deterministically) 
	with obstacles, enemies, gems.'''
	wipeOldScenario(); resetDust()
	#Reset the player's location to 0,0 and his speed to zero
	globalvars.player.loc = (0.0, 0.0)
	globalvars.player.speed = 0.0
	globalvars.player.targetSpeed = 0.0
	finish_line = (6000, 0)

	#Display timer with the following:
	globalvars.intangibles_top.add(displayUtilities.TimerDisplay(finish_line))
	#Display arrow to finish line
	globalvars.intangibles_top.add(displayUtilities.ArrowToDestination(finish_line))
	#Display finish bullseye
	globalvars.intangibles_top.add(objInstances.FinishBullsEye(finish_line))

	#determine what sorts of obstacles to put on the race course.
	numbers = [0 for _ in range(hudHelpers.capital_ship+1)]
	numbers[hudHelpers.enemy] = 3
	numbers[hudHelpers.crystal] = 5
	numbers[hudHelpers.large_asteroid] = 20
	numbers[hudHelpers.medium_asteroid] = 30
	numbers[hudHelpers.small_asteroid] = 40
	numbers[hudHelpers.gold_metal] = 5
	numbers[hudHelpers.silver_metal] = 6
	numbers[hudHelpers.health] = 7
	numbers[hudHelpers.capital_ship] = 0

	#Populate space in a semi narrow corridor between the player and the finish line
	course_length = 6000 #pixels
	course_height = 1000 #pixels
	#Midway between player and destination
	midway = (course_length/2, 0)

	hudHelpers.populateSpace(objects=numbers, width=course_length, height=course_height, center=midway, seed=rd.random())

	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text='Welcome to the race!',
		timeOff=0.3, timeOn=0.5, ttl=3, fontSize=52)
	globalvars.intangibles_top.add(announcement)
	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52, 
		text='Follow the yellow arrow',
		timeOff=0.3, timeOn=0.5, ttl=3, fontSize=52)
	globalvars.intangibles_top.add(announcement)
	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52*2,
		text='to the finish as fast as possible.',
		timeOff=0.3, timeOn=0.5, ttl=3, fontSize=52)
	globalvars.intangibles_top.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.screen.fill(globalvars.BGCOLOR)
	pygame.display.flip()


def furball(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
	#Display player location and speed info with the following:
	globalvars.intangibles_top.add(displayUtilities.ShipStatsText())

	globalvars.BGIMAGE = displayUtilities.image_list['bggalaxies'].convert()

	#Make a few enemies near the player
	mindist = 200
	maxdist = 800
	x,y = getCoordsNearLoc(globalvars.player.rect.center, mindist, maxdist, maxdist)
	makeNewEnemy(x=x, y=y)

	x,y = getCoordsNearLoc(globalvars.player.rect.center, mindist, maxdist, maxdist)
	makeNewEnemy(x=x, y=y)

	x,y = getCoordsNearLoc(globalvars.player.rect.center, mindist, maxdist, maxdist)
	makeNewEnemy(x=x, y=y, weaponType='missile_mk1') #The third enemy gets a missile.

	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text='Fight off 3 enemy ships!',
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.intangibles_top.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.screen.blit(globalvars.BGIMAGE, (0,0))
	pygame.display.flip()


def capitalShipScenario(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
	#Display player location and speed info with the following:
	globalvars.intangibles_top.add(displayUtilities.ShipStatsText())

	globalvars.BGIMAGE = displayUtilities.image_list['bggalaxies'].convert()

	#Make the capital ship
	enemy_ship = capitalShip.CapitalShip(centerx=0, centery=400, image_name='bigShip')
	globalvars.tangibles.add(enemy_ship)
	globalvars.whiskerables.add(enemy_ship)

	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text='Blow up the capital ship!',
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.intangibles_top.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.screen.blit(globalvars.BGIMAGE, (0,0))
	pygame.display.flip()


def goToInfiniteSpace(nodeid):
	'''This is a helper method that enables the menu system to function more easily.
	nodeid of the infinite space and the seed to use to generate the space.'''
	#Update all the factions
	opportunity = globalvars.factions.update(nodeid)
	#Get the node that has the id that this portal will lead to
	n = globalvars.galaxy.getNode(nodeid)
	infiniteSpace(seed=nodeid, playerloc=n.loc, warps=n.connections)
	#Check for an opportunity. This is when a player is moving to a node that is
	#the target of an action from a faction.
	if not opportunity is None:
		globalvars.menu.setOpportunityPanel(opportunity)


#The distances between nodes in the galaxy view is proportional to the distance between warp portals in the regular ship view. The scaling factor is warpPortalScaling.
warpPortalScaling = 100
def infiniteSpace(seed=0, playerloc=(0.0,0.0), warps=None):
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()	
	#Reset the player's location to 0,0 and his speed to zero
	globalvars.player.loc = playerloc
	globalvars.player.speed = 0.0
	globalvars.player.targetSpeed = 0.0
	globalvars.player.nodeid = seed #Player's new node id is set to be the seed argument.
	globalvars.player.destinationNode = seed

	#Place warp portals
	allWarps = []
	if not warps is None:
		for w in warps:
			#Get the slope of the line from playerLoc to this warp
			angle = angleFromPosition(playerloc, w[1])
			scaledDistance = distance(playerloc, w[1]) * warpPortalScaling
			#print scaledDistance #TESTING
			x,y = translate(playerloc, angle, scaledDistance)
			temp = objInstances.WarpPortal(x=x, y=y, destinationNode=w[0],
						method=goToInfiniteSpace)
			globalvars.tangibles.add(temp)
			allWarps.append(temp)

	#Need a new hud helper that will generate the landscape and clean up distant objects on the fly.
	globalvars.intangibles_bottom.add(hudHelpers.InfiniteSpaceGenerator(seed=seed, warps=allWarps))
	#Display player location and speed info with the following:
	globalvars.intangibles_top.add(displayUtilities.ShipStatsText())

	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text='You\'ve arrived in system '+str(seed),
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.intangibles_top.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.screen.fill(globalvars.BGCOLOR)
	pygame.display.flip()


def setDestinationNode(nodeid):
	globalvars.player.destinationNode = nodeid
	#Find the infinite space generator
	destNodeLoc = None
	foundObjWithWarps = False
	for i in globalvars.intangibles_bottom:
		if hasattr(i, 'warps'):
			foundObjWithWarps = True
			#Get the location of the destination node
			for w in i.warps:
				if w.destinationNode == nodeid:
					destNodeLoc = w.rect.center
					break
			break
	#Error check
	if destNodeLoc is None:
		if foundObjWithWarps:
			print 'ERROR: The infiniteSpaceGenerator object was found in intangibles_bottom, but it has no warp with an id matching nodeid '+str(nodeid)+'. Exiting.'; exit()
		else:
			print 'Warning: cannot set destination node from here. No infiniteSpaceGenerator object was found in intangibles_bottom.'
	else:
		#Search through intangibles_top and remove any existing arrows
		for i in globalvars.intangibles_top:
			if i.is_a == globalvars.ARROW:
				globalvars.intangibles_top.remove(i)
		#Create a new arrow pointing to the destination node and add it to intangibles_top
		globalvars.intangibles_top.add(displayUtilities.ArrowToDestination(destNodeLoc))


def restart():
	'''Give the player a new ship and boot him to the testing scenario. '''
	globalvars.player = player.Player('ship')
	globalvars.menu.main_panel = None

	#Order matters. This has to go after making the new player.
	goToInfiniteSpace(0)

	#reset the death display countdown
	globalvars.deathcountdown = 15


def profile():
	'''Profile some of the functions in this file.'''
	import cProfile
	cProfile.runctx('for _ in range(10000): hudHelpers.getObstacles(seed=0)', globals(),locals(), 'profiling/getObstacles.profile')
	cProfile.runctx('for _ in range(1000): 	obstacles = hudHelpers.getObstacles(seed=0); hudHelpers.populateSpace(objects=obstacles, width=1000, height=1000, center=(0,0), seed=0)', globals(),locals(), 'profiling/populateSpace.profile')

