import colors
from objInstances import Missile
import globalvars
import random as rd

num_missile_attributes = 9
#The following arrays map classes into actual values. The class is the index and the values are, well, the array values:

#The number of degrees that can be turned through per second.
turn_rate_classes = [0.0, 90.0, 180.0, 270.0]
for i in range(len(turn_rate_classes)):
	turn_rate_classes[i] = turn_rate_classes[i] / float(globalvars.FPS)
#Time in seconds until the missile disappears
longevity_classes = [1.5, 2.0, 2.5, 3.0]
for i in range(len(longevity_classes)):
	longevity_classes[i] = int(longevity_classes[i]*globalvars.FPS)
#Speed in pixels per second
speed_classes = [200., 300., 400., 500.]
for i in range(len(speed_classes)):
	speed_classes[i] = speed_classes[i] / float(globalvars.FPS)
damage_classes = [5,10,20,30,40,50]
#This is one over the number of shots per second. So 0.1 means 10 shots per second. 0.2 = 5 shots per second.
refire_classes = [2.0, 1.5, 1.0, 0.5, 0.2]
for i in range(len(refire_classes)):
	refire_classes[i] = int(refire_classes[i]*globalvars.FPS)
ammo_classes = [1,5,10,25,50]
blast_classes = ['Area of effect', 'Fragmentation']
radius_classes = [20,40,60]
fragment_classes = [5,10,15]
seeking_classes = ['dumb','steer','lock','seek']
#Amount of health before the missile is destroyed by bullets
health_classes = [1,5,100]


#Names of the various missile classes
missile_class_names = ['Worthless', 'Junk', 'Scrap', 'Cheap', 'Okay', 'Tepid', 'Cool', 'Hot', 'Noble', 'Knightly', 'Worthy', 'Peerless', 'Kingly', 'Emperor', 'Tyrant', 'God-Emperor','Stellar','Transcendent']


def generateMissile(missile_class):
	'''Returns a missile of the given class.'''
	#Start by randomly generating a missile.
	missile = MissileLauncher(None)
	#Calculate the class of the missile.
	actual_class = missile.getMissileClass()
	#print 'missile is class '+missile_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+missile_class_names[missile_class]+' ('+str(missile_class)+')'
	#print 'missile name: '+missile.getMissileName()
	#Now nudge the missile in the direction of the desired missile class.
	#randomly select an attribute of the missile
	randatt = rd.randint(0, num_missile_attributes-1)
	#while the missile is above the selected class...
	while actual_class > missile_class:
		#Decrement selected attribute
		missile.decrementAttribute(randatt)
		#move to the next missile attribute
		randatt = (randatt+1)%num_missile_attributes
		#Calculate the class of the missile.
		actual_class = missile.getMissileClass()
		#print 'Missile is now class '+missile_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+missile_class_names[missile_class]+' ('+str(missile_class)+')'
		#print 'Missile name: '+missile.getMissileName()
	#randomly select an attribute of the missile
	randatt = rd.randint(0, num_missile_attributes-1)
	#while the missile is below the selected class...
	while actual_class < missile_class:
		#Increment selected attribute
		missile.incrementAttribute(randatt)
		#move to the next missile attribute
		randatt = (randatt+1)%num_missile_attributes
		#Calculate the class of the missile.
		actual_class = missile.getMissileClass()
		#print 'Missile is now class '+missile_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+missile_class_names[missile_class]+' ('+str(missile_class)+')'
		#print 'Missile name: '+missile.getMissileName()
	#print 'Final missile is class '+missile_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+missile_class_names[missile_class]+' ('+str(missile_class)+')'
	#print 'Final missile name: '+missile.getMissileName()+'\n'
	missile.initialize()
	return missile


#_names arrays
turn_rate_names = ['Dumbfire','','','Spiteful']
longevity_names = ['Winking','','','Undying']
speed_names = ['Fat Man','','','Dart']
damage_names = ['Needle', 'Javelin','','','Missile','Torpedo']
refire_names = ['Cold','Mirthful','','Wrathful','Furious'] #maybe reduce this down to just 2 names
ammo_names = ['Tooth','','','','Epiphany'] #Maybe don't incorporate this in the name.
blast_names = ['','Fragmentation']
blast_radius_names = ['Bitter','','Ravenous']
seeking_names = ['','Steerable','Lock-on','Seeking']
health_names = ['', '', 'Immortal']


