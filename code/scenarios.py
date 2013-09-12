import pygame.sprite
from misc import wipeOldScenario
import objInstances
import colors
import random as rd
from geometry import getCoordsNearLoc, translate, distance
import ship
import displayUtilities
import globalvars
import math

def makeNewEnemy(x=0, y=0):
	enemy_ship = ship.Ship(centerx=x, centery=y, image_name='images/destroyer')
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


def populateSpace():
	'''This is the first draft of a method to randomly populate space with objects.
	This is currently called by the racing minigame.
	TODO TESTING.'''
	#Test variables START
	TESTING = True #Turn on and off testing.
	area_covered = 0
	collisions = 0
	num_removed = 0
	#Test variables END

	enemy = 0
	crystal = 1
	large_asteroid = 2
	medium_asteroid = 3
	small_asteroid = 4
	gold_metal = 5
	silver_metal = 6
	health = 7

	numbers = [0 for _ in range(health+1)]
	numbers[enemy] = 3
	numbers[crystal] = 5
	numbers[large_asteroid] = 20
	numbers[medium_asteroid] = 30
	numbers[small_asteroid] = 40
	numbers[gold_metal] = 5
	numbers[silver_metal] = 6
	numbers[health] = 7

	#Populate space in a semi narrow corridor between the player and the finish line
	course_length = 3000 #actually half length because getCoordsNearLoc doubles it
	course_height = 1000 #actually half height because getCoordsNearLoc doubles it
	#Midway between player and destination
	midway = course_length, 0

	physical_objs = []

	for _ in xrange(numbers[enemy]):
		x,y = getCoordsNearLoc(midway, 0, course_length, course_height)
		physical_objs.append(ship.Ship(centerx=x, centery=y, image_name='images/destroyer'))

	for _ in xrange(numbers[crystal]):
		x,y = getCoordsNearLoc(midway, 0, course_length, course_height)
		#Make gems stationary in the race for now.
		physical_objs.append(objInstances.Gem(x=x, y=y, speed_min=0., speed_max=0.))

	for _ in xrange(numbers[large_asteroid]):
		x,y = getCoordsNearLoc(midway, 0, course_length, course_height)
		physical_objs.append(objInstances.Asteroid(x=x, y=y, speed_min=0., speed_max=0., image_name='images/asteroidBigRoundTidied'))

	for _ in xrange(numbers[medium_asteroid]):
		x,y = getCoordsNearLoc(midway, 0, course_length, course_height)
		physical_objs.append(objInstances.Asteroid(x=x, y=y, speed_min=0., speed_max=0., image_name='images/asteroidWild2'))

	for _ in xrange(numbers[small_asteroid]):
		x,y = getCoordsNearLoc(midway, 0, course_length, course_height)
		physical_objs.append(objInstances.Asteroid(x=x, y=y, speed_min=0., speed_max=0., image_name='images/asteroidTempel'))

	for _ in xrange(numbers[gold_metal]):
		x,y = getCoordsNearLoc(midway, 0, course_length, course_height)
		physical_objs.append(objInstances.Asteroid(x=x, y=y, speed_min=0., speed_max=0., image_name='images/Sikhote_small'))

	for _ in xrange(numbers[silver_metal]):
		x,y = getCoordsNearLoc(midway, 0, course_length, course_height)
		physical_objs.append(objInstances.Asteroid(x=x, y=y, speed_min=0., speed_max=0., image_name='images/bournonite_30percent'))

	for _ in xrange(numbers[health]):
		x,y = getCoordsNearLoc(midway, 0, course_length, course_height)
		physical_objs.append(objInstances.HealthKit(x, y))

	#Prevent collisions.
	#The following copied from collisionHandling()
	physical_objs = sorted(physical_objs, \
			key=lambda c: c.rect.topleft[1]+c.rect.height,\
			reverse=True)
	#Nudge objects that collide apart.
	for i in xrange(len(physical_objs)):
		A = physical_objs[i]
		for j in xrange(i+1, len(physical_objs)):
			B = physical_objs[j]
			if A.rect.topleft[1] > B.rect.topleft[1]+B.rect.height:
				break
			else:
				if distance(A.rect.center, B.rect.center) > A.radius+B.radius:
					pass
				else:
					#They collide. Move them apart.
					if TESTING: collisions += 1
					magnitude = max(A.radius, B.radius)*2
					angle = A.getAngleToTarget(target=B)
					B.rect.center = translate(B.rect.center, angle, magnitude)
	#Put everything in tangibles and whiskerables unless they collide with any tangibles.
	for p in physical_objs:
		if pygame.sprite.spritecollideany(p, globalvars.tangibles):
			if TESTING: num_removed += 1
		else:
			if TESTING: area_covered += math.pi*p.radius**2
			globalvars.tangibles.add(p)
			globalvars.whiskerables.add(p)

	#Print testing feedback
	if TESTING:
		print 'Area covered: '+str(area_covered)
		temp = course_length*2 * course_height*2
		print 'compared to the total area '+str(temp)
		print 'fraction of area covered '+str(area_covered / temp)
		print 'Initial collisions: '+str(collisions)
		print 'Objects removed: '+str(num_removed)
		print 'from a total of '+str(sum(numbers))+' objects.'
		print 'Fraction of objects removed: '+str(float(num_removed)/float(sum(numbers)))


