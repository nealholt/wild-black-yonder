#This file contains all the classes that are used as heads up displays for various scenarios.
import pygame
import colors
import time
import globalvars
import displayUtilities
import random as rd
from geometry import getCoordsNearLoc
import objInstances
import ship
import capitalShip
import sys
sys.path.append('code/cython')
import cygeometry

def getNewEnemy(x,y,image_name,ship_tech,engine_tech,gun_tech,missile_tech,mine_tech):
	temp = ship.generateShip(ship_tech, x=x, y=y, image=image_name)
	temp.initialize()
	temp.gun = ship.weapon.generateWeapon(gun_tech)
	temp.gun.shooter = temp
	temp.missile = ship.missile.generateMissile(missile_tech)
	temp.missile.shooter = temp
	temp.mine = ship.mine.generateMine(mine_tech)
	temp.mine.shooter = temp
	temp.engine = ship.engine.generateEngine(engine_tech)
	temp.engineUpdate()
	return temp

def addNewEnemyToWorld(newship, add_to_blue=False):
	newship.setHealthBar()
	globalvars.tangibles.add(newship)
	globalvars.whiskerables.add(newship)
	if add_to_blue:
		newship.team = globalvars.BLUETEAM
		globalvars.BLUE_TEAM.add(newship)
	else:
		newship.team = globalvars.REDTEAM
		globalvars.RED_TEAM.add(newship)

def getNewCapitalShip(x,y):
	temp = capitalShip.CapitalShip(centerx=x, centery=y, image_name='bigShip')
	return temp

def getObstacles(seed=0,
		enemy_min = 0.0,
		enemy_max = 1.2,
		crystal_min = 0.0,
		crystal_max = 1.3,
		large_asteroid_min = 0.0,
		large_asteroid_max = 3.0,
		medium_asteroid_min = 0.0,
		medium_asteroid_max = 4.0,
		small_asteroid_min = 0.0,
		small_asteroid_max = 5.0,
		gold_metal_min = 0.0,
		gold_metal_max = 2.0,
		silver_metal_min = 0.0,
		silver_metal_max = 2.0,
		health_min = 0.0,
		health_max = 1.5,
		capital_ship_min = 0.0,
		capital_ship_max = 1.1,
		fuel_min = 0.0,
		fuel_max = 1.1,
		planet_min = 0.0,
		planet_max = 1.1):
	rd.seed(seed) #Fix the seed for the random number generator.
	numbers = [0 for _ in range(planet+1)]
	numbers[enemy] = int(rd.uniform(enemy_min, enemy_max))
	numbers[crystal] = int(rd.uniform(crystal_min, crystal_max))
	numbers[large_asteroid] = int(rd.uniform(large_asteroid_min, large_asteroid_max))
	numbers[medium_asteroid] = int(rd.uniform(medium_asteroid_min, medium_asteroid_max))
	numbers[small_asteroid] = int(rd.uniform(small_asteroid_min, small_asteroid_max))
	numbers[gold_metal] = int(rd.uniform(gold_metal_min, gold_metal_max))
	numbers[silver_metal] = int(rd.uniform(silver_metal_min, silver_metal_max))
	numbers[health] = int(rd.uniform(health_min, health_max))
	numbers[capital_ship] = int(rd.uniform(capital_ship_min, capital_ship_max))
	numbers[fuel] = int(rd.uniform(fuel_min, fuel_max))
	numbers[planet] = int(rd.uniform(planet_min, planet_max))
	return numbers


