from globalvars import FPS
import random as rd

num_engine_attributes = 5
#The following arrays map classes into actual values. The class is the index and the values are, well, the array values:

#Time in seconds that it takes to accelerate from zero to top speed
acceleration_classes = [2.0, 1.5, 1.0]
#The number of degrees that can be turned through per second.
turn_rate_classes = [90.0, 180.0, 270.0]
for i in range(len(turn_rate_classes)):
	turn_rate_classes[i] = turn_rate_classes[i] / float(FPS)
#Rate at which turn rate decays as speed moves away from maxTurnSpeed. This sets the turnRateDecay attribute. A value of 1.0 gives 1/4 the turn rate at top speed. A smaller value is better here.
turn_scaling_classes = [1.0, 0.5, 0.1]
#Speed in pixels per second
top_speed_classes = [200., 250., 300.]
for i in range(len(top_speed_classes)):
	top_speed_classes[i] = top_speed_classes[i] / float(FPS)
#Amount of fuel consumed per frame. Smaller is better.
efficiency_classes = [10,5,1]


#Names of the various engine classes
engine_class_names = ['Worthless', 'Scrap', 'Cheap', 'Okay', 'Hot', 'Noble', 'King', 'Emperor', 'Tyrant', 'Transcendent']


def generateEngine(engine_class):
	'''Returns an engine of the given class.'''
	#Start by randomly generating an engine.
	engine = Engine()
	#Calculate the class of the engine.
	actual_class = engine.getEngineClass()
	#print 'engine is class '+engine_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+engine_class_names[engine_class]+' ('+str(engine_class)+')'
	#print 'engine name: '+engine.getEngineName()
	#Now nudge the engine in the direction of the desired engine class.
	#randomly select an attribute of the engine
	randatt = rd.randint(0, num_engine_attributes-1)
	#while the engine is above the selected class...
	while actual_class > engine_class:
		#Decrement selected attribute
		engine.decrementAttribute(randatt)
		#move to the next engine attribute
		randatt = (randatt+1)%num_engine_attributes
		#Calculate the class of the engine.
		actual_class = engine.getEngineClass()
		#print 'Engine is now class '+engine_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+engine_class_names[engine_class]+' ('+str(engine_class)+')'
		#print 'Engine name: '+engine.getEngineName()
	#randomly select an attribute of the engine
	randatt = rd.randint(0, num_engine_attributes-1)
	#while the engine is below the selected class...
	while actual_class < engine_class:
		#Increment selected attribute
		engine.incrementAttribute(randatt)
		#move to the next engine attribute
		randatt = (randatt+1)%num_engine_attributes
		#Calculate the class of the engine.
		actual_class = engine.getEngineClass()
		#print 'Engine is now class '+engine_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+engine_class_names[engine_class]+' ('+str(engine_class)+')'
		#print 'Engine name: '+engine.getEngineName()
	#print 'Final Engine is class '+engine_class_names[actual_class]+' ('+str(actual_class)+') but should be class '+engine_class_names[engine_class]+' ('+str(engine_class)+')'
	#print 'Final Engine name: '+engine.getEngineName()+'\n'
	engine.initialize()
	return engine


acceleration_names = ['Unwilling', '', 'Eager']
def getEngineAdj1(acceleration_index):
	return acceleration_names[acceleration_index]


wide_turn_names = ['Relaxed', 'Inertial', 'Changeable']
normal_turn_names = ['Patient', '', 'Responsive']
tight_turn_names = ['High-G', 'Nimble', 'Dynamic']
def getEngineAdj2(turn_index, turn_scaling_index):
	if turn_index == 0:
		return wide_turn_names[turn_scaling_index]
	elif turn_index == 1:
		return normal_turn_names[turn_scaling_index]
	elif turn_index == 2:
		return tight_turn_names[turn_scaling_index]
	else:
		print 'ERROR in getEngineAdj2. Exiting'; exit()


