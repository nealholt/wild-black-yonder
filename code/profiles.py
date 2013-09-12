#Each method in this file takes a physical object and sets a profile for the object. For example, bulletProfile(pObject) will set pObject to have bullet characteristics. Then the bullet will call bulletProfile on itself. This, I think, will clean the code and reduce redundancy and voodoo constants.
import random as rd

def bulletProfile(pObject, direction):
	pObject.speed = 10.0
	pObject.theta = direction
	pObject.setColor((255,100,100))


def enemyProfile(pObject):
	pObject.setColor((100,255,255))
	#Give enemy reduced max speed relative to player
	pObject.maxSpeed = 2.0
	#Go to max speed immediately.
	pObject.targetSpeed = pObject.maxSpeed
	#Turn rate:
	pObject.maxdtheta = 1.0


def playerProfile(pObject):
	#Go to max speed immediately.
	pObject.maxSpeed = 5.0
	pObject.targetSpeed = pObject.maxSpeed
	#Turn rate:
	pObject.maxdtheta = 8.0


def followerProfile(pObject):
	'''This is the object that invisibly follows the player and the screen centers on it.
	This mechanism was intended to give a sense of speed and direction.'''
	pObject.setColor((155,155,0))
	pObject.maxSpeed = 10.0
	pObject.dv = 0.5 #acceleration
	#Go to max speed immediately.
	pObject.targetSpeed = pObject.maxSpeed
	#Turn rate:
	pObject.maxdtheta = 180.0
	pObject.dtheta = 10.0
	pObject.ddtheta = 20.0

