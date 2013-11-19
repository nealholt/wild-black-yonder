from globalvars import FPS

class Engine():
	def __init__(self):
		''' '''
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

def setProfile(profile, engine):
	engine.name = 'Thrusters Mk2'
	engine.maxSpeed = 300./float(FPS) #Speed in pixels per second
	engine.dv = engine.maxSpeed/float(FPS*1.0) #Gets up to speed in 1 second
	engine.dtheta = 180./float(FPS) #Turning angle per second

