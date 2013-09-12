import weapon
import engine
#Each method in this file takes a physical object and sets a profile for the object. For example, bulletProfile(pObject) will set pObject to have bullet characteristics. Then the bullet will call bulletProfile on itself. This, I think, will clean the code and reduce redundancy and voodoo constants.

def shipProfile(ship, profile='default'):
	if profile == 'default':
		#Give enemy a weapon
		w = weapon.Weapon()
		weapon.setProfile('mk1', w)
		ship.weapons = [w] #Previously we appended the weapon, but since player is a subclass of ship, it was getting the default weapon AND its own weapon which caused a weird bug, especially with bullets colliding with themselves.
		#Give enemy an engine
		ship.engine = engine.Engine()
		engine.setProfile('mk1', ship.engine)
		#return 'images/destroyer' #Return the image to use
	elif profile.startswith('mk'):
		#Give enemy a weapon
		w = weapon.Weapon()
		weapon.setProfile(profile, w)
		ship.weapons = [w] #Previously we appended the weapon, but since player is a subclass of ship, it was getting the default weapon AND its own weapon which caused a weird bug, especially with bullets colliding with themselves.
		#Give enemy an engine
		ship.engine = engine.Engine()
		engine.setProfile(profile, ship.engine)
		#return 'images/destroyer' #Return the image to use

def followerProfile(pObject):
	'''This is the object that invisibly follows the player and the screen centers on it.
	This mechanism was intended to give a sense of speed and direction.'''
	pObject.setColor((155,155,0))
	pObject.maxSpeed = 10.0
	pObject.dv = 0.5 #acceleration
	#Turn rate:
	pObject.dtheta = 10.0

