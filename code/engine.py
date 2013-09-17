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

def setProfile(profile, engine):
	if profile == 'mk0':
		engine.name = 'Thrusters Mk0'
		engine.maxSpeed = 0.
		engine.dv = 0.
		engine.dtheta = 0.
	elif profile == 'mk1':
		engine.name = 'Thrusters Mk1'
		engine.maxSpeed = 150./float(FPS) #Speed in pixels per second
		engine.dv = 5./float(FPS*3.0) #Gets up to speed in 3 seconds
		engine.dtheta = 90./float(FPS) #Turning angle per second
	elif profile == 'mk2':
		engine.name = 'Thrusters Mk2'
		engine.maxSpeed = 300./float(FPS)
		engine.dv = 10./float(FPS*2.0)
		engine.dtheta = 135./float(FPS)
	elif profile == 'mk3':
		engine.name = 'Thrusters Mk3'
		engine.maxSpeed = 400./float(FPS)
		engine.dv = 20./float(FPS*1.0)
		engine.dtheta = 180./float(FPS)

