import pygame.sprite
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
import misc


def wipeOldScenario():
	for sprt in globalvars.tangibles: sprt.kill()
	for sprt in globalvars.intangibles: sprt.kill()
	globalvars.intangibles = []
	for sprt in globalvars.whiskerables: sprt.kill()

	globalvars.BGCOLOR = colors.black
	globalvars.BGIMAGE = None

	#Add the player back in.
	globalvars.tangibles.add(globalvars.player)
	globalvars.player.setHealthBar()

	#Immediately clear the panel
	globalvars.panel = None

	#Reset the hud_helper
	globalvars.hud_helper = None

	#Reset the arena
	globalvars.arena = 0


def makeNewEnemy(x=0, y=0, weaponType='mk1'):
	enemy_ship = ship.Ship(centerx=x, centery=y, image_name='destroyer')
	enemy_ship.setWeapon(weaponType)
	globalvars.tangibles.add(enemy_ship)
	globalvars.whiskerables.add(enemy_ship)


def initializeDust():
	#Kill all the old dust.
	for d in globalvars.dust: d.kill()
	#Make 100 dust particles scattered around the player.
	globalvars.dust = []
	for _ in range(100):
		length = rd.randint(1,4)
		temp = objInstances.FixedBody(x=0, y=0, width=length, height=length,\
				 color=colors.white)
		globalvars.dust.append(temp)


def resetDust():
	for d in globalvars.dust:
		x,y = getCoordsNearLoc(globalvars.player.rect.center, 50, globalvars.WIDTH, globalvars.WIDTH)
		d.rect.center = (x,y)


def testScenario00(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	initializeDust()

	wipeOldScenario(); resetDust()

	globalvars.hud_helper = hudHelpers.PlayerInfoDisplayer()

	globalvars.BGCOLOR = colors.black

	globalvars.BGIMAGE = displayUtilities.image_list['bgjupiter'].convert()

	#Create motionless objects for reference purposes while testing.
	temp = objInstances.FixedBody(0, -100, image_name='gem') #little crystal
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of TyDfN_tiny is '+str(temp.collisionradius)
	temp = objInstances.FixedBody(200, 200, image_name='bigrock') #largest asteroid
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of asteroidBigRoundTidied is '+str(temp.collisionradius)
	temp = objInstances.FixedBody(500, 500, image_name='medrock') #medium asteroid
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of asteroidWild2 is '+str(temp.collisionradius)
	temp = objInstances.FixedBody(500, 0, image_name='smallrock') #small asteroid
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of asteroidTempel is '+str(temp.collisionradius)
	temp = objInstances.FixedBody(-500, -500, image_name='gold') #goldish metal rock
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of Sikhote_small is '+str(temp.collisionradius)
	temp = objInstances.FixedBody(-500, 300, image_name='silver') #silvery metal rock
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of bournonite_30percent is '+str(temp.collisionradius)

	temp = objInstances.HealthKit(-100, 0) #health pack
	globalvars.tangibles.add(temp)

	announcement = misc.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text=['Press H to access the help menu',
		' and learn the controls.'],
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.hud_helper.addObjectToUpdate(announcement)


def asteroids(seed=0):
	''' '''
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
	globalvars.hud_helper = hudHelpers.PlayerInfoDisplayer()
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
	#Insert at the beginning of intangibles so it doesn't draw over top of the health bars.
	globalvars.intangibles.insert(0,temp)
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

	announcement = misc.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text=['Watch out for asteroids while you',
			'blow them up to collect gems.'],
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.hud_helper.addObjectToUpdate(announcement)



def gemWild(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
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
	#Insert at the beginning of intangibles so it doesn't draw over top of the health bars.
	globalvars.intangibles.insert(0,temp)
	#Make 50 crystals centered around, but not on the player
	for _ in range(50):
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(globalvars.player.rect.center, mindist, maxdist, maxdist)
		temp = objInstances.Gem(x=x, y=y)
		globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)

	time_limit = 30 #time limit in seconds
	globalvars.hud_helper = hudHelpers.TimeLimit(time_limit=time_limit)

	announcement = misc.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text=['Collect as many gems as you can in '+str(time_limit)+' seconds.'],
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.hud_helper.addObjectToUpdate(announcement)



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
	globalvars.hud_helper = hudHelpers.TimeTrialAssistant(finish_line)

	#determine what sorts of obstacles to put on the race course.
	numbers = [0 for _ in range(hudHelpers.health+1)]
	numbers[hudHelpers.enemy] = 3
	numbers[hudHelpers.crystal] = 5
	numbers[hudHelpers.large_asteroid] = 20
	numbers[hudHelpers.medium_asteroid] = 30
	numbers[hudHelpers.small_asteroid] = 40
	numbers[hudHelpers.gold_metal] = 5
	numbers[hudHelpers.silver_metal] = 6
	numbers[hudHelpers.health] = 7

	#Populate space in a semi narrow corridor between the player and the finish line
	course_length = 6000 #pixels
	course_height = 1000 #pixels
	#Midway between player and destination
	midway = (course_length/2, 0)

	hudHelpers.populateSpace(objects=numbers, width=course_length, height=course_height, center=midway, seed=rd.random())

	announcement = misc.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text=['Welcome to the race!', 
		'Follow the yellow arrow', 
		'to the finish as fast as possible.'],
		timeOff=0.3, timeOn=0.5, ttl=3, fontSize=52)
	globalvars.hud_helper.addObjectToUpdate(announcement)


