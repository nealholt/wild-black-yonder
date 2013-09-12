import weapon
import engine
#Each method in this file takes a physical object and sets a profile for the object. For example, bulletProfile(pObject) will set pObject to have bullet characteristics. Then the bullet will call bulletProfile on itself. This, I think, will clean the code and reduce redundancy and voodoo constants.

def enemyProfile(ship, profile='default'):
	if profile == 'default':
		ship.setColor((100,255,255))
		#Give enemy a weapon
		w = weapon.Weapon()
		weapon.setProfile('mk1', w)
		ship.weapons.append(w)
		#Give enemy an engine
		ship.engine = engine.Engine()
		engine.setProfile('mk1', ship.engine)

def playerProfile(pObject):
	pObject.maxSpeed = 20.0
	#Turn rate:
	pObject.dtheta = 8.0

def followerProfile(pObject):
	'''This is the object that invisibly follows the player and the screen centers on it.
	This mechanism was intended to give a sense of speed and direction.'''
	pObject.setColor((155,155,0))
	pObject.maxSpeed = 10.0
	pObject.dv = 0.5 #acceleration
	#Turn rate:
	pObject.dtheta = 10.0

