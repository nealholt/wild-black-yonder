import globalvars
import physicalObject
from scenarios import wipeOldScenario, resetDust
import pygame


class ProfilingObject(physicalObject.PhysicalObject):
	''' '''
	def __init__(self):
		physicalObject.PhysicalObject.__init__(self, 0, 0)
		wipeOldScenario()
		#Draw the new background and flip the whole screen.
		globalvars.screen.fill(globalvars.BGCOLOR)
		pygame.display.flip()
		#Countdown to next phase
		self.countdown = globalvars.FPS*5
		self.phase = 0

	def update(self):
		self.countdown -= 1
		if self.countdown < 0:
			#reset countdown
			self.countdown = globalvars.FPS*5
			#Transition to next phase
			if self.phase == 0:
				#Puts in dust and gives player ship motion.
				resetDust()
				globalvars.player.theta = 0.0
				globalvars.player.speed = 10.0
				globalvars.player.targetSpeed = 10.0
			elif self.phase == 1:
				#TODO LEFT OFF HERE
				#puts in rocks at fixed places.
				pass
			elif self.phase == 2:
				#puts in ships at fixed places.
				pass
			elif self.phase == 3:
				#clears all sprite groups again.
				#5 seconds of lots of explosions everywhere.
				pass
			elif self.phase == 4:
				#prints graphical data straight to file.
				pass

