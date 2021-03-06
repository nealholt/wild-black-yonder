import pygame.display
import objInstances
import colors
import random as rd
from geometry import getCoordsNearLoc
import ship
import displayUtilities
import globalvars
import hudHelpers
import player
import sys
sys.path.append('code/cython-'+str(sys.platform)) #Import from a system-specific cython folder
#Because cython files only work on the system they were compiled on.
import cygeometry
from imageList import *


class ScenarioManager:
	"""I created this to reduce the number of files importing scenarios.py which was getting cumbersome and limiting usability because I had to avoid mutual imports. An object referenced by a global variable seems like a much better option even if it doesn't have much state. """
	def __init__(self):
		pass

	def asteroids(self, mission, seed=0):
		''' '''
		globalvars.disable_menu = True #Disable the standard menu for now.
		rd.seed(seed) #Fix the seed for the random number generator.
		wipeOldScenario(); resetDust(use_top=True)
		rocks = ['bigrock','medrock','smallrock','gold','silver']
		#Reset the player's location to 0,0 and his speed to zero
		globalvars.player.loc = (0.0, 0.0)
		globalvars.player.speed = 0.0
		globalvars.player.targetSpeed = 0.0
		#Define an arena 2000 pixels across for the player and all the asteroids
		#to bounce around inside
		globalvars.arena = 1000 #1000 pixel radius centered at zero, zero.
		#Make the background color blue so that we can draw a black circle 
		#to show where the arena is located.
		globalvars.BGCOLOR = colors.blue
		#Draw a black circle and put it in intangibles to show the limits 
		#of the arena
		temp = objInstances.FixedCircle(x=0, y=0, radius=globalvars.arena, color=colors.black)
		globalvars.intangibles_bottom.add(temp)
		#Make 10 rocks centered around, but not on the player
		for _ in range(10):
			#Select a rock type
			rock = rocks[rd.randint(0, len(rocks)-1)]
			#Get the coordinates of the rock
			mindist = 200
			maxdist = 800
			x,y = getCoordsNearLoc(globalvars.player.rect.center, mindist, maxdist, maxdist)
			#Make the rock
			temp = objInstances.Asteroid(x=x, y=y, image_name=rock)
			globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
		time_limit = 30 #time limit in seconds
		points_to_win = 50
		text = ['ASTEROIDS COMPLETED']
		#Display timer and score count with the following:
		globalvars.score_keeper = displayUtilities.TimeLimitDisplay(text, \
			points_to_win=points_to_win, time_limit=time_limit, mission=mission)
		globalvars.intangibles_top.add(globalvars.score_keeper)
		#Draw the new background and flip the whole screen.
		globalvars.screen.fill(globalvars.BGCOLOR)
		pygame.display.flip()
		#Display the intro to the mission
		globalvars.menu.setBasicTextPanel(['You have '+str(time_limit)+' seconds to collect '+str(points_to_win)+' points.', 'Blow up asteroids and collect gems to earn points.'])


	def gemWild(self, mission, seed=0):
		globalvars.disable_menu = True #Disable the standard menu for now.
		rd.seed(seed) #Fix the seed for the random number generator.
		wipeOldScenario(); resetDust(use_top=True)
		#Reset the player's location to 0,0 and his speed to zero
		globalvars.player.loc = (0.0, 0.0)
		globalvars.player.speed = 0.0
		globalvars.player.targetSpeed = 0.0
		#Define an arena 2000 pixels across for the player and all the asteroids
		#to bounce around inside
		globalvars.arena = 1000 #1000 pixel radius centered at zero, zero.
		#Make the background color blue so that we can draw a black circle 
		#to show where the arena is located.
		globalvars.BGCOLOR = colors.blue
		#Draw a black circle and put it in intangibles to show the limits 
		#of the arena
		temp = objInstances.FixedCircle(x=0, y=0, radius=globalvars.arena, color=colors.black)
		globalvars.intangibles_bottom.add(temp)
		#Make 50 crystals centered around, but not on the player
		for _ in range(50):
			mindist = 200
			maxdist = 800
			x,y = getCoordsNearLoc(globalvars.player.rect.center, mindist, maxdist, maxdist)
			temp = objInstances.Gem(x=x, y=y)
			globalvars.tangibles.add(temp); globalvars.whiskerables.add(temp)
		time_limit = 30 #time limit in seconds
		points_to_win=150
		text = ['GEM WILD COMPLETED']
		#Display timer and score count with the following:
		globalvars.score_keeper = displayUtilities.TimeLimitDisplay(text, \
			points_to_win=150, time_limit=time_limit, mission=mission)
		globalvars.intangibles_top.add(globalvars.score_keeper)
		#Draw the new background and flip the whole screen.
		globalvars.screen.fill(globalvars.BGCOLOR)
		pygame.display.flip()
		#Display the intro to the mission
		globalvars.menu.setBasicTextPanel(['You have '+str(time_limit)+' seconds to collect '+str(points_to_win)+' points.', 'Collect gems to earn points.'])


	def race(self, mission, seed=0):
		globalvars.disable_menu = True #Disable the standard menu for now.
		rd.seed(seed) #Fix the seed for the random number generator.
		'''Race (infinite space) - player is given a destination and the clock 
		starts ticking. Space is populated pseudo randomly (deterministically) 
		with obstacles, enemies, gems.'''
		wipeOldScenario(); resetDust()
		#Reset the player's location to 0,0 and his speed to zero
		globalvars.player.loc = (0.0, 0.0)
		globalvars.player.speed = 0.0
		globalvars.player.targetSpeed = 0.0
		finish_line = (6000, 0)
		bulls_eye = objInstances.FinishBullsEye(globalvars.player, finish_line)
		#Display arrow to finish line
		globalvars.intangibles_top.add(displayUtilities.ArrowToDestination(bulls_eye))
		#Display finish bullseye
		globalvars.intangibles_top.add(bulls_eye)
		#determine what sorts of obstacles to put on the race course.
		numbers = dict()
		numbers['enemy'] = 3
		numbers['crystal'] = 5
		numbers['large_asteroid'] = 20
		numbers['medium_asteroid'] = 30
		numbers['small_asteroid'] = 40
		numbers['gold_metal'] = 5
		numbers['silver_metal'] = 6
		numbers['health'] = 7
		numbers['capital_ship'] = 0
		#Populate space in a semi narrow corridor between the player and the finish line
		course_length = 6000 #pixels
		course_height = 1000 #pixels
		#Midway between player and destination
		midway = (course_length/2, 0)
		hudHelpers.populateSpace(objects=numbers, width=course_length, \
			height=course_height, center=midway, seed=rd.random())
		time_limit = 30 #time limit in seconds
		text = ['RACE COMPLETED']
		#Display timer and score count with the following:
		globalvars.score_keeper = displayUtilities.TimeLimitDisplay(text, \
			points_to_win=1000000, time_limit=time_limit, mission=mission)
		globalvars.intangibles_top.add(globalvars.score_keeper)
		#Draw the new background and flip the whole screen.
		globalvars.screen.fill(globalvars.BGCOLOR)
		pygame.display.flip()
		#Display the intro to the mission
		globalvars.menu.setBasicTextPanel(['You have '+str(time_limit)+' seconds to reach the finish.', 'Follow the yellow arrow and reach the finish bullseye before time runs out in order to win.'])


	def furball(self, mission, seed=0):
		globalvars.disable_menu = True #Disable the standard menu for now.
		rd.seed(seed) #Fix the seed for the random number generator.
		wipeOldScenario(); resetDust()
		globalvars.BGIMAGE = image_list['bggalaxies'].convert()
		#Make a few enemies near the player
		mindist = 200
		maxdist = 800
		#Make enemy units:
		points_to_win = 3 #Same as the number of enemies
		for _ in xrange(points_to_win):
			x,y = getCoordsNearLoc(globalvars.player.rect.center, mindist, maxdist, maxdist)
			enemy_ship = hudHelpers.getNewEnemy(x,y,'destroyer',2,2,2,2,2)
			hudHelpers.addNewEnemyToWorld(enemy_ship)
		#Make the score keeper:
		time_limit = 30 #time limit in seconds
		text = ['FURBALL COMPLETED']
		#Display timer and score count with the following:
		globalvars.score_keeper = displayUtilities.TimeLimitDisplay(text, \
			points_to_win=points_to_win, time_limit=time_limit, mission=mission)
		globalvars.intangibles_top.add(globalvars.score_keeper)
		#Draw the new background and flip the whole screen.
		globalvars.screen.blit(globalvars.BGIMAGE, (0,0))
		pygame.display.flip()
		#Display the intro to the mission
		globalvars.menu.setBasicTextPanel(['You have '+str(time_limit)+' seconds to defeat 3 enemies to win.'])


	def capitalShipScenario(self, mission, seed=0):
		globalvars.disable_menu = True #Disable the standard menu for now.
		rd.seed(seed) #Fix the seed for the random number generator.
		wipeOldScenario(); resetDust()
		globalvars.BGIMAGE = image_list['bggalaxies'].convert()
		#Make the capital ship
		enemy_ship = hudHelpers.getNewCapitalShip(0,400)
		hudHelpers.addNewCapitalShipToWorld(newship)
		#Create the score keeper.
		time_limit = 30 #time limit in seconds
		text = ['CAPITAL SHIP BATTLE COMPLETED']
		#Display timer and score count with the following:
		globalvars.score_keeper = displayUtilities.TimeLimitDisplay(text, \
			points_to_win=100, time_limit=time_limit, mission=mission)
		globalvars.intangibles_top.add(globalvars.score_keeper)
		#Draw the new background and flip the whole screen.
		globalvars.screen.blit(globalvars.BGIMAGE, (0,0))
		pygame.display.flip()
		#Display the intro to the mission
		globalvars.menu.setBasicTextPanel(['You have '+str(time_limit)+' seconds to defeat the capital ship to win.'])


	def escort(self, mission, seed=0):
		globalvars.disable_menu = True #Disable the standard menu for now.
		rd.seed(seed) #Fix the seed for the random number generator.
		'''Escort (infinite space) - player must escort a friendly NPC ship to the destination'''
		wipeOldScenario(); resetDust()
		#Reset the player's location to 0,0 and his speed to zero
		globalvars.player.loc = (0.0, 0.0)
		globalvars.player.speed = 0.0
		globalvars.player.targetSpeed = 0.0
		finish_line = (6000, 0)
		#Protect this little dude on his way to the finish line.
		npc_friend = hudHelpers.getNewEnemy(25.0,25.0,'ship',2,2,0,0,0)
		npc_friend.setDestination(finish_line)
		npc_friend.state = ship.GOTO_STATE
		hudHelpers.addNewEnemyToWorld(npc_friend, add_to_team=globalvars.team_manager.player_team)
		#Display arrow to finish line
		globalvars.intangibles_top.add(displayUtilities.ArrowToDestination(npc_friend))
		#Display finish bullseye
		globalvars.intangibles_top.add(objInstances.FinishBullsEye(npc_friend, finish_line))
		#determine what sorts of obstacles to put on the race course.
		numbers = dict()
		numbers['enemy'] = 3
		numbers['crystal'] = 5
		numbers['large_asteroid'] = 20
		numbers['medium_asteroid'] = 30
		numbers['small_asteroid'] = 40
		numbers['gold_metal'] = 5
		numbers['silver_metal'] = 6
		numbers['health'] = 7
		numbers['capital_ship'] = 0
		#Populate space in a semi narrow corridor between the player and the finish line
		course_length = 6000 #pixels
		course_height = 1000 #pixels
		#Midway between player and destination
		midway = (course_length/2, 0)
		hudHelpers.populateSpace(objects=numbers, width=course_length, \
			height=course_height, center=midway, seed=rd.random())
		time_limit = 60 #time limit in seconds
		text = ['ESCORT MISSION COMPLETED']
		#Display timer and score count with the following:
		globalvars.score_keeper = displayUtilities.TimeLimitDisplay(text, \
			points_to_win=1000000, time_limit=time_limit, mission=mission)
		globalvars.intangibles_top.add(globalvars.score_keeper)
		#Draw the new background and flip the whole screen.
		globalvars.screen.fill(globalvars.BGCOLOR)
		pygame.display.flip()
		#Display the intro to the mission
		globalvars.menu.setBasicTextPanel(['You have '+str(time_limit)+' seconds to escort the friendly NPC to the finish.', 'If you lose your NPC ally, look for the yellow arrow.'])


	def epicBattle(self, mission, seed=0):
		globalvars.disable_menu = True #Disable the standard menu for now.
		rd.seed(seed) #Fix the seed for the random number generator.
		wipeOldScenario(); resetDust()
		globalvars.BGIMAGE = image_list['bggalaxies'].convert()
		spacing = 50
		n = 3
		#Make n+1 enemy units starting to the left of the player:
		start = (globalvars.player.rect.centerx-500, globalvars.player.rect.centery)
		for i in range(n+1):
			enemy_ship = hudHelpers.getNewEnemy(start[0],start[1]+spacing*i,\
				'destroyer',2,2,2,2,2)
			hudHelpers.addNewEnemyToWorld(enemy_ship)
		#Add an enemy capital ship
		enemy_ship = hudHelpers.getNewCapitalShip(start[0],start[1]+spacing*n)
		hudHelpers.addNewEnemyToWorld(enemy_ship)
		#Make n friendly units:
		start = (globalvars.player.rect.centerx+500, globalvars.player.rect.centery)
		add_to_blue = True
		for i in range(n):
			friendly_ship = hudHelpers.getNewEnemy(start[0],start[1]+spacing*i,\
				'ship',2,2,2,2,2)
			friendly_ship.theta = 179.0 #Face the ship to the left
			hudHelpers.addNewEnemyToWorld(friendly_ship,\
				add_to_team=globalvars.team_manager.player_team)
		#Add a friendly capital ship
		friendly_ship = hudHelpers.getNewCapitalShip(start[0],start[1]+spacing*n)
		hudHelpers.addNewEnemyToWorld(friendly_ship,\
			add_to_team=globalvars.team_manager.player_team)
		#Make the score keeper:
		time_limit = 120 #time limit in seconds
		text = ['BATTLE COMPLETED']
		#Display timer and score count with the following:
		globalvars.score_keeper = displayUtilities.TimeLimitDisplay(text, \
			points_to_win=103, time_limit=time_limit, mission=mission)
		globalvars.intangibles_top.add(globalvars.score_keeper)
		#Draw the new background and flip the whole screen.
		globalvars.screen.blit(globalvars.BGIMAGE, (0,0))
		pygame.display.flip()
		#Display the intro to the mission
		globalvars.menu.setBasicTextPanel(['You have '+str(time_limit)+' seconds to defeat the enemy team and prevent your team from being defeated.','Your team is to the right. The enemy team is to the left.'])


	def goToInfiniteSpace(self, nodeid, update=True):
		'''This is a helper method that enables the menu system to function more easily.
		nodeid of the infinite space and the seed to use to generate the space.'''
		opportunity = None #See factions.update for what opportunity is all about
		if update:
			#Update all the factions
			opportunity = globalvars.factions.update(nodeid)
		#Get the node that has the id that this portal will lead to
		n = globalvars.galaxy.getNode(nodeid)
		self.infiniteSpace(seed=nodeid, playerloc=n.loc, node=n)
		#Check for an opportunity. This is when a player is moving to a node that is
		#the target of an action from a faction.
		if not opportunity is None:
			globalvars.menu.setOpportunityPanel(opportunity)
		#If the player has moved to a node in his path, then pop it.
		if len(globalvars.player.destinationNode) > 0 and globalvars.player.destinationNode[0] == nodeid:
			globalvars.player.destinationNode.pop(0)
		#Reset the arrow to the destination
		self.resetArrow()
		#If this node is faction-owned, then give the player options of minigame missions
		if n.owner != -1:
			globalvars.menu.setFactionMissionPanel(n)


	def infiniteSpace(self, seed=0, playerloc=(0.0,0.0), node=None):
		rd.seed(seed) #Fix the seed for the random number generator.
		wipeOldScenario(); resetDust()
		#Reset the player's location to 0,0 and his speed to zero
		globalvars.player.loc = playerloc
		globalvars.player.speed = 0.0
		globalvars.player.targetSpeed = 0.0
		globalvars.player.nodeid = seed #Player's new node id is set to be the seed argument.
		#Place warp portals
		if not node is None:
			globalvars.galaxy.player_node = node #Current node is updated
			for w in node.warps:
				globalvars.tangibles.add(w)
		else: #Current node is updated
			globalvars.galaxy.player_node = globalvars.galaxy.getNode(seed)
		#Need a new hud helper that will generate the landscape and clean up distant objects on the fly.
		globalvars.intangibles_bottom.add(hudHelpers.InfiniteSpaceGenerator(seed=seed))
		#Display player location and speed info with the following:
		globalvars.intangibles_top.add(displayUtilities.ShipStatsText())

		announcement = displayUtilities.TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY, 
			text='You\'ve arrived in system '+str(seed),
			timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
		globalvars.intangibles_top.add(announcement)

		#Draw the new background and flip the whole screen.
		globalvars.screen.fill(globalvars.BGCOLOR)
		pygame.display.flip()


	def setDestinationNode(self, nodeid):
		'''Chart a shortest path using breadth first search to the node with the given id.
		Set the player's destination to be the path.
		Get the very first node in the path and point an arrow to it to lead 
		the player in the right direction.'''
		#End conditions
		failure = False #But this can be true if we run out of destinations to append.
				#There are disconnects in the graph.
		success = False #This is set true when we find the destination
		#Append as tuples all nodes reachable from player's current node along with the distance to them.
		visited_node_ids = [globalvars.player.nodeid]
		old_bfs_array = []
		new_bfs_array = []
		current_node = globalvars.galaxy.player_node
		for connectid,location in current_node.connections:
			#If connectid is the destination then we can shortcircuit here
			if connectid == nodeid:
				globalvars.player.destinationNode = [nodeid]
				new_bfs_array = []
				success = True
				break
			if not connectid in visited_node_ids:
				#Calculate the distance (aka cost)
				cost = cygeometry.distance(current_node.loc, location)
				visited_node_ids.append(connectid)
				#Append a tuple where the first element is a path in the form of 
				#an array of node ids and the second element is the cost of the path.
				new_bfs_array.append(([connectid], cost))
		while not success and not failure:
			#Sort by shortest path when updating the arrays
			old_bfs_array = sorted(new_bfs_array, key=lambda pair: pair[1])
			new_bfs_array = []
			#We may exhaust all the connections if the destination is not 
			#connected to the player's location.
			if len(old_bfs_array) == 0:
				failure = True
				continue
			#Then for each node by id in the current list
			for path, cost in old_bfs_array:
				if success == True: break
				#Get the last node in the path
				current_node = globalvars.galaxy.getNode(path[-1])
				#For each of the node's neighbors
				for connectid,location in current_node.connections:
					#If connectid is the destination then we can shortcircuit here
					if connectid == nodeid:
						path.append(nodeid)
						globalvars.player.destinationNode = path
						success = True
						break
					#skip if the neighbor has already been considered
					#otherwise add node+neighbor + the sum of the distances to a new list
					elif not connectid in visited_node_ids:
						#Calculate the distance (aka cost)
						extra_cost = cygeometry.distance(current_node.loc, location)
						visited_node_ids.append(connectid)
						#Append a tuple where the first element is a path in the form of 
						#an array of node ids and the second element is the cost of 
						#the path.
						new_bfs_array.append((path+[connectid], cost+extra_cost))
		#If we failed to find a path, return false
		if failure: return False
		#Otherwise, make a new arrow point to the first warp point on the path and remove any old arrows.
		self.resetArrow()
		return True #Indicate that the destination was successfully set.


	def resetArrow(self):
		#Error check
		if len(globalvars.player.destinationNode) == 0:
			return True
		#Get the first node on the path:
		next_node_id = globalvars.player.destinationNode[0]
		#Get the location of the destination node
		for w in globalvars.galaxy.player_node.warps:
			if w.destinationNode == next_node_id:
				#Set the warp as the destination for the arrow to point at
				self.setArrowTarget(w)


	def setArrowTarget(self, target):
		#Search through intangibles_top and find the arrow then change its target
		arrow_set = False
		for i in globalvars.intangibles_top:
			if i.is_a == globalvars.ARROW:
				i.target = target
				arrow_set = True
				break
		if not arrow_set:
			#Create a new arrow pointing to the target and add it to intangibles_top
			globalvars.intangibles_top.add(displayUtilities.ArrowToDestination(target))
			


	def restart(self):
		'''Give the player a new ship and boot him to the testing scenario. '''
		globalvars.player = player.Player('ship')
		globalvars.menu.main_panel = None

		#Order matters. This has to go after making the new player.
		self.goToInfiniteSpace(0)

		#reset the death display countdown
		globalvars.deathcountdown = 15





