
class Engine():
	def __init__(self):
		''' '''
		self.name='default'
		self.maxSpeed=8
		#Acceleration in pixels per second squared. 
		#Each second the speed increases towards the goal speed by this amount.
		self.dv=0 #delta velocity
		self.dtheta=5 #the turning rate of a ship in degrees per ... per frame?

def setProfile(profile, engine):
	if profile == 'mk1':
		engine.name = 'Thrusters Mk1'
		engine.maxSpeed = 5
		engine.dv = 2
		engine.dtheta = 3
	elif profile == 'mk2':
		engine.name = 'Thrusters Mk2'
		engine.maxSpeed = 10
		engine.dv = 2
		engine.dtheta = 5
	elif profile == 'mk3':
		engine.name = 'Thrusters Mk3'
		engine.maxSpeed = 20
		engine.dv = 2
		engine.dtheta = 8

