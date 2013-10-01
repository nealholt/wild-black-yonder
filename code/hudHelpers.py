#This file contains all the classes that are used as heads up displays for various scenarios.
import pygame
import colors
import time
import globalvars
from misc import writeTextToScreen
import displayUtilities
import random as rd
from geometry import getCoordsNearLoc, distance
import objInstances
import ship


def getObstacles(seed=0):
	'''TODO later I want to get profiles instead of pure random number generation. '''
	rd.seed(seed) #Fix the seed for the random number generator.
	numbers = [0 for _ in range(health+1)]
	numbers[enemy] = 0 #rd.randint(0,2)
	numbers[crystal] = rd.randint(0,1)
	numbers[large_asteroid] = rd.randint(0,2)
	numbers[medium_asteroid] = rd.randint(1,4)
	numbers[small_asteroid] = rd.randint(2,4)
	numbers[gold_metal] = rd.randint(0,2)
	numbers[silver_metal] = rd.randint(0,2)
	numbers[health] = rd.randint(0,1)
	return numbers


enemy = 0
crystal = 1
large_asteroid = 2
medium_asteroid = 3
small_asteroid = 4
gold_metal = 5
silver_metal = 6
health = 7
def populateSpace(objects=None, width=1000, height=1000, center=(0,0), seed=0.):
	'''This is the first draft of a method to randomly populate space with objects.
	This is currently called by the racing minigame.
	Pre: objects is an array of natural numbers specifying how
	many of each of a variety of objects should be placed in the space.
	width is a nat specifying the width of the rectangle of space to be populated.
	height is a nat specifying the height.
	center is where the center of the rectangle should be positioned.
	Post: 
	TODO TESTING.'''
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

	for _ in xrange(objects[enemy]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		physical_objs.append(ship.Ship(centerx=x, centery=y, image_name='destroyer'))

	for _ in xrange(objects[crystal]):
		x,y = getCoordsNearLoc(center, 0, course_length, course_height)
		#Make gems stationary in the race for now.
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
				if distance(A.rect.center, B.rect.center) > A.collisionradius+B.collisionradius:
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


class Hud():
	'''This is the parent hud class.'''
        def __init__(self):
		#List of objects to update. This is where you should put
		#objects that won't collide with anything but still need updated.
		#self.toUpdate = []
		pass

	def setArrowTarget(self, targetid):
		'''Pre: targetid is a node id.'''
		print 'cannot set arrow target for this HUD'

	#def addObjectToUpdate(self, toUp):
	#	self.toUpdate.append(toUp)

	def update(self, _):
		pass
		#for tu in self.toUpdate:
		#	if tu.update():
		#		self.toUpdate.remove(tu)



class PlayerInfoDisplayer(Hud):
	'''I have a hunch that this is not the best way to do this,
	but it will work for now.
	Displays player information at the top of the screen.'''
        def __init__(self):
		Hud.__init__(self)

	def update(self, _):
		Hud.update(self, _)
		displayUtilities.displayShipLoc(globalvars.player)


class TimeTrialAssistant(Hud):
	'''Displays an arrow pointing towards the destination
	and counts down time remaining in race.'''
        def __init__(self, target):
		Hud.__init__(self)
		self.target = target #A location
		#Track time in seconds
		self.start_time = time.time()
		self.finish_reached = False

	def update(self, offset):
		Hud.update(self, offset)
		#Draw a bulls eye (multiple overlapping red and white 
		#circles centered at the destination point.
		target = (self.target[0] - offset[0], self.target[1] - offset[1])
		pygame.draw.circle(globalvars.screen, colors.red, target, 50, 0)
		pygame.draw.circle(globalvars.screen, colors.white, target, 40, 0)
		pygame.draw.circle(globalvars.screen, colors.red, target, 30, 0)
		pygame.draw.circle(globalvars.screen, colors.white, target, 20, 0)
		pygame.draw.circle(globalvars.screen, colors.red, target, 10, 0)

		if self.finish_reached: return True

		#Distance to target
		dtt = distance(globalvars.player.rect.center, self.target)

		#elapsed time
		elapsed = time.time() - self.start_time
		#Write the elapsed time to the top of the screen.
		string = 'Time: '+displayUtilities.formatTime(elapsed)+\
				'. Distance: '+displayUtilities.trunc(dtt,0)
		writeTextToScreen(string=string, fontSize=36,\
				color=colors.white, pos=(400,10))

		#Only display the guiding arrow if player is too far away to see the target
		if dtt > globalvars.SCREENRADIUS:
			displayUtilities.drawArrowAtTarget(self.target)
		#Check if the player has reached the destination.
		if dtt < 40:
			#If so, end the race.
			self.finish_reached = True
			writeTextToScreen(string='TIME TRIAL COMPLETED',\
				fontSize=64,pos=(globalvars.WIDTH/3, globalvars.HEIGHT/2))
			pygame.display.flip()
			time.sleep(2) #Sleep for 2 seconds.
		pass


class TimeLimit(Hud):
	'''Initially to be used for the gem wild scenario in 
	which the player has a limited amount of time to 
	grab as many gems as possible.'''
        def __init__(self, time_limit=0):
		Hud.__init__(self)
		self.points = 0
		self.time_limit = time_limit #in seconds
		#Track time in seconds
		self.start_time = time.time()
		self.finish_reached = False

	def update(self, offset):
		Hud.update(self, offset)
		if self.finish_reached: return True

		#Update elapsed time
		elapsed = time.time() - self.start_time
		#Write the elapsed time to the top of the screen.
		string = 'Time: '+displayUtilities.formatTime(elapsed)+\
			' Points:'+str(self.points)
		writeTextToScreen(string=string, fontSize=36,\
				       color=colors.white, pos=(400,10))

		#Check to see if time has run out.
		if elapsed >= self.time_limit:
			#If so, end the scenario.
			self.finish_reached = True
			writeTextToScreen(string='GEM WILD COMPLETED',\
				fontSize=64,pos=(globalvars.WIDTH/3, globalvars.HEIGHT/2))
			pygame.display.flip()
			time.sleep(2) #Sleep for 2 seconds.
			#Wipe out all the gems:
			for t in globalvars.tangibles:
				if t.is_a == globalvars.GEM: t.kill()
		pass



def populateSpaceHelper(seed=0, length=0, x=0, y=0):
	obstacles = getObstacles(seed=seed)
	return populateSpace(objects=obstacles, width=length, height=length, center=(x*length, y*length), seed=seed)


class InfiniteSpaceGenerator(Hud):
	'''An object which will deterministically but randomly generate
	objects in space based on the player's location.
	The player can fly around freely and objects will be automatically 
	and randomly but deterministically generated ahead of the player. These 
	objects will also be removed when they get too far from the player.
	This allows the player to explore in effectively infinite space.'''
        def __init__(self, seed=0, warps=None):
		Hud.__init__(self)
		self.warps = warps
		self.arrowTarget = None
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
		self.dict[loc] = populateSpaceHelper(\
				seed=loc, \
				length=self.space_length, \
				x=px, y=py)
		#print 'testing keys in the dictionary: '+str(self.dict.keys())
		#print 'end of InfiniteSpaceGenerator'

		#Keep an index into the dictionary's list of keys. At each update, check the next key and if it is too distant from the player, then delete it.
		self.key_index = 0

	def setArrowTarget(self, targetid):
		'''Pre: targetid is a node id.'''
		for w in self.warps:
			if w.destinationNode == targetid:
				self.arrowTarget = (w.rect.centerx, w.rect.centery)
				return 
		self.arrowTarget = None
		return

	def update(self, offset):
		Hud.update(self, offset)
		#Display player's location
		displayUtilities.displayShipLoc(globalvars.player)

		#Display arrow to target. Target is a warp portal.
		if not self.arrowTarget is None:
			dtt = distance(globalvars.player.rect.center, self.arrowTarget)
			#Only display the guiding arrow if player is too far away to see the target
			if dtt > globalvars.SCREENRADIUS:
				displayUtilities.drawArrowAtTarget(self.arrowTarget)

		#Get the player's location.
		px,py = globalvars.player.rect.center
		#Player's location divided by the length of each cell is the 
		#square the player is currently in.
		px = px / self.space_length
		py = py / self.space_length

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
				self.dict[loc] = populateSpaceHelper(\
					seed=loc, length=self.space_length, \
					x=x, y=y)


