import pygame
import math
from displayUtilities import image_list
import geometry
import colors
import globalvars
import sys
sys.path.append('code/cython')
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
		#object is in a 90 degree wide cone, for instance, then it will test 
		#to see if the object is close enough to initiate an avoidance behavior.
		self.danger_cone = 90

		#If the distance between this object and another is less than this 
		#number of pixels, then this object will turn away.
		self.avoidance_threshold = 20

		#If the distance between this object and another is less than this 
		#number of pixels, then this object will not turn in the direction of 
		#the object even if this object's target is in that direction.
		self.suppress_turn_threshold = 40

		#Set the recommended ship speed to 1/4 max speed if another object is on 
		#a collision course with us and is danger_red_distance distance away, 
		#1/2 max speed if yellow and otherwise 3/4 max speed.
		self.danger_red_distance = 10
		self.danger_yellow_distance = 20


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

	def turnTowards(self, force_turn=False):
		"""This was copied out of scripts.py in stardog and 
		modified slightly. Collision avoidance is all my 
		own, however.
		force_turn causes the object to turn off collision avoidance.
		PRE: The following code MUST MUST MUST be set in order to make 
		self.angle_to_target current before calling this method:
		self.angle_to_target = self.getAngleToTarget()
		POST: Returns recommended speed for optimal turning. """
		#Collision avoidance: Avoid Collisions!
		#The following can only be used to suppress
		#turning if they are true. If false, they have no effect.
		dontTurnLeft = False
		dontTurnRight = False
		#If there is a closest sprite, amend turning to avoid it.
		if not force_turn and not self.closest_sprite is None:
			angle = self.getAngleToTarget(target=self.closest_sprite)
			#If the closest sprite is at any angle closer 
			#than danger_cone degrees, consider altering this 
			#physical object's turn to avoid the other sprite.
			abs_angle = abs(angle)
			if abs_angle < self.danger_cone:
				#self.dist_to_closest is the distance from this sprite's
				#center to self.closest_sprite's center. We need to factor 
				#in the radius for these sprites.
				actual_distance = self.dist_to_closest - \
					self.collisionradius-self.closest_sprite.collisionradius
				if actual_distance < self.avoidance_threshold:
					#Too close. It's vital that we turn away from the object.
					if angle < 0:
						self.turnClockwise()
					else:
						self.turnCounterClockwise()
					#Figure out optimal speed
					if actual_distance < self.danger_red_distance:
						return self.maxTurnSpeed
					elif actual_distance < self.danger_yellow_distance:
						return self.maxTurnSpeed*2
					else:
						return self.maxTurnSpeed*3
				#elif actual_distance + abs_angle < 70:
				elif actual_distance < self.suppress_turn_threshold:
					#It's not too close yet, but don't get any closer.
					if angle < 0:
						dontTurnLeft = True
					else:
						dontTurnRight = True
			#Reset closest sprite.
			self.closest_sprite = None
			self.dist_to_closest = globalvars.MINSAFEDIST

		#If we need to turn more towards the target or there is an 
		#object in front of us
		abs_angle = abs(self.angle_to_target)
		if abs_angle > self.acceptableError:
			#Get the amount to turn. It may be less than the 
			#amount this object is capable of turning.
			#Only turn this small amount if there is no object in
			#front of us.
			if abs_angle < self.calculateDTheta():
				if dontTurnLeft and self.angle_to_target < 0:
					pass
				elif dontTurnRight and self.angle_to_target > 0:
					pass
				else:
					self.turn(self.angle_to_target)
			#Turn counter clockwise if that's the direction of our 
			#target and there is no obstacle in that direction or
			#if there is an obstacle in front of us and to the right.
			elif self.angle_to_target < 0 and not dontTurnLeft:
				self.turnCounterClockwise()
			#In all other cases turn clockwise
			elif not dontTurnRight:
				self.turnClockwise()
		return self.maxSpeed


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
		#This previously caused an infinite loop, but
		#I think the following condition and speed setting fixes the problem. 
		#There were cases in which the speed
		#was infintesimally small, but non-zero.
		if self.inCollision(other) and self.speed < 1.0:
			self.speed = 1.0 
		while self.inCollision(other):
			self.move()