def testScenario00(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	initializeDust()

	wipeOldScenario(); resetDust()

	globalvars.hud_helper = displayUtilities.PlayerInfoDisplayer()

	globalvars.BGCOLOR = colors.black

	globalvars.BGIMAGE = displayUtilities.loadImage('images/ioOverJupiter' + displayUtilities.ext,\
			transparency=False)

	#Create motionless objects for reference purposes while testing.
	temp = objInstances.FixedBody(0, -100, image_name='images/TyDfN_tiny') #little crystal
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of TyDfN_tiny is '+str(temp.radius)
	temp = objInstances.FixedBody(200, 200, image_name='images/asteroidBigRoundTidied') #largest asteroid
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of asteroidBigRoundTidied is '+str(temp.radius)
	temp = objInstances.FixedBody(500, 500, image_name='images/asteroidWild2') #medium asteroid
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of asteroidWild2 is '+str(temp.radius)
	temp = objInstances.FixedBody(500, 0, image_name='images/asteroidTempel') #small asteroid
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of asteroidTempel is '+str(temp.radius)
	temp = objInstances.FixedBody(-500, -500, image_name='images/Sikhote_small') #goldish metal rock
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of Sikhote_small is '+str(temp.radius)
	temp = objInstances.FixedBody(-500, 300, image_name='images/bournonite_30percent') #silvery metal rock
	globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
	#print 'Radius of bournonite_30percent is '+str(temp.radius)

	temp = objInstances.HealthKit(-100, 0) #health pack
	globalvars.tangibles.add(temp)


def asteroids(seed=0):
	'''	'asteroidBigRoundTidied', \#largest asteroid
		'asteroidWild2', \#medium asteroid
		'asteroidTempel', \#small asteroid
		'Sikhote_small', \#goldish metal rock
		'bournonite_30percent' \#silvery metal rock
	'''
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
	globalvars.hud_helper = displayUtilities.PlayerInfoDisplayer()
	rocks = ['asteroidBigRoundTidied',\
		'asteroidWild2',\
		'asteroidTempel',\
		'Sikhote_small',\
		'bournonite_30percent'\
		]
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
		temp = objInstances.Asteroid(x=x, y=y,\
			image_name='images/'+rock)
		globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)


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

	#30 second time limit.
	globalvars.hud_helper = displayUtilities.TimeLimit(time_limit=30)


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
	globalvars.hud_helper = displayUtilities.TimeTrialAssistant(finish_line)
	populateSpace() #TODO TESTING


def furball(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	wipeOldScenario(); resetDust()
	globalvars.hud_helper = displayUtilities.PlayerInfoDisplayer()

	globalvars.BGIMAGE = displayUtilities.loadImage('images/galaxyLenses' + displayUtilities.ext,\
			transparency=False)

	#Make a few enemies near the player
	for _ in range(3):
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(globalvars.player.rect.center, mindist, maxdist, maxdist)
		makeNewEnemy(x=x, y=y)


def infiniteSpace(seed=0):
	rd.seed(seed) #Fix the seed for the random number generator.

	#wipeOldScenario(); resetDust()
	#globalvars.hud_helper = displayUtilities.PlayerInfoDisplayer()
	print 'infinite space. TODO Not yet implemented. Will require some interesting new functions.'