def furball(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
	globalvars.hud_helper = hudHelpers.PlayerInfoDisplayer()

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

	announcement = misc.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text=['Fight off 3 enemy ships!'],
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.hud_helper.addObjectToUpdate(announcement)



def capitalShipScenario(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
	globalvars.hud_helper = hudHelpers.PlayerInfoDisplayer()

	globalvars.BGIMAGE = displayUtilities.image_list['bggalaxies'].convert()

	#Make the capital ship
	enemy_ship = capitalShip.CapitalShip(centerx=0, centery=400, image_name='bigShip')
	globalvars.tangibles.add(enemy_ship)
	globalvars.whiskerables.add(enemy_ship)

	announcement = misc.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text=['Blow up the capital ship!'],
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.hud_helper.addObjectToUpdate(announcement)



def goToInfiniteSpace(nodeid):
	'''This is a helper method that enables the menu system to function more easily.
	nodeid of the infinite space and the seed to use to generate the space.'''
	#Get the node that has the id that this portal will lead to
	n = globalvars.localSystem.getNode(nodeid)
	infiniteSpace(seed=nodeid, playerloc=n.loc, warps=n.connections)


#The distances between nodes in the galaxy view is proportional to the distance between warp portals in the regular ship view. The scaling factor is warpPortalScaling.
warpPortalScaling = 25
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
	globalvars.hud_helper = hudHelpers.InfiniteSpaceGenerator(seed=seed, warps=allWarps)

	announcement = misc.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text=['You\'ve arrived in system '+str(seed)],
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.hud_helper.addObjectToUpdate(announcement)



def setDestinationNode(nodeid):
	globalvars.player.destinationNode = nodeid
	#Tell the hud helper to update its pointer arrow
	globalvars.hud_helper.setArrowTarget(nodeid)


def restart():
	'''Give the player a new ship and boot him to the testing scenario. '''
	globalvars.player = player.Player('ship')
	globalvars.panel = None

	#Order matters. This has to go after making the new player.
	testScenario00(seed=0)

	#reset the death display countdown
	globalvars.deathcountdown = 15


def profile():
	'''Profile some of the functions in this file.'''
	import cProfile
	cProfile.runctx('for _ in range(10000): hudHelpers.getObstacles(seed=0)', globals(),locals(), 'profiling/getObstacles.profile')
	cProfile.runctx('for _ in range(1000): 	obstacles = hudHelpers.getObstacles(seed=0); hudHelpers.populateSpace(objects=obstacles, width=1000, height=1000, center=(0,0), seed=0)', globals(),locals(), 'profiling/populateSpace.profile')

