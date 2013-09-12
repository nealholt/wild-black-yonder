import pygame
import math
import game


def translate(location, angle, magnitude):
	'''This is very similar to the PhysicalObject.move function.'''
	vectx = math.cos(math.radians(angle))
	vecty = math.sin(math.radians(angle))
	x,y = location
	return x+vectx*magnitude, y+vecty*magnitude


class PhysicalObject(pygame.sprite.Sprite):
	def __init__(self, top=0, left=0, width=0, height=0, image_name=None):

		#Sprite tutorial being used is here:
		# http://kai.vm.bytemark.co.uk/~piman/writing/sprite-tutorial.shtml
		#Sprite class:
		# http://pygame.org/docs/ref/sprite.html
		pygame.sprite.Sprite.__init__(self)
		#There is nothing particularly special about any of the following default values.

		#speed. All speeds will be in pixels per second.
		self.speed = 0.0
		self.targetSpeed = 0.0
		self.maxSpeed = 5.0
		#Acceleration in pixels per second squared. 
		#Each second the speed goes up by this amount.
		self.dv = 1.0

		#Rotation. All rotations are in degrees
		self.theta = 0.0
		self.dtheta = 3.0

		#you can be within this many degrees of the target to stop turning
		self.acceptableError = 0.5

		self.destination = (0.0, 0.0)

		self.image_name = image_name

		if self.image_name is None:
			self.image = pygame.Surface([width, height])
			self.image.fill((100,255,100)) #Randomly chosen default color
			self.base_image = self.image
		else:
			self.image = game.loadImage(self.image_name + game.ext)
			#Base image is needed because we need a reference to the
			#original image that is never modified.
			#self.base_image is used in updateImageAngle.
			self.base_image = game.loadImage(self.image_name + game.ext)
			self.rect = self.base_image.get_rect()

		self.rect = self.image.get_rect()
		self.rect.topleft = (left, top)

		#For now calculate the radius as the average of the width and height.
		#Divide by 4 because we average the width and height and also divide them in half
		#to calculate radius rather than diameter.
		#Old way: This made the asteroids slightly too large.
		#self.radius = max(int((self.rect.width+self.rect.height)/4), 1)
		self.radius = max(int(min(self.rect.width,self.rect.height)/2), 1)

		#What is this object.
		self.is_a = game.OTHER

		#We use closest_sprite to help the NPC's avoid objects.
		self.closest_sprite = None
		self.dist_to_closest = game.MINSAFEDIST


	def handleCollisionWith(self, other_sprite):
		'''React to a collision with other_sprite.'''
		pass


	def update(self):
		'''This is called by game.py. Mostly objects implementing 
		physicalObjects should have their own version of this 
		function, but ship objects won't.'''
		pass


	def updateImageAngle(self):
		self.image = pygame.transform.rotate(self.base_image, -self.theta).convert_alpha()
		#Awesome! The following works. It fixes the most egregious 
		#of the hit box issues and is probably as good as it gets.
		temp = self.rect.topleft
		self.rect = self.image.get_rect()
		self.rect.topleft = temp

	def getCenter(self):
		return self.rect.center

	def getX(self):
		return self.rect.centerx

	def getY(self):
		return self.rect.centery

	def noClipWith(self,other):
		'''Everything defaults to clipping.
		The idea was to have one's own bullets not clip with one's 
		self since the bullet starts out under the object that fired it
		which would otherwise cause everything to shoot itself.'''
		return False

	def setColor(self, color):
	        self.image.fill(color)

	def setClosest(self, closest_sprite, distance):
		self.closest_sprite = closest_sprite
		self.dist_to_closest = distance

	def turnCounterClockwise(self, delta=None):
		'''Turn in the desired direction.
		I'm using an angle system like stardog uses such that 
		east=0, north=-90, west=180, south=90'''
		if delta is None: delta = self.dtheta
		self.theta -= delta
		if self.theta < -180: self.theta += 360
		self.updateImageAngle()

	def turnClockwise(self, delta=None):
		'''Turn in the desired direction
		I'm using an angle system like stardog uses such that 
		east=0, north=-90, west=180, south=90'''
		if delta is None: delta = self.dtheta
		self.theta += delta
		if self.theta > 180: self.theta -= 360
		self.updateImageAngle()

	def turn(self, delta):
		'''I'm using an angle system like stardog uses such that 
		east=0, north=-90, west=180, south=90'''
		self.theta += delta
		if self.theta > 180: self.theta -= 360
		elif self.theta < -180: self.theta += 360
		self.updateImageAngle()

	def park(self):
		'''Slow to a stop near target destination.'''
		itersToStop = self.speed / self.dv
		if not self.speed == 0 and \
		itersToStop >= self.distanceToDestination() / self.speed:
			self.decelerate()
			self.targetSpeed = self.speed
			return True
		return False

	def approachSpeed(self):
		'''Modify this object's speed to approach the 
		goal speed (aka targetSpeed).'''
		if abs(self.speed - self.targetSpeed) < self.dv:
			self.speed = self.targetSpeed
		elif self.speed < self.targetSpeed:
				self.accelerate()
		else:
			self.decelerate()

	def accelerate(self):
		self.speed = min(self.maxSpeed, self.speed + self.dv)

	def decelerate(self):
		self.speed = max(0, self.speed - self.dv)

	def distanceToDestination(self, dest=None):
		if dest is None:
			x,y = self.destination
		else:
			x,y = dest
		return math.sqrt( (self.rect.centerx-x)**2 + (self.rect.centery-y)**2 )

	def setDestination(self,point):
		'''Pre: point must be a tuple of integers or floats.'''
		self.destination = point

	def killDestination(self):
		self.destination = None

	def getShorterTurnDirection(self, target_angle):
		'''Given a target angle, calculate the shorter direction to turn 
		and how many degrees to turn in that direction.
		Figuring out how to calculate this was a little tricky for me.
		Drawing helped. The idea is that there are two different
		distances between points when those points are on a ring.
		True = clockwise
		False = counterclockwise
		'''
		a = self.theta
		b = target_angle
		self_is_a = True
		if b < a: #Ensure that a is the smaller of the two values.
			a = target_angle
			b = self.theta
			self_is_a = False
		dist1 = b-a
		dist2 = (a+180)+(180-b) #a+180 is actually a - -180
		if dist1 < dist2:
			if self_is_a:
				return True
			else:
				return False
		else:
			if self_is_a:
				return False
			else:
				return True

	def getAngleToTarget(self, target=None):
		'''This is a major departure from the old implementation. 
		THIS will pretend that up is positive Y values and down is 
		negative Y values as is standard in math, but not computer 
		science.
		SHIT. It's still not working. I haven't wrapped my head around why.'''
		#x,y = None,None
		if target is None:
			x,y = self.destination
		else:
			x,y = target.getCenter()
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

	def turnTowards(self):
		"""This was copied out of scripts.py in stardog and 
		modified slightly. Collision avoidance is all my 
		own, however."""
		#Collision avoidance: Avoid Collisions!
		#The following can only be used to suppress
		#turning if they are true. If false, they have no effect.
		dontTurnLeft = False
		dontTurnRight = False
		#If there is a closest sprite, amend turning to avoid it.
		if not self.closest_sprite is None:
			angle = self.getAngleToTarget(target=self.closest_sprite)
			#If the ship is at any angle closer than a right angle, consider altering its turn
			abs_angle = abs(angle)
			if abs_angle < 90:
				#self.dist_to_closest is the distance from this sprite's
				#center to self.closest_sprite's center. We need to factor 
				#in the radius for these sprites.
				actual_distance = self.dist_to_closest - \
					self.radius-self.closest_sprite.radius
				#TODO. These constants might need adjusted.
				#Previously the following was just this commented out portion. I thought making it trickier might reduce the jiggle. It did not.
				#if actual_distance + abs_angle < 30:
				if actual_distance < 20:

					#Too close. It's vital that we turn away from the object.
					if angle < 0:
						self.turnClockwise()
						return True
					else:
						self.turnCounterClockwise()
						return True
				#elif actual_distance + abs_angle < 70:
				elif actual_distance < 40:
					#It's not too close yet, but don't get any closer.
					if angle < 0:
						dontTurnLeft = True
					else:
						dontTurnRight = True
			#Reset closest sprite.
			self.closest_sprite = None
			self.dist_to_closest = game.MINSAFEDIST


		angleToTarget = self.getAngleToTarget()
		#If we need to turn more towards the target or there is an 
		#object in front of us
		if abs(angleToTarget) > self.acceptableError:
			#Get the amount to turn. It may be less than the 
			#amount this object is capable of turning.
			#Only turn this small amount if there is no object in
			#front of us.
			if abs(angleToTarget) < self.dtheta:
				if dontTurnLeft and angleToTarget < 0:
					pass
				elif dontTurnRight and angleToTarget > 0:
					pass
				else:
					self.turn(angleToTarget)
			#Turn counter clockwise if that's the direction of our 
			#target and there is no obstacle in that direction or
			#if there is an obstacle in front of us and to the right.
			elif angleToTarget < 0 and not dontTurnLeft:
				self.turnCounterClockwise()
			#In all other cases turn clockwise
			elif not dontTurnRight:
				self.turnClockwise()


	def move(self):
		'''This is very similar to the translate function.'''
		#Get new vector
		vectx = math.cos(math.radians(self.theta))
		vecty = math.sin(math.radians(self.theta))

		self.rect = self.rect.move(vectx*self.speed, vecty*self.speed)


	def draw(self, offset=(0,0)):
		x,y = self.rect.topleft
		pos = x - offset[0], y - offset[1]
		game.screen.blit(self.image, pos)

	def drawAt(self, position=(0,0)):
		pos = position[0] - self.rect.width/2, position[1] - self.rect.height/2
		game.screen.blit(self.image, pos)


	def getArea(self):
		return self.rect.width*self.rect.height


	def bounceOff(self, other):
		'''Other is another physical object that this physical object 
		just struck and should bounce off of.

		two objects, A and B, collide. let theta be the angle of the line from the 
		center of A to the center of B. Let A be the smaller of the two. let 
		theta' be a line perpendicular to theta. If A's direction is less 
		than 90 degrees from pointing at B then reflect A's direction over 
		theta'. Reduce both objects' speeds. 
		else move A's direction half way to theta in the direction away from B. 
		Increase A's speed. Decrease B's speed. (This is the case where A 
		is hit from behind despite moving in the same direction as B.)
		'''
		angleToOther = self.getAngleToTarget(target=other)
		if abs(angleToOther) < 90:
			#This object should bounce off other in a dramatically
			#new direction. Specifically, our angle should be 
			#reflected over the line perpendicular to the line that
			#passes through the center of this and other.
			#First pass for code follows. This is good enough for now.
			if angleToOther < 0:
				self.turnClockwise(90)
			else:
				self.turnCounterClockwise(90)
		else:
			#this should sort of be bounced to a higher speed, as 
			#when an object is hit from behind.
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
			#Use max because speed*2 might be zero.
			self.speed = max(self.speed*2, 10)
		#Move twice immediately to prevent multiple collisions.
		self.move()
		self.move()

