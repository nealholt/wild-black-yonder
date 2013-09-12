#Each method in this file takes a physical object and sets a profile for the object. For example, bulletProfile(pObject) will set pObject to have bullet characteristics. Then the bullet will call bulletProfile on itself. This, I think, will clean the code and reduce redundancy and voodoo constants.
import random as rd

def bulletProfile(pObject, direction):
	pObject.speed = 10.0
	pObject.theta = direction
	pObject.setColor((255,100,100))

def enemyProfile(pObject):
	pObject.setColor((100,255,255))

	#Go to max speed immediately.
	pObject.targetSpeed = pObject.maxSpeed

	#Give enemy reduced max speed relative to player
	pObject.maxSpeed = 2.0
	pObject.maxdtheta = 3.0

def playerProfile(pObject):
	#Go to max speed immediately.
	pObject.targetSpeed = pObject.maxSpeed

