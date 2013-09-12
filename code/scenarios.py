import game
import objInstances
import colors

def testScenario00():
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

	game.BGCOLOR = colors.black

	#You must return something so that this is an expression and not a statement, because this is likely to be used in a lambda and lambdas only take expressions, not statements:
	#http://mail.python.org/pipermail/tutor/2007-July/055260.html
	return True


def asteroids():
	print 'asteroids'

def gemWild():
	print 'gemwild'

def race():
	print 'race'

def furball():
	print 'furball'

def infiniteSpace():
	print 'infinite space'

