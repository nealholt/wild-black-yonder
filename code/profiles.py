import weapon
import engine
#Each method in this file takes a physical object and sets a profile for the object. For example, bulletProfile(pObject) will set pObject to have bullet characteristics. Then the bullet will call bulletProfile on itself. This, I think, will clean the code and reduce redundancy and voodoo constants.

def shipProfile(ship, profile='default'):
	if profile == 'default':
		#Give enemy a weapon
		ship.setWeapon('mk1')
		#Give enemy an engine
		ship.engine = engine.Engine()
		engine.setProfile('mk1', ship.engine)
		#return 'destroyer' #Return the image to use
	elif profile.startswith('mk'):
		#Give enemy a weapon
		ship.setWeapon(profile)
		#Give enemy an engine
		ship.engine = engine.Engine()
		engine.setProfile(profile, ship.engine)
		#return 'destroyer' #Return the image to use


