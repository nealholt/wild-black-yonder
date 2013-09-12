import game
import objInstances
import colors
import random as rd
from geometry import getCoordsNearLoc
import ship
import displayUtilities

def makeNewEnemy(x=0, y=0):
	enemy_ship = ship.Ship(centerx=x, centery=y, image_name='images/destroyer')
	game.tangibles.add(enemy_ship)
	game.whiskerables.add(enemy_ship)


#When a rock is blown up, what comes out?
subrocks = dict()
subrocks['images/asteroidBigRoundTidied'] = ('asteroidWild2', 4)
subrocks['images/asteroidWild2'] = ('asteroidTempel', 4)
subrocks['images/asteroidTempel'] = ('debris', 10)
subrocks['images/Sikhote_small'] = ('gem',1)
subrocks['images/bournonite_30percent'] = ('gem', 3)
def splitRock(image_name, centerx=0, centery=0):
	new_image, count = subrocks[image_name]
	if new_image == 'gem':
		for _ in range(count):
			temp = objInstances.Gem(x=centerx, y=centery)
			game.tangibles.add(temp)
			game.whiskerables.add(temp)
	elif new_image == 'debris':
		for _ in range(count):
			temp = objInstances.Debris(x=centerx, y=centery)
			game.tangibles.add(temp)
			game.whiskerables.add(temp)
	else:
		for _ in range(count):
			temp = objInstances.Asteroid(x=centerx, y=centery,
				image_name='images/'+new_image)
			game.tangibles.add(temp)
			game.whiskerables.add(temp)


def wipeOldScenario():
	for sprt in game.tangibles: sprt.kill()
	for sprt in game.intangibles: sprt.kill()
	for sprt in game.whiskerables: sprt.kill()

	#Add the player back in.
	game.tangibles.add(game.player)
	game.player.setHealthBar()

	#Immediately clear the panel
	game.game_obj.panel = None

	#Default the hud_helper to display player info
	game.hud_helper = displayUtilities.PlayerInfoDisplayer()

	#Reset the arena
	game.arena = 0


def testScenario00():
	wipeOldScenario()

	game.BGCOLOR = colors.black

	#Create motionless objects for reference purposes while testing.
	temp = objInstances.FixedBody(0, -100, image_name='images/TyDfN_tiny') #little crystal
	game.tangibles.add(temp); game.whiskerables.add(temp)
	#print 'Radius of TyDfN_tiny is '+str(temp.radius)
	temp = objInstances.FixedBody(200, 200, image_name='images/asteroidBigRoundTidied') #largest asteroid
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
	temp = objInstances.FixedBody(-500, 300, image_name='images/bournonite_30percent') #silvery metal rock
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
	#Reset the player's location to 0,0 and his speed to zero
	game.player.loc = (0.0, 0.0)
	game.player.speed = 0.0
	game.player.targetSpeed = 0.0
	#Define an arena 2000 pixels across for the player and all the asteroids
	#to bounce around inside
	game.arena = 1000 #1000 pixel radius centered at zero, zero.
	#Make the background color blue so that we can draw a black circle 
	#to show where the arena is located.
	game.BGCOLOR = colors.blue
	#Draw a black circle and put it in intangibles to show the limits 
	#of the arena
	temp = objInstances.FixedCircle(x=0, y=0, radius=game.arena, color=colors.black)
	game.intangibles.add(temp)
	#Make 10 rocks centered around, but not on the player
	for _ in range(10):
		#Select a rock type
		rock = rocks[rd.randint(0, len(rocks)-1)]
		#Get the coordinates of the rock
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(game.player.rect.center, mindist, maxdist)
		#Make the rock
		temp = objInstances.Asteroid(x=x, y=y,\
			image_name='images/'+rock)
		game.tangibles.add(temp); game.whiskerables.add(temp)


def gemWild():
	wipeOldScenario()
	#Make 50 crystals centered around, but not on the player
	for _ in range(50):
		mindist = 200
		maxdist = 800
		x,y = getCoordsNearLoc(game.player.rect.center, mindist, maxdist)
		temp = objInstances.Gem(x=x, y=y)
		game.tangibles.add(temp); game.whiskerables.add(temp)


def race():
	wipeOldScenario()
	#Reset the player's location to 0,0 and his speed to zero
	game.player.loc = (0.0, 0.0)
	game.player.speed = 0.0
	game.player.targetSpeed = 0.0
	finish_line = (500, 500)
	game.hud_helper = displayUtilities.TimeTrialAssistant(finish_line)


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

