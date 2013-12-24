from physicalObject import *
import colors
import objInstances
import weapon
import missile
import mine
import engine
import random as rd

healthBarDefaultWidth = 20


KILL_PLAYER_STATE = 0
GOTO_STATE = 1


num_ship_attributes = 6
#The following arrays map classes into actual values. The class is the index and the values are, well, the array values:

#Number of hitpoints the ship has
health_classes = [2, 8, 25, 50, 75, 100, 125, 150, 175]
#fuel capacity
#180000 = 5*60*60*10 = 5 minutes of fuel assuming 60 frames per second and 10 units of fuel consumed per frame. More efficient ships will consume less per frame.
fuelcap_classes = [180000/2, 180000, 180000*2, 180000*3]
#Cargo space
cargospace_classes = [10,20,30,40]
#Collision damage reduction. Reduces damage from things other than bullets.
collision_safe_classes = [1.0, 0.5, 0.0]
#Damage dealt to other ships upon collision
thorns_classes = [0, 25, 50]
#Damage dealt to asteroids upon collision
breaker_classes = [0, 20, 50]

#Names of the various ship classes
ship_class_names = ['Worthless', 'Junk', 'Scrap', 'Cheap', 'Okay', 'Tepid', 'Cool', 'Hot', 'Amazing', 'Wonderful', 'Noble', 'Knightly', 'Worthy', 'Peerless', 'Kingly', 'Emperor', 'Tyrant', 'God-Emperor','Stellar','Transcendent']


def generateShip(ship_class, x=0.0, y=0.0, image='default'):
	'''Returns a ship of the given class.'''
	#Start by randomly generating a ship.
	ship = Ship(centerx=x, centery=y, image_name=image)
	#Calculate the class of the ship.
	actual_class = ship.getShipClass()
	#print 'ship is class '+ship_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+ship_class_names[ship_class]+' ('+str(ship_class)+')'
	#print 'ship name: '+ship.getShipName()
	#Now nudge the ship in the direction of the desired ship class.
	#randomly select an attribute of the ship
	randatt = rd.randint(0, num_ship_attributes-1)
	#while the ship is above the selected class...
	while actual_class > ship_class:
		#Decrement selected attribute
		ship.decrementAttribute(randatt)
		#move to the next ship attribute
		randatt = (randatt+1)%num_ship_attributes
		#Calculate the class of the ship.
		actual_class = ship.getShipClass()
		#print 'Ship is now class '+ship_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+ship_class_names[ship_class]+' ('+str(ship_class)+')'
		#print 'Ship name: '+ship.getShipName()
	#randomly select an attribute of the ship
	randatt = rd.randint(0, num_ship_attributes-1)
	#while the ship is below the selected class...
	while actual_class < ship_class:
		#Increment selected attribute
		ship.incrementAttribute(randatt)
		#move to the next ship attribute
		randatt = (randatt+1)%num_ship_attributes
		#Calculate the class of the ship.
		actual_class = ship.getShipClass()
		#print 'Ship is now class '+ship_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+ship_class_names[ship_class]+' ('+str(ship_class)+')'
		#print 'Ship name: '+ship.getShipName()
	#print 'Final Ship is class '+ship_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+ship_class_names[ship_class]+' ('+str(ship_class)+')'
	#print 'Final Ship name: '+ship.getShipName()+'\n'
	ship.initialize()
	return ship


health_names = ['Skeleton', 'Bare', 'Light', '', '', '', 'Heavy', 'Armored', 'Martial']
collision_safe_names = ['','','Headbutting']
thorns_names = ['','','Thorny']
breaker_names = ['','','Sledge']
def getShipAdj(health_index, collision_safe_index, thorns_index, breaker_index):
	if thorns_index == 2:
		return thorns_names[thorns_index]
	elif breaker_index == 2:
		return breaker_names[breaker_index]
	elif collision_safe_index == 2:
		return collision_safe_names[collision_safe_index]
	else:
		return health_names[health_index]