def wipeOldScenario():
	globalvars.tangibles.empty()
	globalvars.intangibles_bottom.empty()
	globalvars.intangibles_top.empty()
	globalvars.whiskerables.empty()
	globalvars.team_manager.reset()
	globalvars.BGCOLOR = colors.black
	globalvars.BGIMAGE = None
	globalvars.score_keeper = None
	#Add the player back in.
	#Set the player's health bar. This must be done right before adding any ship to tangibles
	globalvars.player.setHealthBar()
	globalvars.tangibles.add(globalvars.player)
	globalvars.whiskerables.add(globalvars.player)
	globalvars.team_manager.addToTeam(globalvars.player, globalvars.team_manager.player_team)
	#Immediately clear the panel
	globalvars.menu.main_panel = None
	#Reset the arena
	globalvars.arena = 0
	#Add back in the storyteller
	globalvars.intangibles_bottom.add(globalvars.story_keeper)


def resetDust(use_top=False):
	#Kill all the old dust.
	for d in globalvars.intangibles_bottom:
		if d.is_a == globalvars.DUST:
			d.kill()
	for d in globalvars.intangibles_top:
		if d.is_a == globalvars.DUST:
			d.kill()
	#Make 50 dust particles scattered around the player.
	for _ in range(50):
		x,y = getCoordsNearLoc(globalvars.player.rect.center, 50, 
				globalvars.WIDTH, globalvars.WIDTH)
		temp = objInstances.Dust(x=x, y=y, width=1, height=1,\
				 color=colors.white)
		if use_top:
			globalvars.intangibles_top.add(temp)
		else:
			globalvars.intangibles_bottom.add(temp)


