import globalvars
import physicalObject
from scenarios import wipeOldScenario, resetDust
import pygame
import hudHelpers
from geometry import getCoordsNearLoc
import objInstances
import sys


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
		self.player_destination = (100000000,0)
		self.is_a = 'profiling_object'

	def update(self):
		self.countdown -= 1
		globalvars.player.destination = self.player_destination
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
				self.phase += 1
			elif self.phase == 1:
				#puts in rocks at fixed places.
				numbers = dict()
				numbers['enemy'] = 0
				numbers['crystal'] = 5
				numbers['large_asteroid'] = 20
				numbers['medium_asteroid'] = 30
				numbers['small_asteroid'] = 40
				numbers['gold_metal'] = 5
				numbers['silver_metal'] = 6
				numbers['health'] = 7
				numbers['capital_ship'] = 0
				#Populate space in a semi narrow corridor between the player and the finish line
				course_length = 8000 #pixels
				course_height = 1000 #pixels
				#Midway between player and destination
				midway = (course_length/2, 0)
				hudHelpers.populateSpace(objects=numbers,\
					width=course_length, \
					height=course_height,\
					center=globalvars.player.rect.center,\
					seed=0)
				self.phase += 1
			elif self.phase == 2:
				#puts in ships at fixed places.
				#puts in rocks at fixed places.
				numbers = dict()
				numbers['enemy'] = 10
				numbers['crystal'] = 0
				numbers['large_asteroid'] = 0
				numbers['medium_asteroid'] = 0
				numbers['small_asteroid'] = 0
				numbers['gold_metal'] = 0
				numbers['silver_metal'] = 0
				numbers['health'] = 0
				numbers['capital_ship'] = 1
				#Populate space in a semi narrow corridor between the player and the finish line
				course_length = 8000 #pixels
				course_height = 1000 #pixels
				#Midway between player and destination
				midway = (course_length/2, 0)
				hudHelpers.populateSpace(objects=numbers,\
					width=course_length, \
					height=course_height,\
					center=globalvars.player.rect.center,\
					seed=0)
				self.phase += 1
			elif self.phase == 3:
				#clears all sprite groups again.
				wipeOldScenario()
				#Add self back in
				globalvars.intangibles_bottom.add(self)
				#Draw the new background and flip the whole screen.
				globalvars.screen.fill(globalvars.BGCOLOR)
				pygame.display.flip()
				resetDust()
				#5 seconds of lots of explosions everywhere.
				self.phase += 1
			elif self.phase == 4:
				#prints graphical data straight to file.
				if sys.platform != 'darwin': #This is not working on my mac for some reason
					import matplotlib.pyplot as plt
					plt.plot(globalvars.dirty_rect_size)
					plt.xlabel('Frames')
					plt.ylabel('Number of dirty rects')
					plt.savefig('profiling/dirty_rect_size.jpeg') #plt.show()
					plt.clf()
					plt.plot(globalvars.time_lapses, 'ro')
					plt.xlabel('Frames')
					plt.ylabel('Tick length')
					plt.savefig('profiling/tick_lengths.jpeg') #plt.show()
					plt.clf()
				exit()
		if self.phase == 4:
			x,y = getCoordsNearLoc(globalvars.player.rect.center, 50, 
				globalvars.WIDTH, globalvars.WIDTH)
			globalvars.intangibles_top.add(objInstances.Explosion(x=x,y=y))



class CollisionAvoidanceTester(physicalObject.PhysicalObject):
	''' '''
	def __init__(self):
		physicalObject.PhysicalObject.__init__(self, 0, 0)
		wipeOldScenario()
		#Draw the new background and flip the whole screen.
		globalvars.screen.fill(globalvars.BGCOLOR)
		pygame.display.flip()
		#Countdown to next phase
		self.countdown = 0
		self.phase = 0
		self.player_destination = (100000000,0)
		self.is_a = 'profiling_object'
		self.most_recent_closest = ''

	def update(self):
		self.countdown -= 1
		globalvars.player.destination = self.player_destination
		#print globalvars.player.theta
		if globalvars.player.closest_sprite != self.most_recent_closest:
			self.most_recent_closest = globalvars.player.closest_sprite
			print 'Closest is now: '+str(self.most_recent_closest)
		if self.countdown < 0:
			#reset countdown
			self.countdown = globalvars.FPS*15

			#clears all sprite groups again.
			wipeOldScenario()
			#Add self back in
			globalvars.intangibles_bottom.add(self)
			#Draw the new background and flip the whole screen.
			globalvars.screen.fill(globalvars.BGCOLOR)
			pygame.display.flip()
			resetDust()

			globalvars.player.theta = 0.0
			#globalvars.player.speed = 2.0
			#globalvars.player.targetSpeed = 2.0
			#globalvars.player.maxSpeed = 2.0

			#puts in rocks at fixed places.
			numbers = dict()
			numbers['enemy'] = 0
			numbers['crystal'] = 5
			numbers['large_asteroid'] = 20
			numbers['medium_asteroid'] = 30
			numbers['small_asteroid'] = 40
			numbers['gold_metal'] = 5
			numbers['silver_metal'] = 6
			numbers['health'] = 7
			numbers['capital_ship'] = 0
			#Populate space in a semi narrow corridor between the player and the finish line
			course_length = 8000 #pixels
			course_height = 1000 #pixels
			#Midway between player and destination
			midway = (course_length/2, 0)
			hudHelpers.populateSpace(objects=numbers,\
				width=course_length, \
				height=course_height,\
				center=globalvars.player.rect.center,\
				seed=self.phase)
			self.phase += 1