slow_names = ['Guzzler', 'Automatic', 'Hiker']
medium_names = ['Consumer', 'Jolt', 'Trekker']
fast_names = ['Burner', 'Booster', 'Explorer']
def getEngineNoun(top_speed_index, efficiency_index):
	if top_speed_index == 0:
		return slow_names[efficiency_index]
	elif top_speed_index == 1:
		return medium_names[efficiency_index]
	elif top_speed_index == 2:
		return fast_names[efficiency_index]
	else:
		print 'ERROR in getEngineNoun. Exiting'; exit()


class Engine():
	def __init__(self):
		''' '''
		self.top_speed_index = 0
		self.efficiency_index = 0
		self.turn_index = 0
		self.turn_scaling_index = 0
		self.acceleration_index = 0

		self.name='default'
		self.maxSpeed=8. #in pixels per frame
		self.dv=0. #delta velocity (acceleration) in pixels per frame^2
		self.dtheta=5. #the turning rate of a ship in degrees per frame.
		#For simplicity, the player can set the target or goal speed in 
		#increments equal to this fraction of the maxSpeed.
		self.speedIncrements=1./4.
		#Fraction of maxSpeed at which turn rate is maximal
		self.maxTurnSpeed=self.speedIncrements
		#Rate at which turn rate decays as speed moves away from maxTurnSpeed
		self.turnRateDecay=1.
		#Think of this as the inverse of fuel economy. This is the amount of fuel 
		#consumed by this engine per frame.
		#In general, 10 will be the maximum and 1 the minimum.
		self.fuel_consumption = 10
		self.time_on_top_speed = 1.0

	def setAcceleration(self):
		#Gets up to speed in self.time_on_top_speed seconds
		self.dv = self.maxSpeed/float(FPS*self.time_on_top_speed)

	def initialize(self):
		#Take all the indicies and initialize the attributes based on them.
		self.name=self.getEngineName()
		self.maxSpeed = top_speed_classes[self.top_speed_index]
		self.time_on_top_speed = acceleration_classes[self.acceleration_index]
		self.dtheta = turn_rate_classes[self.turn_index]
		self.turnRateDecay = turn_scaling_classes[self.turn_scaling_index]
		self.fuel_consumption = efficiency_classes[self.efficiency_index]
		self.setAcceleration()

	def decrementAttribute(self, attribute_index):
		if attribute_index == 0:
			if self.top_speed_index > 0: self.top_speed_index -= 1
		elif attribute_index == 1:
			if self.acceleration_index > 0: self.acceleration_index -= 1
		elif attribute_index == 2:
			if self.turn_index > 0: self.turn_index -= 1
		elif attribute_index == 3:
			if self.turn_scaling_index > 0: self.turn_scaling_index -= 1
		elif attribute_index == 4:
			if self.efficiency_index > 0: self.efficiency_index -= 1
		else:
			print 'ERROR in engine.decrementAttribute. Exiting'; exit()

	def incrementAttribute(self, attribute_index):
		if attribute_index == 0:
			if self.top_speed_index < len(top_speed_classes)-1: self.top_speed_index += 1
		elif attribute_index == 1:
			if self.acceleration_index < len(acceleration_classes)-1: self.acceleration_index += 1
		elif attribute_index == 2:
			if self.turn_index < len(turn_rate_classes)-1: self.turn_index += 1
		elif attribute_index == 3:
			if self.turn_scaling_index < len(turn_scaling_classes)-1: self.turn_scaling_index += 1
		elif attribute_index == 4:
			if self.efficiency_index < len(efficiency_classes)-1: self.efficiency_index += 1
		else:
			print 'ERROR in engine.incrementAttribute. Exiting'; exit()

	def getEngineClass(self):
		return self.top_speed_index + self.acceleration_index + self.turn_index + self.turn_scaling_index + self.efficiency_index

	def getEngineName(self):
		return getEngineAdj1(self.acceleration_index)+' '+\
			getEngineAdj2(self.turn_index, self.turn_scaling_index)+' '+\
			getEngineNoun(self.top_speed_index, self.efficiency_index)


#def testing():
#	for i in range(len(engine_class_names)):
#		generateEngine(i)

#testing()
#exit()