low_cargo_names = ['Mayfly','Patrol Boat','Scout','Ranger']
medium_cargo_names = ['Sloop','Corvette','Frigate','S&R Vessel']
large_cargo_names = ['Packet','Freighter','Long-Haul','Smuggler']
very_large_cargo_names = ['Cargo Ship','Freighter','Deliverator','Enterprise']
def getShipNoun(fuelcap_index, cargospace_index):
	if cargospace_index == 0:
		return low_cargo_names[fuelcap_index]
	elif cargospace_index == 1:
		return medium_cargo_names[fuelcap_index]
	elif cargospace_index == 2:
		return large_cargo_names[fuelcap_index]
	elif cargospace_index == 3:
		return very_large_cargo_names[fuelcap_index]
	else:
		print 'ERROR in getShipNoun. Exiting'; exit()


class Ship(PhysicalObject):
	def __init__(self, centerx=0, centery=0, image_name='default'):
		PhysicalObject.__init__(self, centerx=centerx,\
			centery=centery, image_name=image_name)
		#Target is a physical object from which this ship can update its destination.
		self.target = None
		self.state = KILL_PLAYER_STATE
		self.team = globalvars.REDTEAM
		self.health_index = rd.randint(0, len(health_classes)-1)
		self.fuelcap_index = rd.randint(0, len(fuelcap_classes)-1)
		self.cargospace_index = rd.randint(0, len(cargospace_classes)-1)
		self.collision_safe_index = 0 #Initialize as shitty every time.
		self.thorns_index = 0 #Initialize as shitty every time.
		self.breaker_index = 0 #Initialize as shitty every time.

		self.name = ''
		self.engine=None
		self.health=25
		self.maxhealth=25
		self.collision_damage = 1.0 #initialize to 100% damage received.
		self.thorns_damage = 0
		self.breaker_damage = 0
		#number of gun addon hardpoints
		self.gunHardpoints = 1
		self.gun = None
		#number of missile addon hardpoints
		self.missileHardpoints = 1
		self.missile = None
		#number of mine addon hardpoints
		self.mineHardpoints = 1
		self.mine = None
		#number of misc addon hardpoints
		self.miscHardpoints = 1
		#int fuel (just make it a big number and divide it by 100 or 1000 and then display that number without the decimal.)
		self.fuel = 180000 #5*60*60*10 = 5 minutes of fuel assuming 60 frames per second and 10 units of fuel consumed per frame. More efficient engines will consume less per frame.
		#Money. This is updated when the ship runs into a gem.
		self.fuel_capacity = 0
		self.money = 0
		#cargo space
		self.cargospace_max = 30
		self.cargospace = self.cargospace_max
		#cargo array
		self.cargo = []

		self.myHealthBar = None
		self.healthBarOffset = self.rect.height

		self.is_a = globalvars.SHIP
		self.isPlayer = False

		#If the target is further away than this then recommended target engagement speed is max speed.
		self.target_long_range = 600
		#If the target is further away than this then recommended target engagement speed is 3/4 max speed.
		self.target_med_range = 400
		#If the target is further away than this then recommended target engagement speed is 1/2 max speed.
		self.target_short_range = 200
		#If the target is within self.target_front_rear degrees of the axis of our ship, then initiate a squat-and-shoot or flee behavior depending on whether target is in front or behind. Said another way, if the target is in the self.target_front_rear degree cone in front or behind us, then do the corresponding behavior.
		self.target_front_center = 30
		#Ship flees the battle field below min_percent_health
		self.min_percent_health = 0.10 #10 percent


	def initialize(self):
		self.name = self.getShipName()
		self.maxhealth = health_classes[self.health_index]
		self.health = self.maxhealth
		self.fuel_capacity = fuelcap_classes[self.fuelcap_index]
		self.cargospace_max = cargospace_classes[self.cargospace_index]
		self.cargospace = self.cargospace_max
		self.collision_damage = collision_safe_classes[self.collision_safe_index]
		self.thorns_damage = thorns_classes[self.thorns_index]
		self.breaker_damage = breaker_classes[self.breaker_index]


	def makeSelfCopyOfOther(self, other):
		'''Pre: other is a ship.
		Post: gives this ship a copy of the other ship's attributes, but
		does not alter cargo, weapons, or engines on this ship.'''
		self.health_index = other.health_index
		self.fuelcap_index = other.fuelcap_index
		self.cargospace_index = other.cargospace_index
		self.collision_safe_index = other.collision_safe_index
		self.thorns_index = other.thorns_index
		self.breaker_index = other.breaker_index
		self.initialize()
		self.loadNewImage(other.image_name)
		#Prevent artificial boosting of health or fuel by switching ships in and out of cargo hold.
		self.health = min(other.health, self.maxhealth)
		self.fuel = min(other.fuel, self.fuel)


	def unequipGun(self):
		self.addToCargo(self.gun)
		self.gun = None


	def unequipMissile(self):
		self.addToCargo(self.missile)
		self.missile = None


	def unequipMine(self):
		self.addToCargo(self.mine)
		self.mine = None


	def unequipEngine(self):
		self.addToCargo(self.engine)
		self.engine = None
		self.maxSpeed = 0.0
		self.dv = 0.0
		self.dtheta = 0.0
		self.speedIncrements = 0.0


	def addToCargo(self, item):
		if self.cargospace > 0:
			self.cargo.append(item)
			self.cargospace -= 1
			return True
		else:
			return False


	def removeFromCargo(self, index):
		self.cargospace += 1
		return self.cargo.pop(index)


	def equipWeaponFromCargo(self, cargo_index):
		#Error checking
		if cargo_index >= len(self.cargo):
			print 'ERROR: cargo_index '+str(cargo_index)+' is outside the cargo array.'
			exit()
		#This is a bad way to check if the indexed cargo is a weapon but it's what I've got for now.
		if not hasattr(self.cargo[cargo_index], 'shooter'):
			print 'ERROR: cargo indexed by '+str(cargo_index)+' is not a weapon.'
			exit()
		#Remove the weapon from cargo
		weapon = self.removeFromCargo(cargo_index)
		if weapon.is_a == 'gun':
			if not self.gun is None: self.unequipGun()
			self.gun = weapon
		elif weapon.is_a == 'missile':
			if not self.missile is None: self.unequipMissile()
			self.missile = weapon
		elif weapon.is_a == 'mine':
			if not self.mine is None: self.unequipMine()
			self.mine = weapon
		else:
			print 'ERROR: weapon type not recognized.'; exit()


	def equipEngineFromCargo(self, cargo_index):
		#Error checking
		if cargo_index >= len(self.cargo):
			print 'ERROR: cargo_index '+str(cargo_index)+' is outside the cargo array.'
			exit()
		if not self.cargo[cargo_index].is_a == 'engine':
			print 'ERROR: cargo indexed by '+str(cargo_index)+' is not an engine.'
			exit()
		#Remove the engine from cargo
		temp = self.removeFromCargo(cargo_index)
		if not self.engine is None: self.unequipEngine()
		self.engine = temp
		self.engineUpdate()


	def setHealthBar(self):
		self.myHealthBar = objInstances.HealthBar(width=healthBarDefaultWidth, height=10)
		self.myHealthBar.new_width = (self.health/float(self.maxhealth))*healthBarDefaultWidth
		globalvars.intangibles_top.add(self.myHealthBar)


	def engineUpdate(self):
		#Set this object's movement parameters based on the engine.
		self.maxSpeed = self.engine.maxSpeed
		self.dv = self.engine.dv
		self.dtheta = self.engine.dtheta
		self.speedIncrements = self.engine.speedIncrements
		#Fraction of maxSpeed at which turn rate is maximal
		self.maxTurnSpeed = self.engine.maxTurnSpeed
		#Rate at which turn rate decays as speed moves away from maxTurnSpeed
		self.turnRateDecay = self.engine.turnRateDecay


	def takeDamage(self, damage):
		self.health -= damage
		self.myHealthBar.new_width = (self.health/float(self.maxhealth))*healthBarDefaultWidth


	def gainHealth(self, amount):
		self.health = min(self.maxhealth, self.health+amount)
		self.myHealthBar.new_width = (self.health/float(self.maxhealth))*healthBarDefaultWidth


	def isDead(self):
		return self.health <= 0


	def shoot(self, force_shot=False, weapon=None):
		#Force shot tells this to shoot even if a target 
		#is not obviously in view. NPC's will not take such wild shots.
		if weapon is None:
			weapon = self.gun
		if not weapon is None:
			if weapon.cooldown == 0:
				#The player can shoot whenever he wants
				if force_shot:
					weapon.shoot()
				#NPCs need some intelligence when shooting
				else:
					angle = self.getAngleToTarget()
					#Decide whether or not we can shoot
					if geometry.inSights(self, self.destination,\
					weapon.weapon_range, weapon.attack_angle) and\
					self.clearLineOfSight():
						weapon.shoot()


	def cooldown(self):
		'''Cool all our weapons'''
		if not self.gun is None: self.gun.cool()
		if not self.missile is None: self.missile.cool()
		if not self.mine is None: self.mine.cool()


	def clearLineOfSight(self):
		'''Pre: Sight_range is an int or float.
		Post: Returns true if there are no whiskerables in the line of sight of this ship.
		Useful for avoiding friendly fire.'''
		#Get distance to target
		dtt = cygeometry.distance(self.rect.center, self.destination)
		#For each potential obstacle...
		for w in globalvars.whiskerables:
			#Get distance to the obstacle
			dist = cygeometry.distance(self.rect.center, w.rect.center)
			#   If the distance to the obstacle is less than the distance 
			#to the target then the obstacle might be obstructing our 
			#sight of the target.
			#   If the obstacle's distance is greater than zero then the 
			#obstacle is not ourself.
			#   If the angle to the obstacle is less than 80 degrees, then 
			#the obstacle is in front of this ship.
			if dist < dtt and dist > 0 and\
			abs(self.getAngleToTarget(target=w.rect.center)) < 90:
				#   If a line extending straight out from this ship
				#intersects a circle around the obstacle, then our 
				#sight is blocked.
				m,b = self.getStraightAhead()
				x,y = w.rect.center
				r = w.collisionradius
				#I boost the radius by a 1.5 fudge factor to 
				#help the NPCs avoid friendly fire.
				if geometry.lineIntersectsCircle(m, b, x, y, r*1.5):
					return False
		return True


	def getStraightAhead(self):
		'''Pre: 
		Post: returns slope and intercept of line extending straight 
		ahead from this ship'''
		slope = geometry.angleToSlope(self.theta)
		x,y = self.rect.center
		intercept = y - slope * x
		return slope, intercept


	def flee(self):
		#Get the direction in which to flee
		angle = geometry.angleFromPosition(globalvars.player_target_lead, self.rect.center)
		#Flee far away!
		magnitude = 1000000
		#Get the point to flee towards
		objective = geometry.translate(self.rect.center, angle, magnitude)
		self.setDestination(objective)


	def goTo(self, attacking=False, max_speed=False, force_turn=False):
		''' '''
		#Get angle to target
		self.angle_to_target = self.getAngleToTarget()
		#Get distance to target
		d = cygeometry.distance(self.rect.center, self.destination)
		#If target is far or max_speed is true, increase goal speed.
		recommended_targeting_speed = self.maxTurnSpeed
		if d > self.target_long_range:
			recommended_targeting_speed = self.maxSpeed
		elif d > self.target_med_range:
			recommended_targeting_speed = self.maxSpeed * 3./4.
		elif d > self.target_short_range:
			recommended_targeting_speed = self.maxSpeed * 1./2.
		#Only set speed to zero if target is infront of us and we are attacking.
		elif attacking and abs(self.angle_to_target) < self.target_front_center:
			recommended_targeting_speed = 0.0
			#Ignore collision avoidance to turn towards the target.
			force_turn = True
		#Turn towards target
		recommended_turn_speed = self.turnTowards(force_turn=force_turn)
		#Set goal speed to the minimum of the recommended speeds
		if max_speed:
			self.targetSpeed = self.maxSpeed
		else:
			self.targetSpeed = min(recommended_targeting_speed, recommended_turn_speed)
		#modify speed
		self.approachSpeed()
		#move
		self.move()


	def setTarget(self):
		if self.team == globalvars.REDTEAM:
			#Pick a blue team target
			limit = len(globalvars.BLUE_TEAM)
			if limit > 1:
				n = rd.randint(0, limit-1)
				self.target = globalvars.BLUE_TEAM.sprites()[n]
			elif limit == 1:
				self.target = globalvars.BLUE_TEAM.sprites()[0]
			else:
				return True
		else:
			#Pick a red team target
			limit = len(globalvars.RED_TEAM)
			if limit > 1:
				n = rd.randint(0, limit-1)
				self.target = globalvars.RED_TEAM.sprites()[n]
			elif limit == 1:
				self.target = globalvars.RED_TEAM.sprites()[0]
			else:
				return True
		return False


	def update(self):
		'''The following code is mostly duplicated in the missile's update function. Eventually I'd like to break this out as a more general seeking behavior.'''
		if self.state == KILL_PLAYER_STATE:
			#Initialize target
			if self.target is None or self.target.health <= 0:
				if self.setTarget(): return True
			#Set target location
			self.setDestination(self.target.lead_indicator)
			#Get angle to target
			self.angle_to_target = self.getAngleToTarget()
			#Get distance to target
			d = cygeometry.distance(self.rect.center, self.destination)

			#low health => retreat
			if float(self.health) / float(self.maxhealth) < self.min_percent_health:
				self.flee() #Set a far away destination
				self.goTo() #Go to the far away destination
			#enemy behind me => evade
			elif d < self.target_short_range and \
			abs(self.angle_to_target) > 180 - self.target_front_center:
				#If the target is behind us at short range,
				#flee quickly away. Ignore all else.
				self.goTo(max_speed=True, force_turn=True)
			#attacking enemy => attack
			else:
				self.goTo(attacking=True)
				#Check for firing solutions
				self.shoot()
				#Check for firing solutions for missiles
				if self.missile.cooldown == 0:
					self.shoot(force_shot=True, weapon=self.missile)
					#Double the cooldown to make missiles shoot less often.
					self.missile.cooldown = self.missile.cooldown*4
			#cooldown all the weapons
			self.cooldown()
		#going to location => go to
		elif self.state == GOTO_STATE:
			self.goTo()
		#Update my health bar
		self.updateHealthBar()
		self.setLeadIndicator()


	def updateHealthBar(self):
		self.myHealthBar.rect.center = self.rect.center
		self.myHealthBar.rect.top -= self.healthBarOffset


	def draw(self, offset):
		x,y = self.rect.center
		pos = x - offset[0], y - offset[1]
		self.drawAt(pos)


	def handleCollisionWith(self, other_sprite):
		'''For now ships take damage regardless of what they hit.'''
		died = False
		#Check for collisions with one's own bullets.
		#Don't respond to such collisions.
		if other_sprite.is_a == globalvars.BULLET:
			if other_sprite.dontClipMe == self: return died
			else: self.takeDamage(other_sprite.damage)
		elif other_sprite.is_a == globalvars.SHIP:
			#Check for bounce off
			#For now, area stands in for mass and only the
			#less massive object bounces off
			if other_sprite.getArea() >= self.getArea():
				self.bounceOff(other_sprite)
			#But all ships take damage regardless of size
			self.takeDamage(int(self.collision_damage*other_sprite.thorns_damage))
		elif other_sprite.is_a == globalvars.FIXEDBODY:
			self.bounceOff(other_sprite)
			return died
		elif other_sprite.is_a == globalvars.ASTEROID:
			#If I'm about to kill the asteroid then don't bounce off
			if other_sprite.health_amt > self.breaker_damage:
				self.bounceOff(other_sprite)
			self.takeDamage(int(self.collision_damage*2))
		#This if is not necessary since falling through has the same effect.
		#elif other_sprite.is_a == globalvars.HEALTH:
			#The health kit gives the player health. This is better because otherwise
			#we have to deal with multiple collisions between player and health
			#or a race condition over who gets updated first, the player sprite 
			#or the health sprite.
		#	return died
		if self.isDead():
			globalvars.intangibles_top.add(objInstances.Explosion(\
				x=self.rect.centerx,y=self.rect.centery))
			#kill removes the calling sprite from all sprite groups
			self.kill()
			self.myHealthBar.kill()
			died = True
			#Award points
			if not globalvars.score_keeper is None and self.team == globalvars.REDTEAM:
				globalvars.score_keeper.points += 1
			#Chance to spawn an item
			if rd.random() > 0.5:
				rand = rd.randint(0,2)
				if rand == 0: #Gun
					temp = objInstances.Pickup(self.gun, \
						x=self.rect.centerx, y=self.rect.centery)
				elif rand == 1: #Engine
					temp = objInstances.Pickup(self.engine, \
						x=self.rect.centerx, y=self.rect.centery)
				else: #Ship
					self.initialize()
					self.engine = None
					self.gun = None
					temp = objInstances.Pickup(self, \
						x=self.rect.centerx, y=self.rect.centery)
				globalvars.tangibles.add(temp)
		return died


	def getShipClassName(self):
		return ship_class_names[self.getShipClass()]

	def getShipClass(self):
		rating = self.health_index

		if self.fuelcap_index == 1:
			rating += 1
		elif self.fuelcap_index > 1:
			rating += 2

		if self.cargospace_index == 1:
			rating += 1
		elif self.cargospace_index > 1:
			rating += 2

		if self.collision_safe_index == 2:
			rating += 3

		if self.thorns_index == 1:
			rating += 1
		elif self.thorns_index > 1:
			rating += 2

		if self.breaker_index == 1:
			rating += 1
		elif self.breaker_index > 1:
			rating += 2

		return rating


	def getShipName(self):
		return getShipAdj(self.health_index, self.collision_safe_index,\
			self.thorns_index,self.breaker_index)\
			+' '+getShipNoun(self.fuelcap_index, self.cargospace_index)


	def decrementAttribute(self, attribute_index):
		if attribute_index == 0:
			if self.health_index > 0: self.health_index -= 1
		elif attribute_index == 1:
			if self.fuelcap_index > 0: self.fuelcap_index -= 1
		elif attribute_index == 2:
			if self.cargospace_index > 0: self.cargospace_index -= 1
		elif attribute_index == 3:
			if self.collision_safe_index > 0: self.collision_safe_index -= 1
		elif attribute_index == 4:
			if self.thorns_index > 0: self.thorns_index -= 1
		elif attribute_index == 5:
			if self.breaker_index > 0: self.breaker_index -= 1
		else:
			print 'ERROR in ship.decrementAttribute. Exiting'; exit()

	def incrementAttribute(self, attribute_index):
		if attribute_index == 0:
			if self.health_index < len(health_classes)-1: self.health_index += 1
		elif attribute_index == 1:
			if self.fuelcap_index < len(fuelcap_classes)-1: self.fuelcap_index += 1
		elif attribute_index == 2:
			if self.cargospace_index < len(cargospace_classes)-1: self.cargospace_index += 1
		elif attribute_index == 3:
			if self.collision_safe_index < len(collision_safe_classes)-1: self.collision_safe_index+=1
		elif attribute_index == 4:
			if self.thorns_index < len(thorns_classes)-1: self.thorns_index += 1
		elif attribute_index == 5:
			if self.breaker_index < len(breaker_classes)-1: self.breaker_index += 1
		else:
			print 'ERROR in ship.incrementAttribute. Exiting'; exit()


#def testing():
#	for i in range(len(ship_class_names)):
#		generateShip(i)
#testing()
#exit()
