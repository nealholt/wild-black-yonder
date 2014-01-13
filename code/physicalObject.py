import pygame
import math
from imageList import *
import geometry
import colors
import globalvars
import sys
sys.path.append('code/cython-'+str(sys.platform)) #Import from a system-specific cython folder
#Because cython files only work on the system they were compiled on.
import cygeometry


class PhysicalObject(pygame.sprite.Sprite):
	'''The four collision options are available to specify different collision zones than would 
	normally be specified by the size of this physical object's image.'''
	def __init__(self, centerx=0.0, centery=0.0, width=0, height=0, image_name=None, color=colors.white, collisiontopleft=None, collisionwidth=None,  collisionheight=None, collisionradius=None):
		#Sprite tutorial being used is here:
		# http://kai.vm.bytemark.co.uk/~piman/writing/sprite-tutorial.shtml
		#Sprite class:
		# http://pygame.org/docs/ref/sprite.html
		pygame.sprite.Sprite.__init__(self)
		#Keep track of whether or not this object's angle changed for efficiency
		self.angleChanged = False
		#Whether to offset this object's location based on the camera.
		#Text does not useOffset because we want to only position it relative to 0,0
		self.useOffset = True
		#There is nothing particularly special about any of the following default values.
		self.color = color
		#speed. All speeds will be in pixels per second.
		self.speed = 0.0
		self.targetSpeed = 0.0
		self.maxSpeed = 5.0
		#Acceleration in pixels per second squared. 
		#Each frame the speed goes up by this amount.
		self.dv = 1.0
		#Rotation. All rotations are in degrees
		self.theta = 0.0
		self.dtheta = 3.0
		#For simplicity, the player can set the target or goal speed in 
		#increments equal to this fraction of the maxSpeed.
		self.speedIncrements=1./4.
		#Speed at which turn rate is maximal
		self.maxTurnSpeed=self.maxSpeed*self.speedIncrements
		#Rate at which turn rate decays as speed moves away from maxTurnSpeed
		self.turnRateDecay=0.5
		#you can be within this many degrees of the target to stop turning
		self.acceptableError = 0.5
		#Calculate angle to target in turnTowards and store it so that ships don't have to recalculate it
		self.angle_to_target = 0.0

		self.destination = (0.0, 0.0)

		self.image_name = ''
		#The location of this object. It is two floats for accuracy, 
		#because rectangles will be rounded to an integer which can cause 
		#an inability to move diagonally at slow speeds because the integer 
		#always rounds down.
		#The downside of this is that there are now two valid location variables self.loc and self.rect.center, both of which need to be maintained and kept equal to each other.
		self.loc = (centerx, centery)
		self.image = None
		self.loadNewImage(image_name, width=width, height=height)
		self.rect.centerx = self.loc[0]
		self.rect.centery = self.loc[1]

		#For now calculate the radius as the average of the width and height.
		#Divide by 4 because we average the width and height and also divide them in half
		#to calculate radius rather than diameter.
		#Old way: This made the asteroids slightly too large.
		#self.collisionradius = max(int((self.rect.width+self.rect.height)/4), 1)
		self.collisionradius = collisionradius
		if self.collisionradius is None:
			self.collisionradius = max(int(min(self.rect.width,self.rect.height)/2), 1)

		#The following is the inset for the top left point for the collision box.
		self.collisiontopleft=collisiontopleft
		if self.collisiontopleft is None:
			self.collisiontopleft=(0,0)

		self.collisionwidth=collisionwidth
		if self.collisionwidth is None:
			self.collisionwidth=self.rect.width

		self.collisionheight=collisionheight
		if self.collisionheight is None:
			self.collisionheight=self.rect.height

		#If True, this physical object will perform rectangular collision detection.
		#If False, this physical object will perform circular collision detection.
		#The capital ship was the first object to use rectangular collision detection.
		self.useRectangular = False

		#What is this object.
		self.is_a = globalvars.OTHER

		#We use closest_sprite to help the NPC's avoid objects.
		self.closest_sprite = None
		self.dist_to_closest = globalvars.MINSAFEDIST

		#The following parameters could be tweaked to improve NPC performance, 
		#or they could be customized so that different NPCs could have 
		#different levels of caution.

		#Angle within which npc should consider avoiding an object. If the 
		#object is within + or - 90 degrees, for instance, then self will test 
		#to see if the object is close enough to initiate an avoidance behavior.
		#Only self.closest_sprite is evaluated for the danger cone.
		self.danger_cone = 90

		#If the distance between this object and self.closest_sprite is less than this 
		#number of pixels, then self will turn away.
		self.avoidance_threshold = 20

		#If the distance between this object and another is less than this 
		#number of pixels, then this object will not turn in the direction of 
		#the object even if this object's target is in that direction.
		self.suppress_turn_threshold = 40

		#Used for firing where a ship will be not where it's currently at.
		#This is not perfectly implemented.
		self.lead_indicator = self.rect.center

		#Ratio of distance to closest sprite over abs(angle to closest sprite) that 
		#corresponds to how self's speed should be set, assuming the ratio is less than one.
		#Max angle at which we even pay attention to such a sprite is 90 degrees.
		#100/20 degrees seems like a good threshold ratio.
		#So how about when distance/(abs(angle)*3) is less than one, then our target speed 
		#should be no more than this ratio of our maximum speed.
		#So in this case, 3 is the parameter. However, in reality, this depends on our 
		#acceleration and the object's size, but this will suffice for now.
		self.speed_safety_factor = 3.0 #Higher value == more conservative == slower near objects

		#What ratio of distance to target over abs(angle to target) the npc considers 
		#acceptable before the npc needs to reduce speed to improve turning.
		#Set the default ratio as anything over 25/1
		#if dist / angle is less than this value then the ship will slow to maxTurnSpeed, 
		#otherwise ship will approach at maxSpeed.
		#dist / angle is small for an npc when target is behind the npc and larger when the 
		#target is infront of the npc.
		#Making this value larger encourages NPCs to slow down to angle towards their target more often.
		self.distance_angle_ratio = 25.0


	def setLocation(self, centerx, centery):
		self.loc = (centerx, centery)
		self.rect.centerx = self.loc[0]
		self.rect.centery = self.loc[1]


	def loadNewImage(self, image_name, width=0, height=0):
		self.image_name = image_name
		if self.image_name is None:
			self.image = pygame.Surface([width, height])
			self.image.fill(self.color)
			self.base_image = self.image
		else:
			self.image = image_list[self.image_name].convert()
			#Base image is needed because we need a reference to the
			#original image that is never modified.
			#self.base_image is used in updateImageAngle.
			self.base_image = image_list[self.image_name].convert()
		self.rect = self.image.get_rect()


	def handleCollisionWith(self, other_sprite):
		'''React to a collision with other_sprite.'''
		pass


	def update(self):
		'''This is called by game.py. Mostly objects implementing 
		physicalObjects should have their own version of this 
		function.'''
		pass


	def updateImageAngle(self):
		self.image = pygame.transform.rotate(self.base_image, -self.theta).convert_alpha()
		#WITH the following code, the ship rotates smoothly relative to its health bar, but since the screen centers on the player, these constant small adjustments cause all the images drawn relative to the player to jiggle.
		#WITHOUT the following code, there is no jiggle, but the ships rotate a little more weirdly and the hit boxes might be slightly off.
		#For now, I choose to run without the following code.
		temp = self.rect.topleft
		self.rect = self.image.get_rect()
		self.rect.topleft = temp


	def noClipWith(self,other):
		'''Everything defaults to clipping.
		The idea was to have one's own bullets not clip with one's 
		self since the bullet starts out under the object that fired it
		which would otherwise cause everything to shoot itself.'''
		return False

	def setColor(self, color):
		self.color = color
		self.image.fill(color)

	def setClosest(self, closest_sprite, dist):
		self.closest_sprite = closest_sprite
		self.dist_to_closest = dist


	def calculateDTheta(self):
		'''This is used for xwing vs tie fighter-style
		maneuvering in which turn rate is reduced at 
		higher speeds. The following formula gives the maximum turn rate of
		self.dtheta only at 1/4 max velocity. The modifier on turn rate
		breaks down as follows when self.turnRateDecay = 1.0:
		f(x) = -abs(x-1/4)+1
		Speed	Turn
		0	3/4
		1/4	1
		1/2	3/4
		3/4	1/2
		1	1/4
		You can test the above out by pasting the following code to the 
		bottom of this file and running the game:
		po = PhysicalObject()
		po.testCalculateDTheta()
		exit()
		I changed self.turnRateDecay to be less severe because the ship was too hard to handle. '''
		return max((-self.turnRateDecay*\
				abs((self.speed - self.maxTurnSpeed) / self.maxSpeed)\
				 + 1.0)\
				* self.dtheta,\
			0.0)

	def testCalculateDTheta(self):
		'''See the comments for method calculateDTheta for more details about this.'''
		self.turnRateDecay = 1.0
		self.dtheta = 10
		for i in range(5):
			fraction = float(i)/4.0
			self.speed = self.maxSpeed * fraction
			print str(fraction)+' - '+str(self.calculateDTheta())

	def turnCounterClockwise(self, delta=None):
		'''Turn in the desired direction.
		I'm using an angle system like stardog uses such that 
		east=0, north=-90, west=180, south=90'''
		if delta is None: delta = self.calculateDTheta()
		self.theta -= delta
		if self.theta < -180: self.theta += 360
		self.angleChanged = True

	def turnClockwise(self, delta=None):
		'''Turn in the desired direction
		I'm using an angle system like stardog uses such that 
		east=0, north=-90, west=180, south=90'''
		if delta is None: delta = self.calculateDTheta()
		self.theta += delta
		if self.theta > 180: self.theta -= 360
		self.angleChanged = True

	def turn(self, delta):
		'''I'm using an angle system like stardog uses such that 
		east=0, north=-90, west=180, south=90'''
		self.theta += delta
		if self.theta > 180: self.theta -= 360
		elif self.theta < -180: self.theta += 360
		self.angleChanged = True

	def setAngle(self, angle):
		'''I'm using an angle system like stardog uses such that 
		east=0, north=-90, west=180, south=90'''
		self.theta = angle
		while self.theta > 180: self.theta -= 360
		while self.theta < -180: self.theta += 360
		self.angleChanged = True

	def park(self):
		'''Slow to a stop near target destination.'''
		itersToStop = self.speed / self.dv
		if not self.speed == 0 and \
		itersToStop >= cygeometry.distance(self.rect.center, self.destination) / self.speed:
			#Decelerate
			self.speed = max(0, self.speed - self.dv)
			self.targetSpeed = self.speed
			return True
		return False

	def approachSpeed(self):
		'''Modify this object's speed to approach the 
		goal speed (aka targetSpeed).'''
		if abs(self.speed - self.targetSpeed) < self.dv and \
		self.targetSpeed <= self.maxSpeed and \
		self.targetSpeed >= 0:
			self.speed = self.targetSpeed
		elif self.speed < self.targetSpeed:
			#Accelerate
			self.speed = min(self.maxSpeed, self.speed + self.dv)
		else:
			#Decelerate
			self.speed = max(0, self.speed - self.dv)

	def setDestination(self,point):
		'''Pre: point must be a tuple of integers or floats.'''
		self.destination = point

	def killDestination(self):
		self.destination = None

	def getAngleToTarget(self, target=None):
		'''This is a major departure from the old implementation. 
		THIS will pretend that up is positive Y values and down is 
		negative Y values as is standard in math, but not computer 
		science.'''
		if target is None:
			x,y = self.destination
		elif isinstance(target, tuple):
			x,y = target
		else:
			x,y = target.rect.center
		rise = y - self.rect.centery
		run = x - self.rect.centerx
		#As I understand it, this ought to return one angle to the target,
		#though not necessarily the shortest angle.
		#Range of arctan is negative pi to pi and the world is upside down
		#because down is positive in the y direction.
		#See testAngleToTarget.py in backups for some examples.
		angle_to_target = math.degrees(math.atan2(rise, run)) - self.theta
		if angle_to_target < -180: angle_to_target += 360
		if angle_to_target > 180: angle_to_target -= 360
		return angle_to_target


	def collisionAvoidance(self):
		'''returns recommended turning angle and speed, or None, in which case no change is mandated by collision avoidance. Also returns whether or not turning in a particular direction is suppressed.'''
		#Collision avoidance: Avoid Collisions!
		#The following can only be used to suppress
		#turning if they are true. If false, they have no effect.
		speed = None
		dtheta = None
		dontTurnLeft = False
		dontTurnRight = False
		#If there is a closest sprite, amend turning to avoid it.
		if self.closest_sprite is None:
			#Set no conditions on turning and no recommended speed
			#or turning angle
			return [speed, dtheta, dontTurnLeft, dontTurnRight]
		else:
			angle = self.getAngleToTarget(target=self.closest_sprite)
			#If the closest sprite is at any angle closer 
			#than danger_cone degrees, consider altering this 
			#physical object's turn to avoid the other sprite.
			abs_angle = abs(angle)
			if abs_angle < self.danger_cone:
				if self.dist_to_closest < self.avoidance_threshold:
					#Too close. It's vital that we turn away from the object.
					dtheta = self.calculateDTheta()
					if angle > 0:
						dtheta = -dtheta
					#Figure out optimal speed
					fraction = (self.dist_to_closest / (abs_angle*self.speed_safety_factor))
					speed = self.maxSpeed * fraction
						
				#elif actual_distance + abs_angle < 70:
				elif self.dist_to_closest < self.suppress_turn_threshold:
					#It's not too close yet, but don't get any closer.
					if angle < 0:
						dontTurnLeft = True
					else:
						dontTurnRight = True
			#Reset closest sprite.
			self.closest_sprite = None
			self.dist_to_closest = globalvars.MINSAFEDIST
		return [speed, dtheta, dontTurnLeft, dontTurnRight]


	def getRecommendedVector(self):
		"""This was copied out of scripts.py in stardog and 
		modified slightly.
		PRE: The following code MUST MUST MUST be set in order to make 
		self.angle_to_target current before calling this method:
		self.angle_to_target = self.getAngleToTarget()
		POST: Returns recommended speed and direction for approaching target. """
		dtheta = 0.0
		speed = self.maxSpeed
		#If we need to turn more towards the target...
		abs_angle = abs(self.angle_to_target)
		if abs_angle > self.acceptableError:
			#Get the amount to turn. It may be less than the 
			#amount this object is capable of turning.
			capable_dtheta = self.calculateDTheta()
			#Turn counter clockwise if that's the direction of our target
			if self.angle_to_target < 0:
				dtheta = max(self.angle_to_target, -capable_dtheta)
			#In all other cases turn clockwise
			else:
				dtheta = min(self.angle_to_target, capable_dtheta)
		#Now determine the best speed
		#Get distance to target. Cap the distance at one screen width.
		d = min(globalvars.WIDTH, cygeometry.distance(self.rect.center, self.destination))
		if d / max(abs_angle, 1.0) < self.distance_angle_ratio:
			speed = self.maxTurnSpeed
		return (speed, dtheta)


	def performMove(self, update_angle=True, max_speed=False, force_turn=False):
		"""Get recommended vector for collision avoidance.
		If nothing needs particularly avoided, get recommended vector
		to reach target.
		Finally turn and move in the recommended manner."""
		if update_angle:
			#Get angle to target
			self.angle_to_target = self.getAngleToTarget()
		#Get vector recommended by collisionAvoidance
		speed, dtheta, dontTurnLeft, dontTurnRight = self.collisionAvoidance()
		#print 'speed: '+str(speed)+'\ndtheta:'+str(dtheta)+'\nleft:'+str(dontTurnLeft)+'\nright:'+str(dontTurnRight) #TESTING
		#If collisionAvoidance does not fully specify a vector then ask
		#getRecommendedVector for a vector.
		if speed is None or dtheta is None:
			speed, dtheta = self.getRecommendedVector()
		#Finally turn the specified amount and direction and return the speed.
		if force_turn or not((dtheta < 0 and dontTurnLeft) or (dtheta > 0 and dontTurnRight)):
			self.turn(dtheta)
		if max_speed:
			self.targetSpeed = self.maxSpeed
		else:
			self.targetSpeed = speed
		#modify speed
		self.approachSpeed()
		#move
		self.move()


	def move(self):
		'''self.loc is a tuple of floats, but rect.topleft is always
		converted to an integer because it has to be fitted to particular 
		pixels. At low speeds, the rounding down of the integer tuple
		can prevent diagonal motion. That's why we use self.loc instead.'''
		self.loc = geometry.translate(self.loc, \
			self.theta, self.speed)
		self.rect.center = self.loc


	def translate(self, angle, magnitude):
		self.loc = geometry.translate(self.loc, \
			angle, magnitude)
		self.rect.centerx = self.loc[0]
		self.rect.centery = self.loc[1]


	def draw(self, offset=(0,0)):
		if self.angleChanged:
			self.updateImageAngle()
			self.angleChanged = False
		x,y = self.rect.topleft
		pos = x - offset[0], y - offset[1]
		globalvars.screen.blit(self.image, pos)

	def drawAt(self, position=(0,0)):
		if self.angleChanged:
			self.updateImageAngle()
			self.angleChanged = False
		pos = position[0] - self.rect.width/2, position[1] - self.rect.height/2
		globalvars.screen.blit(self.image, pos)


	def isOnScreen(self, offset):
		'''Returns true if this sprite is on screen.
		rect.right < left #Then not on screen
		rect.bottom < top #Then not on screen
		rect.top > top + globalvars.HEIGHT #Then not on screen
		rect.left > left + globalvars.WIDTH #Then not on screen'''
		left, top = offset
		return not( self.rect.right < left or \
		self.rect.bottom < top or \
		self.rect.top > top + globalvars.HEIGHT or \
		self.rect.left > left + globalvars.WIDTH )


	def getArea(self):
		return self.rect.width*self.rect.height


	def inCollision(self, other):
		'''Pre: Other is a physical object
		Post: returns true if self and other are colliding.'''
		#treat both objects as rectangles if either object wants to be
		#treated as a rectangle.
		#collision detect based on rectangles:
		if self.useRectangular or other.useRectangular:
			#If not that self's right most point is left of other's left most point
			#or other's right most point is left of self's left most point
			#then the two objects collided.
			selfRight = self.rect.topleft[0]+self.collisionwidth+self.collisiontopleft[0]
			otherLeft = other.rect.topleft[0]+other.collisiontopleft[0]
			otherRight = other.rect.topleft[0]+other.collisionwidth+other.collisiontopleft[0]
			selfLeft = self.rect.topleft[0]+self.collisiontopleft[0]
			selfBottom = self.rect.topleft[1]+self.collisionheight+self.collisiontopleft[1]
			otherTop = other.rect.topleft[1]+other.collisiontopleft[1]
			otherBottom = other.rect.topleft[1]+other.collisionheight+other.collisiontopleft[1]
			selfTop = self.rect.topleft[1]+self.collisiontopleft[1]

			return not(selfRight < otherLeft or otherRight < selfLeft)\
			and not(selfBottom < otherTop or otherBottom < selfTop)
		#collision detect based on circles:
		#If the distance between our centers is less than our 
		#summed radii, then we have collided.
		else:
			return cygeometry.distance(self.rect.center, other.rect.center) < self.collisionradius+other.collisionradius



	def bounceOff(self, other):
		'''Other is another physical object that this physical object 
		just struck and should bounce off of.

		two objects, A and B, collide. let theta be the angle of the line from the 
		center of A to the center of B. Let A be the smaller of the two. let 
		theta' be a line perpendicular to theta.
		If A's direction is less than 90 degrees from pointing at B then 
		reflect A's direction over theta'. Reduce both objects' speeds. 
		else move A's direction half way to theta in the direction away from B. 
		Increase A's speed. Decrease B's speed. (This is the case where A 
		is hit from behind despite moving in the same direction as B.) '''
		#If either object uses rectangular, we need to bounce off differently
		if self.useRectangular or other.useRectangular:
			#Determine if the collision is in the x direction or the y direction.
			selfRight = self.rect.topleft[0]+self.collisionwidth+self.collisiontopleft[0]
			otherRight = other.rect.topleft[0]+other.collisionwidth+other.collisiontopleft[0]
			selfLeft = self.rect.topleft[0]+self.collisiontopleft[0]
			otherLeft = other.rect.topleft[0]+other.collisiontopleft[0]
			if selfRight > otherRight or otherLeft > selfLeft:
				#horizontal collision
				if self.theta > 0:
					self.setAngle(180.0 - self.theta)
				else:
					self.setAngle(-180.0 - self.theta)
			else:
				#vertical collision
				self.setAngle(-self.theta)
		#The following is for collisions with objects that are not rectangular.
		else:
			angleToOther = self.getAngleToTarget(target=other)
			if abs(angleToOther) < 90: #Relatively head on collision
				bounce_off_angle = 90 - angleToOther
				if angleToOther < 0:
					self.turnClockwise(bounce_off_angle)
				else:
					self.turnCounterClockwise(bounce_off_angle)
				#Decrease speed by an amount related to the
				#headon-ed-ness of the collision
				self.speed = self.speed / (1.0 + float(bounce_off_angle) / 90.0)
				self.targetSpeed = self.speed
			else: #Rear end collision
				#Increase speed, as when an object is hit from behind.
				#The angle will also change slightly to be more in the
				#direction of the object that struck us.
				#Specifically, change our angle to be halfway between 
				#our angle and the angle of other.
				#First pass for code follows. This is good enough for now.
				amountToTurn = (180 - abs(angleToOther))/2
				if angleToOther < 0:
					self.turnCounterClockwise(amountToTurn)
				else:
					self.turnClockwise(amountToTurn)
				#Increase speed by adding other object's speed
				self.speed = self.speed+other.speed
				#Decrease other object's speed
				other.speed -= self.speed
				other.targetSpeed = other.speed
		#Prevent multiple consecutive collisions with the same object
		#Get the angle to move away from other's center.
		angle_to_move = geometry.angleFromPosition(\
				other.rect.center, self.rect.center)
		while self.inCollision(other):
			self.loc = geometry.translate(self.loc, angle_to_move, 1.0)
			self.rect.center = self.loc


	def setLeadIndicator(self):
		'''Sets the point in space that enemies should shoot 
		at to hit the player when the player is moving.'''
		#return self.rect.center
		self.lead_indicator = geometry.translate(self.rect.center, self.theta, self.speed*50.0) #The amount to translate depends on player speed, distance from enemy, and bullet speed. There might be a better way to do this.
		#Why when self.rect.center is used does this still not work for the capital ship? Specifically there is a problem when I perch over the upper left corner of the capital ship. It creates a kind-of cool blind spot though. Maybe this is not a problem.


	def getDirtyRect(self, offset):
		'''Pre: self is on screen.
		Post: Returns the dirty rect for this object.'''
		pos = self.rect.topleft
		#Whether to offset this object's location based on the camera.
		#Text does not useOffset because we want to only position it relative to 0,0
		if self.useOffset:
			pos = pos[0]-offset[0], pos[1]-offset[1]
		# - Return the sprite's current location rectangle.
		return (pos[0], pos[1], self.rect.width, self.rect.height)