class MissileLauncher():
	def __init__(self, shooter, name='default'):
		self.turn_rate_index = rd.randint(0, len(turn_rate_classes)-1)
		self.longevity_index = rd.randint(0, len(longevity_classes)-1)
		self.speed_index = rd.randint(0, len(speed_classes)-1)
		self.damage_index = rd.randint(0, len(damage_classes)-1)
		self.refire_index = rd.randint(0, len(refire_classes)-1)
		self.ammo_index = rd.randint(0, len(ammo_classes)-1)
		self.blast_index = rd.randint(0, len(blast_classes)-1)
		self.blast_radius_index = rd.randint(0, len(radius_classes)-1)
		self.seeking_index = rd.randint(0, len(seeking_classes)-1)
		self.health_index = rd.randint(0, len(health_classes)-1)

		self.name=name
		self.refire_rate=120 #Fires once every refire_rate frames
		self.speed = 0.0
		self.turn_rate = 0.0
		self.damage = 0
		self.longevity = 0
		self.cooldown=0 #How long until next shot
		self.shooter = shooter
		self.attack_angle = 10 #if within this angle to target, can shoot at target
		self.health = 1
		self.is_a = 'missile'


	def initialize(self):
		'''Take all the indicies and initialize the attributes based on them.'''
		self.name=self.getMissileName()
		self.turn_rate = turn_rate_classes[self.turn_rate_index]
		self.longevity = longevity_classes[self.longevity_index]
		self.speed = speed_classes[self.speed_index]
		self.damage = damage_classes[self.damage_index]
		self.refire_rate = refire_classes[self.refire_index]
		#ammo_classes[self.ammo_index] [1,5,10,25,50]
		#blast_classes[self.blast_index] #['Area of effect', 'Fragmentation']
		#radius_classes[self.blast_radius_index] #[20,40,60]
		#fragment_classes[self.blast_radius_index] #[5,10,15]
		#seeking_classes[self.seeking_index] #['dumb','steer','lock','seek'] 
		self.health = health_classes[self.health_index]


	def cool(self):
		if self.cooldown > 0:
			self.cooldown -= 1

	def shoot(self):
		tempmissile = Missile(self.shooter, self.speed, self.turn_rate, self.damage, self.longevity, self.health)
		#Add missile to the sprite groups
		globalvars.tangibles.add(tempmissile)
		self.cooldown=self.refire_rate

	def toStringArray(self):
		str_array = [self.name,
			'Class: '+self.getMissileClassName(),
			'Speed: '+str(self.speed),
			'Damage: '+str(self.damage),
			'Turn rate: '+str(self.turn_rate),
			'Refire rate: '+str(self.refire_rate),
			'Longevity: '+str(self.longevity)]
		return str_array


	def decrementAttribute(self, attribute_index):
		'''Return True if the limit was reached for this attribute, otherwise False'''
		if attribute_index == 0:
			if self.turn_rate_index > 0: self.turn_rate_index -= 1
			else: return True
		elif attribute_index == 1:
			if self.longevity_index > 0: self.longevity_index -= 1
			else: return True
		elif attribute_index == 2:
			if self.speed_index > 0: self.speed_index -= 1
			else: return True
		elif attribute_index == 3:
			if self.damage_index > 0: self.damage_index -= 1
			else: return True
		elif attribute_index == 4:
			if self.refire_index > 0: self.refire_index -= 1
			else: return True
		elif attribute_index == 5:
			if self.ammo_index > 0: self.ammo_index -= 1
			else: return True
		elif attribute_index == 6:
			if self.blast_index > 0: self.blast_index -= 1
			else: return True
		elif attribute_index == 7:
			if self.blast_radius_index > 0: self.blast_radius_index -= 1
			else: return True
		elif attribute_index == 8:
			if self.seeking_index > 0: self.seeking_index -= 1
			else: return True
		elif attribute_index == 9:
			if self.health_index > 0: self.health_index -= 1
			else: return True
		else:
			print 'ERROR in missile.decrementAttribute. Exiting'; exit()
		return False


	def incrementAttribute(self, attribute_index):
		'''Return True if the limit was reached for this attribute, otherwise False'''
		if attribute_index == 0:
			if self.turn_rate_index < len(turn_rate_classes)-1:
				self.turn_rate_index += 1
			else: return True
		elif attribute_index == 1:
			if self.longevity_index < len(longevity_classes)-1:
				self.longevity_index += 1
			else: return True
		elif attribute_index == 2:
			if self.speed_index < len(speed_classes)-1:
				self.speed_index += 1
			else: return True
		elif attribute_index == 3:
			if self.damage_index < len(damage_classes)-1:
				self.damage_index += 1
			else: return True
		elif attribute_index == 4:
			if self.refire_index < len(refire_classes)-1:
				self.refire_index += 1
			else: return True
		elif attribute_index == 5:
			if self.ammo_index < len(ammo_classes)-1:
				self.ammo_index += 1
			else: return True
		elif attribute_index == 6:
			if self.blast_index < len(blast_classes)-1:
				self.blast_index += 1
			else: return True
		elif attribute_index == 7:
			if self.blast_radius_index < len(radius_classes)-1:
				self.blast_radius_index += 1
			else: return True
		elif attribute_index == 8:
			if self.seeking_index < len(seeking_classes)-1:
				self.seeking_index += 1
			else: return True
		elif attribute_index == 9:
			if self.health_index < len(health_classes)-1:
				self.health_index += 1
			else: return True
		else:
			print 'ERROR in missile.incrementAttribute. Exiting'; exit()
		return False


	def getMissileName(self):
		'''Since this is too many attributes, only give keywords for the extreme high and low values and then have these trump other attributes when naming the missile.'''
		name = ''
		if len(seeking_names[self.seeking_index]) > 0:
			name += seeking_names[self.seeking_index]+' '

		if len(health_names[self.health_index]) > 0:
			name += health_names[self.health_index]+' '
		elif len(turn_rate_names[self.turn_rate_index]) > 0:
			name += turn_rate_names[self.turn_rate_index]+' '
		elif len(refire_names[self.refire_index]) > 0:
			name += refire_names[self.refire_index]+' '
		elif len(blast_radius_names[self.blast_radius_index]) > 0:
			name += blast_radius_names[self.blast_radius_index]+' '
		elif len(longevity_names[self.longevity_index]) > 0:
			name += longevity_names[self.longevity_index]+' '

		if len(blast_names[self.blast_index]) > 0:
			name += blast_names[self.blast_index]+' '

		if len(damage_names[self.damage_index]) > 0:
			name += damage_names[self.damage_index]+' '
		elif len(speed_names[self.speed_index]) > 0:
			name += speed_names[self.speed_index]+' '
		elif len(ammo_names[self.ammo_index]) > 0:
			name += ammo_names[self.ammo_index]+' '
		return name

	def getMissileClass(self):
		'''Current range of Missile ratings solely based on the numbers in this method is -10 to 24 inclusive.
		I changed the return value to map these into the range 0-17 inclusive.'''
		rating = 0
		if self.turn_rate_index == 0:
			rating -= 3
		elif self.turn_rate_index == 3:
			rating += 4
		else:
			rating += self.turn_rate_index #0-3

		rating += self.longevity_index #0-3
		
		if self.speed_index == 0:
			rating -= 1
		else:
			rating += self.speed_index #0-3

		rating += self.damage_index-1 #0-5

		rating += self.refire_index-2 #0-4

		if self.ammo_index == 0:
			rating -= 6
		elif self.ammo_index == 1:
			rating -= 4
		elif self.ammo_index == 2:
			rating -= 2
		elif self.ammo_index == 3:
			pass
		else:
			rating += 3

		rating += self.blast_radius_index #0-2

		if self.seeking_index == 3:
			rating += 2

		if self.health_index > 1: rating += 2

		return (rating+12)/2


	def getMissileClassName(self):
		return missile_class_names[self.getMissileClass()]


#def testing():
#	for i in range(len(missile_class_names)):
#		generateMissile(i)
#testing()
#exit()
