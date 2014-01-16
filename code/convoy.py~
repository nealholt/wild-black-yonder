import pygame
import random as rd
import sys
sys.path.append('code/cython-'+str(sys.platform)) #Import from a system-specific cython folder
#Because cython files only work on the system they were compiled on.
import cygeometry


class TeamManager:
	''' '''
	def __init__(self):
		#An array of sprite groups
		self.teams = None
		#Index of the player's team
		self.player_team = 0
		self.default_enemy_team = 1
		self.default_neutral_team = 2
		#An array of int arrays. The index is the team and the integers in the
		#array at that index are teams that are enemies of the indexed team.
		self.enemies = None
		self.reset()


	def reset(self):
		#Initialize teams with an empty player team and empty default enemy team
		self.teams = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]
		self.player_team = 0
		self.default_enemy_team = 1
		self.default_neutral_team = 2
		self.enemies = [[1], [0], []]


	def addToTeam(self, ship_to_add, team_index):
		try:
			self.teams[team_index].add(ship_to_add)
		except IndexError:
			print 'ERROR in teamManager. No team with index '+str(team_index)
			exit()


	#def addToRandomTeam(self, ship_to_add):
	#	'''Adds ship_to_add to a random team and returns the index of the team it was added to.'''
	#Add this later if you want it. For now, keep things simple.


	def getEnemy(self, team_index):
		'''Returns the first enemy of team_index that is found.'''
		enemy_team_list = self.enemies[team_index]
		enemy_sprite_list = self.teams[enemy_team_list[0]].sprites()
		return enemy_sprite_list[0]


	def getRandomEnemy(self, team_index):
		'''Returns a random enemy of team_index.'''
		enemy_team_list = self.enemies[team_index]
		rand = rd.randint(0, len(enemy_team_list)-1)
		enemy_sprite_list = self.teams[enemy_team_list[rand]].sprites()
		rand = rd.randint(0, len(enemy_sprite_list)-1)
		return enemy_sprite_list[rand]


	def getAllEnemies(self, team_index):
		'''Get all enemy sprites in a list.'''
		#Get all the enemy teams
		enemy_team_list = self.enemies[team_index]
		#Compile all the enemy sprites into one list
		enemy_sprite_list = []
		for i in enemy_team_list:
			enemy_sprite_list += self.teams[i].sprites()
		return enemy_sprite_list


	def getNearestEnemy(self, location, team_index):
		'''Returns the enemy nearest location.'''
		enemy_sprite_list = self.getAllEnemies(team_index)
		nearest = None
		min_dist = 1000000.0
		for enemy in enemy_sprite_list:
			dist = cygeometry.distance(location, enemy.rect.center)
			if dist < min_dist:
				min_dist = dist
				nearest = enemy
		return nearest


	def getClosestLeadIndicator(self, location, team_index):
		'''Returns the nearest enemy by that enemy's lead indicator or None.'''
		enemy_sprite_list = self.getAllEnemies(team_index)
		nearest = None
		min_dist = 1000000.0
		for enemy in enemy_sprite_list:
			dist = cygeometry.distance(location, enemy.lead_indicator)
			if dist < min_dist:
				min_dist = dist
				nearest = enemy
		return nearest

