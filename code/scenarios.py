import game
import objInstances
import colors
import random as rd
from math import sqrt


def wipeOldScenario():
	for sprt in game.tangibles: sprt.kill()
	for sprt in game.intangibles: sprt.kill()
	for sprt in game.whiskerables: sprt.kill()

	#Add the player back in.
	game.tangibles.add(game.player)
	game.player.setHealthBar()

	#Immediately clear the panel
	game.game_obj.panel = None


def distance(p1, p2):
	#TODO move this into a common file.
	return sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )


adjustments = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,-1)]
def getCoordsNearLoc(loc, mindist, maxdist):
	'''Returns random coordinates with maxdistx in the x direction
	and within maxdisty in the y direction of the location, loc, 
	but not within bufferdist of the loc.'''
	x = rd.randint(-maxdist, maxdist)+loc[0]
	y = rd.randint(-maxdist, maxdist)+loc[1]
	adjust = adjustments[ rd.randint(0,len(adjustments)-1) ]
	while distance((x,y), loc) < mindist:
		x = x+adjust[0]
		y = y+adjust[1]
	return x,y


def testScenario00():
	wipeOldScenario()

	game.BGCOLOR = colors.black

	#Create motionless objects for reference purposes while testing.
	temp = objInstances.FixedBody(0, -100, image_name='images/TyDfN_tiny') #little crystal
	game.tangibles.add(temp); game.whiskerables.add(temp)
	print 'Radius of TyDfN_tiny is '+str(temp.radius)
	temp = objInstances.FixedBody(0, 0, image_name='images/asteroidBigRoundTidied') #largest asteroid
	game.tangibles.add(temp); game.whiskerables.add(temp)
	print 'Radius of asteroidBigRoundTidied is '+str(temp.radius)
	temp = objInstances.FixedBody(500, 500, image_name='images/asteroidWild2') #medium asteroid
	game.tangibles.add(temp); game.whiskerables.add(temp)
	print 'Radius of asteroidWild2 is '+str(temp.radius)
	temp = objInstances.FixedBody(500, 0, image_name='images/asteroidTempel') #small asteroid
	game.tangibles.add(temp); game.whiskerables.add(temp)
	print 'Radius of asteroidTempel is '+str(temp.radius)
	temp = objInstances.FixedBody(-500, -500, image_name='images/Sikhote_small') #goldish metal rock
	game.tangibles.add(temp); game.whiskerables.add(temp)
	print 'Radius of Sikhote_small is '+str(temp.radius)
	temp = objInstances.FixedBody(-500, 0, image_name='images/bournonite_30percent') #silvery metal rock
	game.tangibles.add(temp); game.whiskerables.add(temp)
	print 'Radius of bournonite_30percent is '+str(temp.radius)

	temp = objInstances.HealthKit(-100, 0) #health pack
	game.tangibles.add(temp)

	#TODO. since you didn't end up using lambdas, I'm not sure the following applies anymore.
	#You must return something so that this is an expression and not a statement, because this is likely to be used in a lambda and lambdas only take expressions, not statements:
	#http://mail.python.org/pipermail/tutor/2007-July/055260.html
	return True


def asteroids():
	'''	'asteroidBigRoundTidied', \#largest asteroid
		'asteroidWild2', \#medium asteroid
		'asteroidTempel', \#small asteroid
		'Sikhote_small', \#goldish metal rock
		'bournonite_30percent' \#silvery metal rock
	'''
	wipeOldScenario()
	rocks = ['asteroidBigRoundTidied',\
		'asteroidWild2',\
		'asteroidTempel',\
		'Sikhote_small',\
		'bournonite_30percent'\
		]
	player_center = game.player.getCenter()
	#Make 10 rocks centered around, but not on the player
	for _ in range(10):
		#Select a rock type
		rock = rocks[rd.randint(0, len(rocks)-1)]
		#Get the coordinates of the rock
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(player_center, mindist, maxdist)
		#Make the rock
		temp = objInstances.FixedBody(x, y, image_name='images/'+rock)
		game.tangibles.add(temp); game.whiskerables.add(temp)


def gemWild():
	wipeOldScenario()
	player_center = game.player.getCenter()
	#Make 50 crystals centered around, but not on the player
	for _ in range(50):
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(player_center, mindist, maxdist)
		temp = objInstances.FixedBody(x, y, image_name='images/TyDfN_tiny')
		game.tangibles.add(temp); game.whiskerables.add(temp)


def race():
	wipeOldScenario()
	x,y = game.player.getCenter()
	#Make a rectangle down and to the right of the player. Later you will want a timer, obstacles, and an arrow or other indicator to the destination. 
	temp = objInstances.FixedBody(x+500, y+500)
	game.intangibles.add(temp)


def furball():
	wipeOldScenario()
	player_center = game.player.getCenter()
	#Make a few enemies near the player
	for _ in range(3):
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(player_center, mindist, maxdist)
		game.makeNewEnemy(x=x, y=y)


def infiniteSpace():
	#wipeOldScenario()
	print 'infinite space. TODO Not yet implemented. Will require some interesting new functions.'

