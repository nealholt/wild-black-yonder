import pygame

class Convoy:
	''' '''
	def __init__(self):
		#A list containing the ships in the convoy
		self.ships = []
		#Index of the convoy's team affiliation
		self.team = 0
		#
		self.danger_close_threshold = 400
		#
		self.destination = None

