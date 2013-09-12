import game
import objInstances
import colors
import random as rd
from geometry import getCoordsNearLoc
import ship


def makeNewEnemy(x=0, y=0):
	enemy_ship = ship.Ship(top=y, left=x, image_name='images/destroyer')
	game.tangibles.add(enemy_ship)
	game.whiskerables.add(enemy_ship)


def wipeOldScenario():
	for sprt in game.tangibles: sprt.kill()
	for sprt in game.intangibles: sprt.kill()
	for sprt in game.whiskerables: sprt.kill()

	#Add the player back in.
	game.tangibles.add(game.player)
	game.player.setHealthBar()

	#Immediately clear the panel
	game.game_obj.panel = None


def testScenario00():
	wipeOldScenario()

	game.BGCOLOR = colors.black

	#Create motionless objects for reference purposes while testing.
	temp = objInstances.FixedBody(0, -100, image_name='images/TyDfN_tiny') #little crystal
	game.tangibles.add(temp); game.whiskerables.add(temp)
	#print 'Radius of TyDfN_tiny is '+str(temp.radius)
	temp = objInstances.FixedBody(0, 0, image_name='images/asteroidBigRoundTidied') #largest asteroid
	game.tangibles.add(temp); game.whiskerables.add(temp)
	#print 'Radius of asteroidBigRoundTidied is '+str(temp.radius)
	temp = objInstances.FixedBody(500, 500, image_name='images/asteroidWild2') #medium asteroid
	game.tangibles.add(temp); game.whiskerables.add(temp)
	#print 'Radius of asteroidWild2 is '+str(temp.radius)
	temp = objInstances.FixedBody(500, 0, image_name='images/asteroidTempel') #small asteroid
	game.tangibles.add(temp); game.whiskerables.add(temp)
	#print 'Radius of asteroidTempel is '+str(temp.radius)
	temp = objInstances.FixedBody(-500, -500, image_name='images/Sikhote_small') #goldish metal rock
	game.tangibles.add(temp); game.whiskerables.add(temp)
	#print 'Radius of Sikhote_small is '+str(temp.radius)
	temp = objInstances.FixedBody(-500, 0, image_name='images/bournonite_30percent') #silvery metal rock
	game.tangibles.add(temp); game.whiskerables.add(temp)
	#print 'Radius of bournonite_30percent is '+str(temp.radius)

	temp = objInstances.HealthKit(-100, 0) #health pack
	game.tangibles.add(temp)


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
	#Make 10 rocks centered around, but not on the player
	for _ in range(10):
		#Select a rock type
		rock = rocks[rd.randint(0, len(rocks)-1)]
		#Get the coordinates of the rock
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(game.player.rect.center, mindist, maxdist)
		#Make the rock
		temp = objInstances.FixedBody(x, y, image_name='images/'+rock)
		game.tangibles.add(temp); game.whiskerables.add(temp)


def gemWild():
	wipeOldScenario()
	#Make 50 crystals centered around, but not on the player
	for _ in range(50):
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(game.player.rect.center, mindist, maxdist)
		temp = objInstances.FixedBody(x, y, image_name='images/TyDfN_tiny')
		game.tangibles.add(temp); game.whiskerables.add(temp)


def race():
	wipeOldScenario()
	x,y = game.player.rect.center
	#Make a rectangle down and to the right of the player. Later you will want a timer, obstacles, and an arrow or other indicator to the destination. 
	temp = objInstances.FixedBody(x+500, y+500)
	game.intangibles.add(temp)


def furball():
	wipeOldScenario()
	#Make a few enemies near the player
	for _ in range(3):
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(game.player.rect.center, mindist, maxdist)
		makeNewEnemy(x=x, y=y)


def infiniteSpace():
	#wipeOldScenario()
	print 'infinite space. TODO Not yet implemented. Will require some interesting new functions.'