enemy = 0
crystal = 1
large_asteroid = 2
medium_asteroid = 3
small_asteroid = 4
gold_metal = 5
silver_metal = 6
health = 7
capital_ship = 8
fuel = 9
planet = 10
def populateSpace(objects=None, width=1000, height=1000, center=(0,0), seed=0., ship_tech=0, engine_tech=0, weapon_tech=0, missile_tech=0, mine_tech=0):
	'''This is the first draft of a method to randomly populate space with objects.
	This is currently called by the racing minigame.
	Pre: objects is an array of natural numbers specifying how
	many of each of a variety of objects should be placed in the space.
	width is a nat specifying the width of the rectangle of space to be populated.
	height is a nat specifying the height.
	center is where the center of the rectangle should be positioned.
	Post: '''
	#print 'TESTING populate '+str(width)+'x'+str(height)+' space centered at '+str(center)
	#Test variables START
	TESTING = False #True #Turn on and off testing.
	area_covered = 0
	collisions = 0
	num_removed = 0
	#Test variables END

	rd.seed(seed) #Fix the seed for the random number generator.
	
	#Populate space in a semi narrow corridor between the player and the finish line
	course_length = width/2 #actually half length because getCoordsNearLoc doubles it
	course_height = height/2 #actually half height because getCoordsNearLoc doubles it

	physical_objs = []

	for _ in xrange(objects[capital_ship]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		enemy_ship = getNewCapitalShip(x,y)
		physical_objs.append(enemy_ship)

	for _ in xrange(objects[enemy]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		#Generate a pirate ship with the node's level of tech
		temp = getNewEnemy(x,y,'destroyer',\
					ship_tech, \
					engine_tech, \
					weapon_tech, \
					missile_tech, \
					mine_tech)
		physical_objs.append(temp)

	for _ in xrange(objects[crystal]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		physical_objs.append(objInstances.Gem(x=x, y=y, speed_min=0., speed_max=0.))

	for _ in xrange(objects[large_asteroid]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		physical_objs.append(objInstances.Asteroid(x=x, y=y, speed_min=0., speed_max=0., image_name='bigrock'))

	for _ in xrange(objects[medium_asteroid]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		physical_objs.append(objInstances.Asteroid(x=x, y=y, speed_min=0., speed_max=0., image_name='medrock'))

	for _ in xrange(objects[small_asteroid]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		physical_objs.append(objInstances.Asteroid(x=x, y=y, speed_min=0., speed_max=0., image_name='smallrock'))

	for _ in xrange(objects[gold_metal]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		physical_objs.append(objInstances.Asteroid(x=x, y=y, speed_min=0., speed_max=0., image_name='gold'))

	for _ in xrange(objects[silver_metal]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		physical_objs.append(objInstances.Asteroid(x=x, y=y, speed_min=0., speed_max=0., image_name='silver'))

	for _ in xrange(objects[health]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		physical_objs.append(objInstances.HealthKit(x, y))

	for _ in xrange(objects[fuel]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		physical_objs.append(objInstances.GasStation(x, y))

	for _ in xrange(objects[planet]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		physical_objs.append(objInstances.Planet(x, y))

	#Prevent collisions.
	#The following copied from collisionHandling()
	physical_objs = sorted(physical_objs, \
			key=lambda c: c.rect.bottom,\
			reverse=True)
	#Nudge objects that collide apart.
	#This code is the same as the code used in setClosestSprites and collisionHandling
	for i in xrange(len(physical_objs)):
		A = physical_objs[i]
		for j in xrange(i+1, len(physical_objs)):
			B = physical_objs[j]
			if A.rect.top > B.rect.bottom:
				break
			else:
				if cygeometry.distance(A.rect.center, B.rect.center) > A.collisionradius+B.collisionradius:
					pass
				else:
					#They collide. Move them apart.
					if TESTING: collisions += 1
					magnitude = max(A.collisionradius, B.collisionradius)*2
					angle = A.getAngleToTarget(target=B)
					B.translate(angle, magnitude)

	#Put everything in tangibles and whiskerables unless they collide with any tangibles.
	toreturn = pygame.sprite.Group()
	for p in physical_objs:
		temp = pygame.sprite.spritecollideany(p, globalvars.tangibles)
		#print temp
		if temp is None:
			if TESTING: area_covered += math.pi*p.collisionradius**2
			#Set the ship's health bar. This must be done right 
			#before adding any ship to tangibles
			#It cannot be done earlier in this method because a ship
			#might collide with an object and not be added, but setHealthBar
			#puts the health bar in intangibles so the health bar ends up
			#floating in space with no one to ever remove it.
			if p.is_a == globalvars.SHIP or p.is_a == globalvars.CAPITALSHIP:
				addNewEnemyToWorld(p)
			else:
				globalvars.tangibles.add(p)
				globalvars.whiskerables.add(p)
			toreturn.add(p)
		else:
			if TESTING: num_removed += 1

	#Print testing feedback
	if TESTING:
		print 'Area covered: '+str(area_covered)
		temp = course_length*2 * course_height*2
		print 'compared to the total area '+str(temp)
		print 'fraction of area covered '+str(area_covered / temp)
		print 'Initial collisions: '+str(collisions)
		print 'Objects removed: '+str(num_removed)
		print 'from a total of '+str(sum(objects))+' objects.'
		print 'Fraction of objects removed: '+str(float(num_removed)/float(sum(objects)))
	return toreturn


class InfiniteSpaceGenerator(pygame.sprite.Sprite):
	'''An object which will deterministically but randomly generate
	objects in space based on the player's location.
	The player can fly around freely and objects will be automatically 
	and randomly but deterministically generated ahead of the player. These 
	objects will also be removed when they get too far from the player.
	This allows the player to explore in effectively infinite space.'''
        def __init__(self, seed=0):
		pygame.sprite.Sprite.__init__(self)
		#The node that this infinite space generator is generating space for.
		self.node = globalvars.galaxy.getNode(seed)
		#Distance above which to depopulate the grid cells.
		self.depopulatedistance = 4
		self.seed = seed
		self.dict = dict()
		self.space_length = 1000
		#Keep local track of the player's location.
		#This can make the update more efficient.
		self.playerx = None
		self.playery = None
		#Get the player's location.
		#Player's location divided by the length of each cell is the square the player is currently in.
		px,py = globalvars.player.rect.center
		#print 'Testing: player\'s location'+str((px,py))
		px = px / self.space_length
		py = py / self.space_length
		#Generate obstacles in player's location and put them in the dictionary. You might want to modify populateSpace to return its newly created physical objects so they can be tracked here for easy removal later.
		loc = str(px).zfill(3)+str(py).zfill(3)
		obstacles = getObstacles(seed=loc,
			enemy_min=self.node.enemy_min,
			enemy_max=self.node.enemy_max,
			crystal_min=self.node.crystal_min,
			crystal_max=self.node.crystal_max,
			large_asteroid_min=self.node.large_asteroid_min,
			large_asteroid_max=self.node.large_asteroid_max,
			medium_asteroid_min=self.node.medium_asteroid_min,
			medium_asteroid_max=self.node.medium_asteroid_max,
			small_asteroid_min=self.node.small_asteroid_min,
			small_asteroid_max=self.node.small_asteroid_max,
			gold_metal_min=self.node.gold_metal_min,
			gold_metal_max=self.node.gold_metal_max,
			silver_metal_min=self.node.silver_metal_min,
			silver_metal_max=self.node.silver_metal_max,
			health_min=self.node.health_min,
			health_max=self.node.health_max,
			capital_ship_min=self.node.capital_ship_min,
			capital_ship_max=self.node.capital_ship_max,
			fuel_min=self.node.fuel_min,
			fuel_max=self.node.fuel_max,
			planet_min=self.node.planet_min,
			planet_max=self.node.planet_max)
		self.dict[loc] = populateSpace(objects=obstacles, 
			width=self.space_length, height=self.space_length, 
			center=(px*self.space_length, py*self.space_length), seed=loc, ship_tech=self.node.pirate_ship_tech, engine_tech=self.node.pirate_engine_tech, weapon_tech=self.node.pirate_weapon_tech, missile_tech=self.node.pirate_missile_tech, mine_tech=self.node.pirate_mine_tech)
		#print 'testing keys in the dictionary: '+str(self.dict.keys())
		#print 'end of InfiniteSpaceGenerator'

		#Keep an index into the dictionary's list of keys. At each update, check the next key and if it is too distant from the player, then delete it.
		self.key_index = 0
		self.useOffset = False
		self.rect = pygame.Rect(0,0,0,0)

	def update(self):
		#Get the player's location.
		px,py = globalvars.player.rect.center
		#Player's location divided by the length of each cell is the 
		#square the player is currently in.
		px = px / self.space_length
		py = py / self.space_length

		#The following is redundant with code in game.py, but for now, who cares.
		offsetx = px - globalvars.CENTERX
		offsety = py - globalvars.CENTERY
		offset = offsetx, offsety

		#Check to see if the player has moved into a
		#different grid cell
		if px == self.playerx and py == self.playery:
			#Remove objects in grid cells too far from the player.
			#Check one cell each update
			keys = self.dict.keys()
			self.key_index = (self.key_index+1)%len(keys)
			key = keys[self.key_index]
			x = int(key[0:3])
			y = int(key[3:6])
			#Get the "grid distance" between the player's location and the x,y location. Grid distance is the distance on a grid allowing diagonal moves. It's pretty easy to verify that this is the larger of the differences between x1 and x2, and y1 and y2.
			dist = max(abs(px-x), abs(py-y))
			if dist > self.depopulatedistance:
				#print 'testing '+str((x,y))+' is more than distance '+str(self.depopulatedistance)+' from '+str((px,py))+' so we\'re gonna kill all the stuff in '+str((px,py))
				#print 'testing prior length of dictionary ('+str(len(self.dict.keys()))+') and tangibles ('+str(len(globalvars.tangibles.sprites()))+')'
				#Kill all of these too distant objects.
				for spr in self.dict[key]: spr.kill()
				#remove them from the dictionary.
				del self.dict[key]
				#print 'testing post length of dictionary ('+str(len(self.dict.keys()))+') and tangibles ('+str(len(globalvars.tangibles.sprites()))+')'
			return False

		#When the player changes cells, the frame rate does get buggered a bit.
		#I'm calling it good-enough for now.

		#print 'testing: player has moved into a new grid cell. previous cell was '+str((self.playerx, self.playery))
		#Update records of player's location
		self.playerx = px
		self.playery = py

		#Make sure all 8 grid cells around the player are populated.
		#If not, populate them.
		#check if these are in the dictionary and if not, populate them.

		#-1,-1 -1,0 -1,2
		# 0,0  0,1  0,2
 		# 1,0  1,1  1,2

		#use modular arithmetic. to check what needs to be populated and reduce code length.
		#px,py = playercenter
		#for i in range(9):
		#  x = i/3 + px -1
		#  y = i%3 + py -1
		for i in range(9):
			x = i/3 + px -1
			y = i%3 + py -1
			#print x,y #TESTING
			loc = str(x).zfill(3)+str(y).zfill(3)
			if not loc in self.dict.keys():
				#print 'testing the location '+str(loc)+' is empty so we are populating it'
				obstacles = getObstacles(seed=loc,
					enemy_min=self.node.enemy_min,
					enemy_max=self.node.enemy_max,
					crystal_min=self.node.crystal_min,
					crystal_max=self.node.crystal_max,
					large_asteroid_min=self.node.large_asteroid_min,
					large_asteroid_max=self.node.large_asteroid_max,
					medium_asteroid_min=self.node.medium_asteroid_min,
					medium_asteroid_max=self.node.medium_asteroid_max,
					small_asteroid_min=self.node.small_asteroid_min,
					small_asteroid_max=self.node.small_asteroid_max,
					gold_metal_min=self.node.gold_metal_min,
					gold_metal_max=self.node.gold_metal_max,
					silver_metal_min=self.node.silver_metal_min,
					silver_metal_max=self.node.silver_metal_max,
					health_min=self.node.health_min,
					health_max=self.node.health_max,
					capital_ship_min=self.node.capital_ship_min,
					capital_ship_max=self.node.capital_ship_max)
				self.dict[loc] = populateSpace(objects=obstacles, 
					width=self.space_length, height=self.space_length, 
					center=(x*self.space_length, y*self.space_length), seed=loc,
					ship_tech=self.node.pirate_ship_tech,
					engine_tech=self.node.pirate_engine_tech,
					weapon_tech=self.node.pirate_weapon_tech,
					missile_tech=self.node.pirate_missile_tech,
					mine_tech=self.node.pirate_mine_tech)
		return False

	def draw(self, _):
		pass

	def isOnScreen(self, _):
		return True

