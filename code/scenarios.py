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
	globalvars.intangibles.empty()
	globalvars.whiskerables.empty()

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


def resetDust():
	#Kill all the old dust.
	for d in globalvars.intangibles:
		if d.is_a == globalvars.DUST:
			d.kill()
	#Make 50 dust particles scattered around the player.
	for _ in range(50):
		size = rd.randint(1,4)
		x,y = getCoordsNearLoc(globalvars.player.rect.center, 50, 
				globalvars.WIDTH, globalvars.WIDTH)
		temp = objInstances.Dust(x=x, y=y, width=size, height=size,\
				 color=colors.white)
		globalvars.intangibles.add(temp)


def testScenario00(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
	#TODO: temporary HUD that does nothing. You want to move the code away from this.
	globalvars.hud_helper = hudHelpers.Hud()
	#Display player location and speed info with the following:
	globalvars.intangibles.add(displayUtilities.ShipStatsText())

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

	temp = objInstances.Explosion(x=200,y=-150)
	globalvars.tangibles.add(temp);

	temp = objInstances.HealthKit(-100, 0) #health pack
	globalvars.tangibles.add(temp)
	
	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY,
		text='Press H to access the help menu',
		timeOff=0, timeOn=1, ttl=3.0, fontSize=52)
	globalvars.intangibles.add(announcement)
	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52,
		text=' and learn the controls.',
		timeOff=0, timeOn=1, ttl=3.0, fontSize=52)
	globalvars.intangibles.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.BGCOLOR = colors.black
	globalvars.BGIMAGE = displayUtilities.image_list['bgjupiter'].convert()
	globalvars.screen.blit(globalvars.BGIMAGE, (0,0))
	pygame.display.flip()


def asteroids(seed=0):
	''' '''
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
	#TODO: temporary HUD that does nothing. You want to move the code away from this.
	globalvars.hud_helper = hudHelpers.Hud()
	#Display player location and speed info with the following:
	globalvars.intangibles.add(displayUtilities.ShipStatsText())

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
	#globalvars.intangibles.insert(0,temp)
	#TODO now that intangibles is a sprite group, you may need some other way of prioritizing what gets drawn in what order. SHIT now I remember why intangibles was a list and not a sprite group.
	globalvars.intangibles.add(temp)
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
	globalvars.intangibles.add(announcement)
	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52,
		text='blow them up to collect gems.',
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.intangibles.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.screen.fill(globalvars.BGCOLOR)
	pygame.display.flip()



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
	#globalvars.intangibles.insert(0,temp)
	#TODO now that intangibles is a sprite group, you may need some other way of prioritizing what gets drawn in what order. SHIT now I remember why intangibles was a list and not a sprite group.
	globalvars.intangibles.add(temp)

	#Make 50 crystals centered around, but not on the player
	for _ in range(50):
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(globalvars.player.rect.center, mindist, maxdist, maxdist)
		temp = objInstances.Gem(x=x, y=y)
		globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)

	time_limit = 30 #time limit in seconds
	#TODO I'm just testing initially here. Ultimately I want to get rid of HUDs altogether and replace them with intangibles. Also, however, the following will not display the arrow or finish line which are important.
	globalvars.hud_helper = hudHelpers.Hud()
	#Display timer and score count with the following:
	globalvars.intangibles.add(displayUtilities.TimeLimitDisplay(time_limit=time_limit))

	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text='Collect as many gems as you can in '+str(time_limit)+' seconds.',
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.intangibles.add(announcement)

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

	#TODO I'm just testing initially here. Ultimately I want to get rid of HUDs altogether and replace them with intangibles. Also, however, the following will not display the arrow or finish line which are important.
	globalvars.hud_helper = hudHelpers.Hud()
	#Display timer with the following:
	globalvars.intangibles.add(displayUtilities.TimerDisplay(finish_line))
	#Display arrow to finish line
	globalvars.intangibles.add(displayUtilities.ArrowToDestination(finish_line))
	#Display finish bullseye
	globalvars.intangibles.add(objInstances.FinishBullsEye(finish_line))

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

	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text='Welcome to the race!',
		timeOff=0.3, timeOn=0.5, ttl=3, fontSize=52)
	globalvars.intangibles.add(announcement)
	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52, 
		text='Follow the yellow arrow',
		timeOff=0.3, timeOn=0.5, ttl=3, fontSize=52)
	globalvars.intangibles.add(announcement)
	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52*2,
		text='to the finish as fast as possible.',
		timeOff=0.3, timeOn=0.5, ttl=3, fontSize=52)
	globalvars.intangibles.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.screen.fill(globalvars.BGCOLOR)
	pygame.display.flip()


def furball(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
	#TODO: temporary HUD that does nothing. You want to move the code away from this.
	globalvars.hud_helper = hudHelpers.Hud()
	#Display player location and speed info with the following:
	globalvars.intangibles.add(displayUtilities.ShipStatsText())

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
	globalvars.intangibles.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.screen.blit(globalvars.BGIMAGE, (0,0))
	pygame.display.flip()


def capitalShipScenario(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
	#TODO: temporary HUD that does nothing. You want to move the code away from this.
	globalvars.hud_helper = hudHelpers.Hud()
	#Display player location and speed info with the following:
	globalvars.intangibles.add(displayUtilities.ShipStatsText())

	globalvars.BGIMAGE = displayUtilities.image_list['bggalaxies'].convert()

	#Make the capital ship
	enemy_ship = capitalShip.CapitalShip(centerx=0, centery=400, image_name='bigShip')
	globalvars.tangibles.add(enemy_ship)
	globalvars.whiskerables.add(enemy_ship)

	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text='Blow up the capital ship!',
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.intangibles.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.screen.blit(globalvars.BGIMAGE, (0,0))
	pygame.display.flip()


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
	#globalvars.hud_helper = hudHelpers.InfiniteSpaceGenerator(seed=seed, warps=allWarps)
	globalvars.intangibles.add(hudHelpers.InfiniteSpaceGenerator(seed=seed, warps=allWarps))
	#TODO: temporary HUD that does nothing. You want to move the code away from this.
	globalvars.hud_helper = hudHelpers.Hud()
	#Display player location and speed info with the following:
	globalvars.intangibles.add(displayUtilities.ShipStatsText())

	announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
		text='You\'ve arrived in system '+str(seed),
		timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
	globalvars.intangibles.add(announcement)

	#Draw the new background and flip the whole screen.
	globalvars.screen.fill(globalvars.BGCOLOR)
	pygame.display.flip()


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

