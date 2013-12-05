import drawable
import pygame
import colors
import globalvars
from geometry import angleFromPosition, translate
import sys
sys.path.append('code/cython')
import cygeometry
import random as rd

def splitTooLongWord(word_to_split='', length_limit=20):
	'''If word_to_split is longer than length_limit, split it into two 
	words of roughly equal size and return them. '''
	word_length = len(word_to_split)
	if word_length > length_limit:
		#Find the blank space closest to the middle of the word
		mid = word_length/2
		min_dist = word_length
		space_index = -1
		for i in range(word_length):
			if word_to_split[i] == ' ':
				dist = abs(i-mid)
				if dist <= min_dist:
					min_dist = dist
					space_index = i
		return (word_to_split[:space_index], word_to_split[space_index:])
	return (word_to_split, '')


def buyGas():
	globalvars.player.fuel += 1000
	globalvars.player.money -= 10
	globalvars.menu.setGasStationPanel()

def buyProduct(triple):
	product_name, sell_price, seed = triple
	globalvars.player.buyTradeGood(product_name, sell_price)
	globalvars.menu.setTradingPanel(seed)

def sellProduct(triple):
	product_name, sell_price, seed = triple
	globalvars.player.sellTradeGood(product_name, sell_price)
	globalvars.menu.setTradingPanel(seed)

def padStringLength(string, length, padding): #TODO Can't this go somewhere else?
	toReturn = string
	while len(toReturn) < length:
		toReturn += padding
	return toReturn

#TODO START should the following all go elsewhere?
def unequipPlayerGun():
	'''This method allows me to keep the unequipGun method in the ship object 
	unpolluted by menu concerns, but to also reset the menu to reflect changes the 
	player makes to his ship.'''
	globalvars.player.unequipGun()
	globalvars.menu.setShipPanel()


def unequipPlayerMissile():
	'''This method allows me to keep the unequipMissile method in the ship object 
	unpolluted by menu concerns, but to also reset the menu to reflect changes the 
	player makes to his ship.'''
	globalvars.player.unequipMissile()
	globalvars.menu.setShipPanel()


def unequipPlayerMine():
	'''This method allows me to keep the unequipMine method in the ship object 
	unpolluted by menu concerns, but to also reset the menu to reflect changes the 
	player makes to his ship.'''
	globalvars.player.unequipMine()
	globalvars.menu.setShipPanel()


def unequipPlayerEngine():
	'''This method allows me to keep the unequipEngine method in the ship object 
	unpolluted by menu concerns, but to also reset the menu to reflect changes the 
	player makes to his ship.'''
	globalvars.player.unequipEngine()
	globalvars.menu.setShipPanel()


def equipPlayerWeapon(cargo_index):
	'''This method allows me to keep the equipWeaponFromCargo method in the ship object 
	unpolluted by menu concerns, but to also reset the menu to reflect changes the 
	player makes to his ship.'''
	globalvars.player.equipWeaponFromCargo(cargo_index)
	globalvars.menu.setShipPanel()


def equipPlayerEngine(cargo_index):
	'''This method allows me to keep the equipEngineFromCargo method in the ship object 
	unpolluted by menu concerns, but to also reset the menu to reflect changes the 
	player makes to his ship.'''
	globalvars.player.equipEngineFromCargo(cargo_index)
	globalvars.menu.setShipPanel()


def equipPlayerShip(cargo_index):
	'''This method allows me to keep the equipShipFromCargo method in the player object 
	unpolluted by menu concerns, but to also reset the menu to reflect changes the 
	player makes to his ship.'''
	globalvars.player.equipShipFromCargo(cargo_index)
	globalvars.menu.setShipPanel()
#TODO END


top = globalvars.MENU_BORDER_PADDING
left = globalvars.MENU_BORDER_PADDING
height = globalvars.HEIGHT-2*globalvars.MENU_BORDER_PADDING
width = globalvars.WIDTH-2*globalvars.MENU_BORDER_PADDING
topbuffer = 100
font_size = 24
stringLength = 30


class Panel:
	"""The basic building block of the menu system. """
	def __init__(self):
		self.panels = []
		self.drawables = []
		self.method = None #Invoke this when the panel is clicked on.
		self.alt_color = colors.green #Use this alternate color upon mouseover
		self.use_alt = False
		self.argument = None #This is useful if the method of the panel takes an argument.

	def addDrawable(self, drawable):
		self.drawables.append(drawable)

	def addPanel(self, panel):
		self.panels.append(panel)

	def highlight(self):
		'''This function is called in response to mouse over events.'''
		self.use_alt = True

	def anySelected(self, pos):
		for d in self.drawables:
			if d.rect.collidepoint(pos):
				return True
		return False

	def setMethod(self, method):
		self.method = method

	def handleEvent(self, event):
		if not self.method is None:
			self.use_alt = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				#Not all event types have positions so we check this inside the other guard.
				if self.anySelected(event.pos):
					if self.argument is None:
						self.method()
					else:
						self.method(self.argument)
			elif event.type == pygame.MOUSEMOTION:
				#Not all event types have positions so we check this inside the other guard.
				if self.anySelected(event.pos):
					self.highlight()
		#Pass event down to sub panels
		for panel in self.panels:
			panel.handleEvent(event)

	def draw(self):
		"""draws this panel on the surface."""
		for d in self.drawables:
			if self.use_alt:
				d.draw(use_color=self.alt_color)
			else:
				d.draw()
		for panel in self.panels:
			panel.draw()


class Menu:
	"""globalvars.menu points to one of these objects in order to reduce the amount of file imports while increasing the availability of menu methods."""
	def __init__(self):
		self.main_panel = None #When this is not none, it should be displayed on the screen.


	def addMenuItem(self, x1=0, y1=0, string='', local_font_size=24, textbuffer=0, text_color=colors.white, method=None, argument=None, framed=False, width=100, height=100, frame_thickness=2, frame_color=colors.yellow):
		'''This code is repeated far too often not to just use a method.'''
		subpanel = Panel()
		if framed:
			temp = drawable.Rectangle(x1=x1, y1=y1, width=width, height=height, \
				color=frame_color, thickness=frame_thickness)
			subpanel.addDrawable(temp)
		if string != '':
			temp = drawable.Text(x1=(x1+textbuffer), y1=(y1+textbuffer), \
				string=string, font_size=local_font_size, color=text_color)
			subpanel.addDrawable(temp)
		subpanel.setMethod(method)
		subpanel.argument = argument
		self.main_panel.addPanel(subpanel)


	def setStandardMenu(self, tabs=True):
		'''There was a lot of code duplication so I stuck it in a method all its own.'''
		self.main_panel = Panel()
		#First draw a white frame around the menu.
		temp = drawable.Rectangle(x1=left, y1=top, width=width, height=height, \
			color=colors.white, thickness=3)
		self.main_panel.addDrawable(temp)
		#Then draw the background for the menu
		temp = drawable.Rectangle(x1=left, y1=top, width=width, height=height, \
			color=colors.reddishgray)
		self.main_panel.addDrawable(temp)
		#Add tabs to the menu:
		if tabs: self.addAllTabs()


	def addTextToMainPanel(self, text_array, this_left, this_top, local_font_size=font_size):
		for i in range(len(text_array)):
			temp = drawable.Text(x1=this_left,\
				y1=font_size*i+this_top, string=text_array[i],\
				font_size=local_font_size, color=colors.white)
			self.main_panel.addDrawable(temp)


	def addAllTabs(self):
		'''Takes a menu and adds a standard set of tabs along the top of the menu.'''
		width = 100
		localheight = 20
		textbuffer = 9
		framethickness = 2
		x_val = left
		#ship
		self.addMenuItem(x1=x_val, y1=top, string='Ship', textbuffer=textbuffer, method=globalvars.menu.setShipPanel, framed=True, width=width, height=localheight, frame_thickness=framethickness, frame_color=colors.yellow)
		x_val += width
		#galaxy info
		self.addMenuItem(x1=x_val, y1=top, string='Galaxy', textbuffer=textbuffer, method=globalvars.menu.setGalaxyPanel, argument=False, framed=True, width=width, height=localheight, frame_thickness=framethickness, frame_color=colors.yellow)
		x_val += width
		#galaxy travel
		self.addMenuItem(x1=x_val, y1=top, string='Far Travel', textbuffer=textbuffer, method=globalvars.menu.setGalaxyPanel, argument=True, framed=True, width=width, height=localheight, frame_thickness=framethickness, frame_color=colors.yellow)
		x_val += width
		#local info
		self.addMenuItem(x1=x_val, y1=top, string='Local Info', textbuffer=textbuffer, method=globalvars.menu.setLocalGalaxyPanel, argument=False, framed=True, width=width, height=localheight, frame_thickness=framethickness, frame_color=colors.yellow)
		x_val += width
		#local travel
		self.addMenuItem(x1=x_val, y1=top, string='Travel', textbuffer=textbuffer, method=globalvars.menu.setLocalGalaxyPanel, argument=True, framed=True, width=width, height=localheight, frame_thickness=framethickness, frame_color=colors.yellow)
		x_val += width
		#Player profile page
		self.addMenuItem(x1=x_val, y1=top, string='Profile', textbuffer=textbuffer, method=globalvars.menu.setPlayerProfilePanel, framed=True, width=width, height=localheight, frame_thickness=framethickness, frame_color=colors.yellow)
		x_val += width
		#test scenarios
		self.addMenuItem(x1=x_val, y1=top, string='Test', textbuffer=textbuffer, method=globalvars.menu.setTestingPanel, framed=True, width=width, height=localheight, frame_thickness=framethickness, frame_color=colors.yellow)
		x_val += width
		#factions
		self.addMenuItem(x1=x_val, y1=top, string='Faction', textbuffer=textbuffer, method=globalvars.menu.setFactionPanel, framed=True, width=width, height=localheight, frame_thickness=framethickness, frame_color=colors.yellow)
		x_val += width


	def setTestingPanel(self):
		self.setStandardMenu()
		#Then draw the contents of the menu
		horiz_space = 200
		vert_space = 70
		x1, y1 = horiz_space, globalvars.HEIGHT/2
		radius = 10
		texts = ['Asteroids', 'Gem Wild', 'Race', 'Furball', 'Capital ship']
		methods = [globalvars.scenario_manager.asteroids, globalvars.scenario_manager.gemWild, globalvars.scenario_manager.race, globalvars.scenario_manager.furball, globalvars.scenario_manager.capitalShipScenario]
		x2 = horiz_space*2
		methodLength = len(methods)
		for i in range(methodLength):
			j = i-methodLength/2
			y2 = globalvars.HEIGHT/2+vert_space*j

			subpanel = Panel()
			#http://www.secnetix.de/olli/Python/lambda_functions.hawk
			subpanel.setMethod(methods[i])
			temp = drawable.Circle(x1=x2, y1=y2, radius=radius, color=colors.yellow)
			subpanel.addDrawable(temp)
			temp = drawable.Text(x1=(x2+2*radius), y1=y2, string=texts[i],\
				font_size=font_size, color=colors.white)
			subpanel.addDrawable(temp)
			self.main_panel.addPanel(subpanel)

			temp = drawable.Line(x1=x1, y1=y1, x2=x2, y2=y2)
			self.main_panel.addDrawable(temp)


	def setGasStationPanel(self):
		self.setStandardMenu()
		text = [
		'Money: $'+str(globalvars.player.money),
		'Fuel: '+str(globalvars.player.fuel)]
		#Then draw the contents of the menu
		self.addTextToMainPanel(text, left+50, 100+top)
		if globalvars.player.money > 10:
			self.addMenuItem(x1=(left+200), y1=(top+200), width=180, height=40, string='Buy 1000 Fuel for $10', textbuffer=12, method=buyGas, framed=True)
		else:
			text = ['You do not have enough money.']
			self.addTextToMainPanel(text, (left+200), (top+200))


	def setTradingPanel(self, seed):
		self.setStandardMenu()
		rd.seed(seed) #Fix the seed for the random number generator.
		local_font_size = 32
		columns = [5, 250, 350, 450, 490, 580, 680]
		#Display player's money
		use_color = colors.white
		if globalvars.player.money < 1:
			use_color = colors.red
		temp = drawable.Text(x1=500,\
			y1=topbuffer-15,\
			string='Your money: $'+str(globalvars.player.money),\
			font_size=local_font_size, color=use_color)
		self.main_panel.addDrawable(temp)
		#Display player's cargospace
		use_color = colors.white
		if globalvars.player.cargospace < 1:
			use_color = colors.red
		temp = drawable.Text(x1=500,\
			y1=topbuffer+local_font_size-20,\
			string='Your cargospace: '+str(globalvars.player.cargospace),\
			font_size=local_font_size, color=use_color)
		self.main_panel.addDrawable(temp)
		#List of all current products
		product_list = ['Niblets', 'Flummox Capacitors', 'Canny Goods',\
			'Reactor Wax', 'Magnet Grease', 'Fools Iridium']
		text_array = [['PRODUCT', 'PRICE', '', 'YOURS', '', '', 'PROFIT']]
		for p in product_list:
			#Get any of this trade good that the player has.
			playerhas = globalvars.player.getTradeGoods(p)
			#Get the sell price
			sell_price = rd.randint(1,99)
			#Determine the amount the player has, profit the player could make by selling,
			#and initialize the sell button.
			player_amt = 0
			player_unit_price = ''
			sell_button = '---'
			unit_profit, percent_profit = 0.0, 0.0 #Unit profit is currently unused
			if not playerhas is None and playerhas.amount > 0:
				player_amt = playerhas.amount
				player_unit_price = ' x $'+str(int(playerhas.unit_price))
				sell_button = 'Sell'
				unit_profit, percent_profit = playerhas.getProfit(sell_price)
			#Format the percent profit nicely
			percent_profit = str(percent_profit)
			#Chop off the decimal and add a percent sign.
			percent_profit = percent_profit[:percent_profit.index('.')]
			if len(percent_profit) > 0: percent_profit += '%'
			#Determine whether or not to display the buy button.
			buy_button = '$$$'
			if globalvars.player.cargospace < 1:
				buy_button = '---'
			elif globalvars.player.money > sell_price:
				buy_button = 'Buy'
			#Populate the row of the text array corresponding to product p
			text_array.append([p, '$'+str(sell_price), buy_button,\
				str(player_amt), player_unit_price, sell_button,\
				percent_profit, sell_price])
		#Display the text array on the screen.
		for i in range(len(text_array)):
			for j in range(len(columns)):
				if text_array[i][j] == 'Buy':
					product_name = text_array[i][0]
					sell_price = text_array[i][-1]
					self.addMenuItem(x1=left+columns[j],\
						y1=local_font_size*i+topbuffer+top,\
						string='Buy', local_font_size=local_font_size,\
						width=50, height=100, textbuffer=3,\
						text_color=colors.white, method=buyProduct,\
						argument=[product_name, sell_price, seed])
				elif text_array[i][j] == 'Sell':
					product_name = text_array[i][0]
					sell_price = text_array[i][-1]
					self.addMenuItem(x1=left+columns[j],\
						y1=local_font_size*i+topbuffer+top,\
						string='Sell', local_font_size=local_font_size,\
						width=50, height=100, textbuffer=3,\
						text_color=colors.white, method=sellProduct,\
						argument=[product_name, sell_price, seed])
				else:
					temp = drawable.Text(x1=left+columns[j],\
						y1=local_font_size*i+topbuffer+top,\
						string=text_array[i][j], font_size=local_font_size)
					self.main_panel.addDrawable(temp)


	def setDestinationUpdateGalaxyTravel(self, destination_node_id):
		'''Set the player's destination to be the given node
		then update the galaxy view to highlight the path.
		If the player cannot reach the selected node, display an error message.'''
		success = globalvars.scenario_manager.setDestinationNode(destination_node_id)
		text = None
		if not success:
			text = ['You cannot reach the selected node from here.']
		self.setGalaxyPanel(True, text=text)


	def setGalaxyPanel(self, travel, text=None):
		'''Pre: galaxy is a NodeManager object that has been initialized.'''
		self.setStandardMenu()
		radius = 3 #Radius of the nodes.
		for n in globalvars.galaxy.nodes:
			subpanel = Panel()
			color = colors.yellow
			#Color the player's location red.
			if n.id == globalvars.player.nodeid:
				color = colors.red
			#If the node has an owner and the player is not here, display the owner's flag
			if n.owner != -1 and n.id != globalvars.player.nodeid:
				temp = drawable.DrawableImage(x1=n.x, y1=n.y, image=n.flag)
			else:
				temp = drawable.Circle(x1=n.x, y1=n.y, radius=radius, color=color)
			subpanel.addDrawable(temp)
			#If this node is connected to the player's current node, make it clickable
			isconnected = False
			subpanel.argument = n.id
			#If travel is set then the node method is to make a destination to the node.
			if travel:
				subpanel.setMethod(globalvars.menu.setDestinationUpdateGalaxyTravel)
			else:
				#Otherwise view options for information only
				subpanel.setMethod(globalvars.menu.setNodeViewPanel)
			self.main_panel.addPanel(subpanel)
		#Draw the connections between nodes
		for c in globalvars.galaxy.connections:
			temp = drawable.Line(x1=c[0], y1=c[1], x2=c[2], y2=c[3])
			self.main_panel.addDrawable(temp)
		#Draw a thicker orange line over the player's path
		if len(globalvars.player.destinationNode) > 0:
			start = globalvars.galaxy.getNode(globalvars.player.nodeid)
			end = globalvars.galaxy.getNode(globalvars.player.destinationNode[0])
			temp = drawable.Line(x1=start.loc[0], y1=start.loc[1],\
					x2=end.loc[0], y2=end.loc[1],\
					color=colors.blue, width=2)
			self.main_panel.addDrawable(temp)
			for i in range(len(globalvars.player.destinationNode)-1):
				start = globalvars.galaxy.getNode(globalvars.player.destinationNode[i])
				end = globalvars.galaxy.getNode(globalvars.player.destinationNode[i+1])
				temp = drawable.Line(x1=start.loc[0], y1=start.loc[1],\
						x2=end.loc[0], y2=end.loc[1],\
						color=colors.blue, width=2)
				self.main_panel.addDrawable(temp)
		#Display optional text
		if not text is None:
			self.addTextToMainPanel(text, left+100, topbuffer+top)


	def setLocalGalaxyPanel(self, travel):
		'''Pre: galaxy is a NodeManager object that has been initialized.'''
		self.setStandardMenu()
		radius = 10
		#Magnitude of the stretch.
		magnitude = 4
		#Center the player node location
		playerNodeLoc = (globalvars.CENTERX, globalvars.CENTERY)
		#Get the player's node
		playerNode = globalvars.galaxy.getNode(globalvars.player.nodeid)
		#Draw player node in the center of the menu.
		subpanel = Panel()
		subpanel.argument = globalvars.player.nodeid
		#If this node is the player's current location then make this reset
		#the player's scenario. This is really only for testing since the player
		#can get away using the testing menu by pressing the m key.
		if travel:
			subpanel.setMethod(globalvars.scenario_manager.goToInfiniteSpace)
		else:
			subpanel.setMethod(globalvars.menu.setNodeViewPanel)

		temp = drawable.Circle(x1=playerNodeLoc[0]-radius, y1=playerNodeLoc[1]-radius,
					radius=radius, color=colors.red)
		subpanel.addDrawable(temp)
		self.main_panel.addPanel(subpanel)

		#Draw all the on-screen nodes and the connections between them
		for n in globalvars.galaxy.nodes:
			angle = angleFromPosition(playerNode.loc, n.loc)
			dist = cygeometry.distance(playerNode.loc, n.loc)
			position = translate(playerNodeLoc, angle, dist*magnitude)
			#If it is on screen...
			if position[0] > globalvars.MENU_PADDING+globalvars.MENU_BORDER_PADDING and \
			position[0] < globalvars.WIDTH-globalvars.MENU_PADDING-globalvars.MENU_BORDER_PADDING and \
			position[1] > globalvars.MENU_PADDING+globalvars.MENU_BORDER_PADDING and \
			position[1] < globalvars.HEIGHT-globalvars.MENU_PADDING-globalvars.MENU_BORDER_PADDING and \
			n.id != playerNode.id:
				#Draw it
				subpanel = Panel()
				subpanel.argument = n.id
				#If travel is set and the node is already connected to the player's node
				if travel and n.alreadyConnected(globalvars.player.nodeid):
					subpanel.setMethod(globalvars.scenario_manager.setDestinationNode)
				else:
					#Otherwise view options for information only
					subpanel.setMethod(globalvars.menu.setNodeViewPanel)
				#If the node has an owner and the player is not here, display the owner's flag
				if n.owner != -1 and n.id != globalvars.player.nodeid:
					temp = drawable.DrawableImage(x1=position[0], y1=position[1], image=n.flag)
				else:
					temp = drawable.Circle(x1=position[0]-radius, y1=position[1]-radius,
							radius=radius, color=colors.yellow)
				subpanel.addDrawable(temp)
				self.main_panel.addPanel(subpanel)
				#draw connections
				for c in n.connections:
					angle = angleFromPosition(n.loc, c[1])
					dist = cygeometry.distance(n.loc, c[1])
					position2 = translate(position, angle, dist*magnitude)
					temp = drawable.Line(x1=position[0]-radius, y1=position[1]-radius,
						x2=position2[0]-radius, y2=position2[1]-radius)
					self.main_panel.addDrawable(temp)


	def setFactionPanel(self):
		self.setStandardMenu()
		temp = drawable.Text(x1=left+50,\
			y1=topbuffer+top, \
			string=padStringLength('Faction', stringLength, ' ')+'Relationship with player',\
			font_size=font_size, color=colors.white)
		self.main_panel.addDrawable(temp)
		for i in range(1, len(globalvars.factions.factions)+1):
			f = globalvars.factions.factions[i-1]
			self.addMenuItem(x1=left+50, y1=font_size*i+topbuffer+top, string=padStringLength(f.name, stringLength, ' ')+str(f.relationToPlayer), method=globalvars.menu.setFactionSpecificPanel, argument=f.id)


	def setFactionSpecificPanel(self, factionid):
		self.setStandardMenu()
		f = globalvars.factions.getFactionById(factionid)
		strings = [padStringLength('Name:', stringLength, ' ')+f.name,
			padStringLength('Flag:', stringLength, ' ')+str(f.flag),
			padStringLength('Count of owned nodes:', stringLength, ' ')+str(len(f.nodes))]
		self.addTextToMainPanel(strings, left+50, topbuffer+top)


	def setPlayerProfilePanel(self):
		self.setStandardMenu()
		text = [
		'Money:    $'+str(globalvars.player.money),
		'Health:   '+str(globalvars.player.health),
		'Fuel:      '+str(globalvars.player.fuel),
		'Trade goods capacity:  '+str(globalvars.player.cargospace)+' / '+str(globalvars.player.cargospace_max),
		'Trade goods: ']
		for tg in globalvars.player.trade_goods:
			text.append('      '+str(tg.amount)+' '+tg.name+' at $'+str(tg.unit_price)+' per')
		#Then draw the contents of the menu
		self.addTextToMainPanel(text, left+50, topbuffer+top, local_font_size=32)


	def setNodeViewPanel(self, nodeid):
		node = globalvars.galaxy.getNode(nodeid)
		self.setStandardMenu()
		text = [
		'Id: '+str(node.id)+'.',
		'Description: '+node.description+'.',
		'Hostility: '+str(node.hostility)+'. Chance to generate opposing ships.',
		'Enemy strength: '+str(node.strength)+'. Strength of opposing ships (initially just capital ship chance).',
		'Debris: '+str(node.amt_debris)+'. Chance of asteroids.',
		'Wealth: '+str(node.amt_wealth)+'. Chance of gems, health, and rich asteroids.'
		]
		#Then draw the contents of the menu
		self.addTextToMainPanel(text, left+50, topbuffer+top)
		#Write the owner if any
		if node.owner != -1:
			owner = globalvars.factions.getFactionById(node.owner)
			self.addMenuItem(x1=left+50, y1=font_size*len(text)+topbuffer+top, string='Owner: '+owner.name, method=globalvars.menu.setFactionSpecificPanel, argument=owner.id)


	def setRestartPanel(self):
		self.setStandardMenu()
		#Then draw the contents of the menu
		#Display text explaining that player died.
		temp = drawable.Text(x1=globalvars.WIDTH/2-100, y1=200, string='You have died',\
			font_size=font_size, color=colors.white)
		self.main_panel.addDrawable(temp)
		#Display button allowing player to restart.
		self.addMenuItem(x1=globalvars.WIDTH/2-75, y1=300, width=200, height=50, string='Restart', local_font_size=32, textbuffer=40, text_color=colors.white, method=globalvars.scenario_manager.restart, argument=None, framed=False, frame_thickness=2, frame_color=colors.blue)


	def setHelpPanel(self):
		self.setStandardMenu()
		help = ['INSTRUCTIONS:', 
		'Press space bar or c key or click left mouse button to shoot primary weapon.',
		'Press x key to shoot missile if equipped and not on cooldown.',
		'Press z key to lay a mine if equipped and not on cooldown.',
		'Press "/" or "?" to query game state. Currently this just prints the player\'s destination.',
		'Press escape to quit.',
		'Press "e" to create an enemy ship that will attack the player.',
		'Press up arrow or w key to increase player speed by one quarter of max up to max.',
		'Press down arrow or s key to decrease player speed by one quarter of max down to zero.',
		'Press left arrow or a key to turn counter-clockwise 30 degrees.',
		'Press right arrow or d key to turn clockwise 30 degrees.',
		'Click on the screen to tell the starship to move towards the clicked point.',
		'Press "m" open the menus. This also pauses the game.',
		'Press anything to close the current menu.',
		'Press "b" to slow down and park at destination.',
		'Press "q" to remove destination set by mouse click and simply fly in current direction.',
		'Press "t" for hit box test.',
		'Press "y" profile a variety of methods.',
		'Press "u" profile game.run().',
		'Press "h" Display help info.',
		'Press "k" to display the galaxy node info menu.',
		'Press "o" to display the galaxy node travel menu.']
		#Then draw the contents of the menu
		self.addTextToMainPanel(help, left+50, 50+top)


	def setEndMinigamePanel(self, text):
		#First kick player back to infinite space but don't update all the nodes:
		globalvars.scenario_manager.goToInfiniteSpace(globalvars.player.nodeid, update=False)
		#Next set the menu displaying the results of the minigame.
		self.setStandardMenu()
		self.addTextToMainPanel(text, left+50, topbuffer+top)
		#Draw the panel and sleep a brief time so that the user does not accidentally
		#close the menu while furiously clicking. This happened to me a few times.
		self.main_panel.draw()
		pygame.display.flip()
		pygame.time.wait(1000) #Wait this many milliseconds


	def addWeaponSubpanel(self, x_val, y_val, localwidth, localheight, framethickness, textbuffer, weapon, method, argument=None, equip=False):
		self.addMenuItem(x1=(left+x_val),\
			y1=(top+y_val),\
			width=localwidth,\
			height=localheight,\
			string=weapon.name,\
			textbuffer=textbuffer, text_color=colors.blue,\
			framed=True, frame_thickness=framethickness)
		#Add option to equip or unequip weapon
		string = 'Equip'
		if not equip:
			string = 'Unequip'
		self.addMenuItem(x1=(left+x_val+textbuffer),\
				y1=(top+y_val+font_size+textbuffer),\
				string=string, method=method, argument=argument)
		#Add option to view information on weapon
		self.addMenuItem(x1=(left+x_val+textbuffer),\
				y1=(top+y_val+font_size*2+textbuffer),\
				string='View stats', method=globalvars.menu.setWeaponViewPanel,\
				argument=weapon)


	def setShipPanel(self):
		self.setStandardMenu()
		temp = drawable.DrawableImage(x1=left+230, y1=300+top,\
									  image='shipoutline')
		self.main_panel.addDrawable(temp)
		textbuffer = 8
		localtopbuffer = 50
		leftoffset = 500
		localheight = 70
		localwidth = 200
		framethickness = 2
		#Draw the currently equipped weapon if any
		if not globalvars.player.gun is None:
			x_val = 200
			y_val = 80
			self.addWeaponSubpanel(x_val, y_val, localwidth, localheight,\
				framethickness, textbuffer, globalvars.player.gun,\
				unequipPlayerGun)
		#Draw the currently equipped missile if any
		if not globalvars.player.missile is None:
			x_val = 100
			y_val = 180
			self.addWeaponSubpanel(x_val, y_val, localwidth, localheight,\
				framethickness, textbuffer, globalvars.player.missile,\
				unequipPlayerMissile)
		#Draw the currently equipped mine if any
		if not globalvars.player.mine is None:
			x_val = 100
			y_val = 380
			self.addWeaponSubpanel(x_val, y_val, localwidth, localheight,\
				framethickness, textbuffer, globalvars.player.mine,\
				unequipPlayerMine)
		#Draw the currently equipped engine if any
		if not globalvars.player.engine is None:
			x_val = 200
			y_val = 420
			self.addWeaponSubpanel(x_val, y_val, localwidth, localheight,\
				framethickness, textbuffer, globalvars.player.engine,\
				unequipPlayerEngine)

		#Find out what's in the cargo hold
		gun_count = 0
		missile_count = 0
		mine_count = 0
		ship_count = 0
		engine_count = 0
		for c in globalvars.player.cargo:
			#I have no idea why this continue line is needed, but I get an
			#AttributeError: 'NoneType' object has no attribute 'is_a'
			#when I unequip an engine and then reequip one without this line.
			if c is None: continue
			if c.is_a == 'gun':
				gun_count += 1
			elif c.is_a == globalvars.SHIP:
				ship_count += 1
			elif c.is_a == 'engine':
				engine_count += 1
			elif c.is_a == 'missile':
				missile_count += 1
			elif c.is_a == 'mine':
				mine_count += 1

		fontsize = 32
		ystart = 150
		yinterval = 100
		xstart = 500

		string = '0 guns in cargo hold.'
		method = None
		if gun_count > 0:
			string = 'Weapon Compare ('+str(gun_count)+' in cargo)'
			method = globalvars.menu.setWeaponComparePanel
		self.addMenuItem(x1=xstart, y1=ystart, string=string,\
			   local_font_size=fontsize, method=method, argument=0)
		ystart += yinterval

		string = '0 missile launchers in cargo hold.'
		method = None
		if missile_count > 0:
			string = 'Missile Compare ('+str(missile_count)+' in cargo)'
			method = globalvars.menu.setMissileComparePanel
		self.addMenuItem(x1=xstart, y1=ystart, string=string,\
			   local_font_size=fontsize, method=method, argument=0)
		ystart += yinterval

		string = '0 mine layers in cargo hold.'
		method = None
		if mine_count > 0:
			string = 'Mine Compare ('+str(mine_count)+' in cargo)'
			method = globalvars.menu.setMineComparePanel
		self.addMenuItem(x1=xstart, y1=ystart, string=string,\
			   local_font_size=fontsize, method=method, argument=0)
		ystart += yinterval

		string = '0 ships available.'
		method = None
		if mine_count > 0:
			string = 'Ship Compare ('+str(ship_count)+' available)'
			method = globalvars.menu.setShipComparePanel
		self.addMenuItem(x1=xstart, y1=ystart, string=string,\
			   local_font_size=fontsize, method=method, argument=0)
		ystart += yinterval

		string = '0 engines in cargo hold.'
		method = None
		if mine_count > 0:
			string = 'Engine Compare ('+str(mine_count)+' in cargo)'
			method = globalvars.menu.setEngineComparePanel
		self.addMenuItem(x1=xstart, y1=ystart, string=string,\
			   local_font_size=fontsize, method=method, argument=0)
		ystart += yinterval


	def setWeaponViewPanel(self, weapon):
		self.setStandardMenu()
		#Then draw the contents of the menu
		text = weapon.toStringArray()
		self.addTextToMainPanel(text, left+50, topbuffer+top)


	def setWeaponComparePanel(self, index):
		'''Pre: index is a valid index into globalvars.player.cargo
		and index indexes an object of type Weapon.
		Post: displays a panel comparing the currently equipped weapon with
		the indexed weapon. Also provides options to view next or previous 
		weapon in the cargo hold.
		Also gives option to replace currently equipped gun with indexed gun.'''
		local_font_size = 32
		self.setStandardMenu()
		#Equipped gun (if any)
		equipped_gun_column = None
		equipped_gun_comparator = None
		if globalvars.player.gun is None:
			equipped_gun_column = ['None equipped','','','','','','','']
			equipped_gun_comparator = [0.0 for _ in range(8)]
		else:
			equipped_gun_column = [globalvars.player.gun.name,
						globalvars.player.gun.getWeaponClassName(),
						globalvars.player.gun.getWeaponType(),
						str(globalvars.player.gun.refire_rate),
						str(globalvars.player.gun.bullet_speed),
						str(globalvars.player.gun.damage),
						str(globalvars.player.gun.weapon_range),
						str(globalvars.player.gun.bullet_num)]
			equipped_gun_comparator = [0,
						globalvars.player.gun.getWeaponClass(),
						0,
						globalvars.player.gun.refire_rate,
						globalvars.player.gun.bullet_speed,
						globalvars.player.gun.damage,
						globalvars.player.gun.weapon_range,
						globalvars.player.gun.bullet_num]
		#error check the cargo hold
		cargo_gun_column = None
		cargo_gun_comparator = None
		if len(globalvars.player.cargo) == 0:
			cargo_gun_column = ['There are no guns in','your cargo hold.','','','','','','']
			cargo_gun_comparator = [0.0 for _ in range(8)]
		else:
			if index < 0 or index >= len(globalvars.player.cargo):
				index = 0
			if globalvars.player.cargo[index].is_a != 'gun':
				for i in range(len(globalvars.player.cargo)):
					if globalvars.player.cargo[i].is_a == 'gun':
						index = i
						break
			if globalvars.player.cargo[index].is_a != 'gun':
				cargo_gun_column = ['There are no guns in','your cargo hold.','','','','','','']
				cargo_gun_comparator = [0.0 for _ in range(8)]
			else:
				cargo_gun_column = [globalvars.player.cargo[index].name,
						globalvars.player.cargo[index].getWeaponClassName(),
						globalvars.player.cargo[index].getWeaponType(),
						str(globalvars.player.cargo[index].refire_rate),
						str(globalvars.player.cargo[index].bullet_speed),
						str(globalvars.player.cargo[index].damage),
						str(globalvars.player.cargo[index].weapon_range),
						str(globalvars.player.cargo[index].bullet_num)]
				cargo_gun_comparator = [0,
						globalvars.player.cargo[index].getWeaponClass(),
						0,
						globalvars.player.cargo[index].refire_rate,
						globalvars.player.cargo[index].bullet_speed,
						globalvars.player.cargo[index].damage,
						globalvars.player.cargo[index].weapon_range,
						globalvars.player.cargo[index].bullet_num]
		i = 0
		column1_offset = 5
		column2_offset = 175
		column3_offset = 500
		#The last two values for refire rate are reversed since smaller refire rate is better.
		comparison_array = [
			['','EQUIPPED','CARGO',0,0],
			['',equipped_gun_column[0],cargo_gun_column[0],
				equipped_gun_comparator[0],cargo_gun_comparator[0]],
			['','','',0,0],
			['Class:',equipped_gun_column[1],cargo_gun_column[1],
				equipped_gun_comparator[1],cargo_gun_comparator[1]],
			['Type:',equipped_gun_column[2],cargo_gun_column[2],
				equipped_gun_comparator[2],cargo_gun_comparator[2]],
			['Refire rate:',equipped_gun_column[3],cargo_gun_column[3],
				cargo_gun_comparator[3],equipped_gun_comparator[3]],
			['Velocity:',equipped_gun_column[4],cargo_gun_column[4],
				equipped_gun_comparator[4],cargo_gun_comparator[4]],
			['Damage:',equipped_gun_column[5],cargo_gun_column[5],
				equipped_gun_comparator[5],cargo_gun_comparator[5]],
			['Range:',equipped_gun_column[6],cargo_gun_column[6],
				equipped_gun_comparator[6],cargo_gun_comparator[6]],
			['Projectiles:',equipped_gun_column[7],cargo_gun_column[7],
				equipped_gun_comparator[7],cargo_gun_comparator[7]]
		]
		#Fix too long names
		part1, part2 = splitTooLongWord(word_to_split=equipped_gun_column[0],\
			length_limit=20)
		comparison_array[1][1] = part1
		comparison_array[2][1] = part2
		part1, part2 = splitTooLongWord(word_to_split=cargo_gun_column[0],\
			length_limit=20)
		comparison_array[1][2] = part1
		comparison_array[2][2] = part2
		#Draw comparison array on screen
		i = self.processComparisonArray(comparison_array, i, local_font_size, column1_offset, column2_offset, column3_offset)
		#Reset color scheme
		equipped_color = colors.white
		cargo_color = colors.white
		#Give player option to equip currently selected weapon in cargo
		i += 1
		self.equipCurrentCargo(index, i, 'gun', local_font_size, column3_offset, cargo_color, equipPlayerWeapon)
		i += 2
		self.previousAndNextInCargo(i, index, 'gun', local_font_size, column2_offset, column3_offset, globalvars.menu.setWeaponComparePanel)


	def setShipComparePanel(self, index):
		'''Pre: index is a valid index into globalvars.player.cargo
		and index indexes an object of type ship.
		Post: displays a panel comparing the current ship with
		the indexed ship. Also provides options to view next or previous 
		ship in the cargo hold.
		Also gives option to replace current ship with indexed ship.'''
		local_font_size = 32
		self.setStandardMenu()
		#Current ship
		equipped_ship_column = [globalvars.player.name,
					globalvars.player.getShipClassName(),
					str(globalvars.player.maxhealth),
					str(globalvars.player.fuel_capacity),
					str(globalvars.player.cargospace_max)]
		equipped_ship_comparator = [0,
					0,
					globalvars.player.maxhealth,
					globalvars.player.fuel_capacity,
					globalvars.player.cargospace_max]
		#error check the cargo hold
		cargo_ship_column = None
		cargo_ship_comparator = None
		if len(globalvars.player.cargo) == 0:
			cargo_ship_column = ['There are no ships in','your cargo hold.','','','']
			cargo_ship_comparator = [0.0 for _ in range(5)]
		else:
			if index < 0 or index >= len(globalvars.player.cargo):
				index = 0
			if globalvars.player.cargo[index].is_a != globalvars.SHIP:
				for i in range(len(globalvars.player.cargo)):
					if globalvars.player.cargo[i].is_a == globalvars.SHIP:
						index = i
						break
			if globalvars.player.cargo[index].is_a != globalvars.SHIP:
				cargo_ship_column = ['There are no ships in','your cargo hold.','','','']
				cargo_ship_comparator = [0.0 for _ in range(5)]
			else:
				cargo_ship_column = [globalvars.player.cargo[index].name,
						globalvars.player.cargo[index].getShipClassName(),
						str(globalvars.player.cargo[index].maxhealth),
						str(globalvars.player.cargo[index].fuel_capacity),
						str(globalvars.player.cargo[index].cargospace_max)]
				cargo_ship_comparator = [0,
						0,
						globalvars.player.cargo[index].maxhealth,
						globalvars.player.cargo[index].fuel_capacity,
						globalvars.player.cargo[index].cargospace_max]
		i = 0
		column1_offset = 5
		column2_offset = 175
		column3_offset = 450
		#The last two values for refire rate are reversed since smaller refire rate is better.
		comparison_array = [
			['','CURRENT SHIP','ALTERNATE SHIP',0,0],
			['',equipped_ship_column[0],cargo_ship_column[0],
				equipped_ship_comparator[0],cargo_ship_comparator[0]],
			['','','',0,0],
			['Class:',equipped_ship_column[1],cargo_ship_column[1],
				equipped_ship_comparator[1],cargo_ship_comparator[1]],
			['Hit points:',equipped_ship_column[2],cargo_ship_column[2],
				equipped_ship_comparator[2],cargo_ship_comparator[2]],
			['Fuel capacity:',equipped_ship_column[3],cargo_ship_column[3],
				cargo_ship_comparator[3],equipped_ship_comparator[3]],
			['Cargo space:',equipped_ship_column[4],cargo_ship_column[4],
				equipped_ship_comparator[4],cargo_ship_comparator[4]]
		]
		#Fix too long names
		part1, part2 = splitTooLongWord(word_to_split=equipped_ship_column[0],\
			length_limit=20)
		comparison_array[1][1] = part1
		comparison_array[2][1] = part2
		part1, part2 = splitTooLongWord(word_to_split=cargo_ship_column[0],\
			length_limit=20)
		comparison_array[1][2] = part1
		comparison_array[2][2] = part2
		#Draw comparison array on screen
		i = self.processComparisonArray(comparison_array, i, local_font_size, column1_offset, column2_offset, column3_offset)
		#Reset color scheme
		equipped_color = colors.white
		cargo_color = colors.white
		#Give player option to equip currently selected ship in cargo
		i += 1
		if globalvars.player.cargo[index].is_a == globalvars.SHIP:
			subpanel = Panel()
			temp = drawable.Text(x1=left+column3_offset,\
				y1=local_font_size*i+topbuffer+top,\
				string='Replace current with this ship',\
				font_size=local_font_size, color=cargo_color)
			subpanel.addDrawable(temp)
			subpanel.setMethod(equipPlayerShip)
			subpanel.argument = index
			self.main_panel.addPanel(subpanel)
		i += 2
		self.previousAndNextInCargo(i, index, globalvars.SHIP, local_font_size, column2_offset, column3_offset, globalvars.menu.setShipComparePanel)


	def setMineComparePanel(self, index):
		'''Pre: index is a valid index into globalvars.player.cargo
		and index indexes an object of type mine.
		Post: displays a panel comparing the current mine with
		the indexed mine. Also provides options to view next or previous 
		mine in the cargo hold.
		Also gives option to replace current mine with indexed mine.'''
		local_font_size = 32
		self.setStandardMenu()
		#Equipped mine (if any)
		equipped_mine_column = None
		equipped_mine_comparator = None
		if globalvars.player.mine is None:
			equipped_mine_column = ['None equipped','','','','','','','']
			equipped_mine_comparator = [0.0 for _ in range(8)]
		else:
			equipped_mine_column = [globalvars.player.mine.name,
						globalvars.player.mine.getMineClassName(),
						str(globalvars.player.mine.refire_rate),
						str(globalvars.player.mine.damage),
						str(globalvars.player.mine.longevity),
						'',
						'',
						'']
			equipped_mine_comparator = [0,
						globalvars.player.mine.getMineClass(),
						globalvars.player.mine.refire_rate,
						globalvars.player.mine.damage,
						globalvars.player.mine.longevity,
						0,
						0,
						0]
		#error check the cargo hold
		cargo_mine_column = None
		cargo_mine_comparator = None
		if len(globalvars.player.cargo) == 0:
			cargo_mine_column = ['There are no mines in','your cargo hold.','','','','','','']
			cargo_mine_comparator = [0.0 for _ in range(8)]
		else:
			if index < 0 or index >= len(globalvars.player.cargo):
				index = 0
			if globalvars.player.cargo[index].is_a != 'mine':
				for i in range(len(globalvars.player.cargo)):
					if globalvars.player.cargo[i].is_a == 'mine':
						index = i
						break
			if globalvars.player.cargo[index].is_a != 'mine':
				cargo_mine_column = ['There are no mines in','your cargo hold.','','','','','','']
				cargo_mine_comparator = [0.0 for _ in range(8)]
			else:
				cargo_mine_column = [globalvars.player.cargo[index].name,
						globalvars.player.cargo[index].getMineClassName(),
						str(globalvars.player.cargo[index].refire_rate),
						str(globalvars.player.cargo[index].damage),
						str(globalvars.player.cargo[index].longevity),
						'',
						'',
						'']
				cargo_mine_comparator = [0,
						globalvars.player.cargo[index].getMineClass(),
						globalvars.player.cargo[index].refire_rate,
						globalvars.player.cargo[index].damage,
						globalvars.player.cargo[index].longevity,
						0,
						0,
						0]
		i = 0
		column1_offset = 5
		column2_offset = 175
		column3_offset = 500
		#The last two values for refire rate are reversed since smaller refire rate is better.
		comparison_array = [
			['','EQUIPPED','CARGO',0,0],
			['',equipped_mine_column[0],cargo_mine_column[0],
				equipped_mine_comparator[0],cargo_mine_comparator[0]],
			['','','',0,0],
			['Class:',equipped_mine_column[1],cargo_mine_column[1],
				equipped_mine_comparator[1],cargo_mine_comparator[1]],
			['Refire rate:',equipped_mine_column[2],cargo_mine_column[2],
				cargo_mine_comparator[2],equipped_mine_comparator[2]],
			['Damage:',equipped_mine_column[3],cargo_mine_column[3],
				equipped_mine_comparator[3],cargo_mine_comparator[3]],
			['Longevity:',equipped_mine_column[4],cargo_mine_column[4],
				equipped_mine_comparator[4],cargo_mine_comparator[4]],
			['Ammo:',equipped_mine_column[5],cargo_mine_column[5],
				equipped_mine_comparator[5],cargo_mine_comparator[5]],
			['Blast:',equipped_mine_column[6],cargo_mine_column[6],
				equipped_mine_comparator[6],cargo_mine_comparator[6]],
			['Radius:',equipped_mine_column[7],cargo_mine_column[7],
				equipped_mine_comparator[7],cargo_mine_comparator[7]]
		]
		#Fix too long names
		part1, part2 = splitTooLongWord(word_to_split=equipped_mine_column[0],\
			length_limit=20)
		comparison_array[1][1] = part1
		comparison_array[2][1] = part2
		part1, part2 = splitTooLongWord(word_to_split=cargo_mine_column[0],\
			length_limit=20)
		comparison_array[1][2] = part1
		comparison_array[2][2] = part2
		#Draw comparison array on screen
		i = self.processComparisonArray(comparison_array, i, local_font_size, column1_offset, column2_offset, column3_offset)
		#Reset color scheme
		equipped_color = colors.white
		cargo_color = colors.white
		#Give player option to equip currently selected mine in cargo
		i += 1
		self.equipCurrentCargo(index, i, 'mine', local_font_size, column3_offset, cargo_color, equipPlayerWeapon)
		i += 1
		self.previousAndNextInCargo(i, index, 'mine', local_font_size, column2_offset, column3_offset, globalvars.menu.setMineComparePanel)


	def setMissileComparePanel(self, index):
		'''Pre: index is a valid index into globalvars.player.cargo
		and index indexes an object of type missile.
		Post: displays a panel comparing the current missile with
		the indexed missile. Also provides options to view next or previous 
		missile in the cargo hold.
		Also gives option to replace current missile with indexed missile.'''
		local_font_size = 32
		self.setStandardMenu()
		#Equipped missile (if any)
		equipped_missile_column = None
		equipped_missile_comparator = None
		if globalvars.player.missile is None:
			equipped_missile_column = ['None equipped','','','','','','','','','','']
			equipped_missile_comparator = [0.0 for _ in range(11)]
		else:
			equipped_missile_column = [globalvars.player.missile.name,
						globalvars.player.missile.getMissileClassName(),
						str(globalvars.player.missile.refire_rate),
						str(globalvars.player.missile.speed),
						str(globalvars.player.missile.damage),
						str(globalvars.player.missile.longevity),
						str(globalvars.player.missile.turn_rate),
						'',
						'',
						'',
						'']
			equipped_missile_comparator = [0,
						globalvars.player.missile.getMissileClass(),
						globalvars.player.missile.refire_rate,
						globalvars.player.missile.speed,
						globalvars.player.missile.damage,
						globalvars.player.missile.longevity,
						globalvars.player.missile.turn_rate,
						0,
						0,
						0,
						0]
		#error check the cargo hold
		cargo_missile_column = None
		cargo_missile_comparator = None
		if len(globalvars.player.cargo) == 0:
			cargo_missile_column = ['There are no missiles in','your cargo hold.','','','','','','','','','']
			cargo_missile_comparator = [0.0 for _ in range(11)]
		else:
			if index < 0 or index >= len(globalvars.player.cargo):
				index = 0
			if globalvars.player.cargo[index].is_a != 'missile':
				for i in range(len(globalvars.player.cargo)):
					if globalvars.player.cargo[i].is_a == 'missile':
						index = i
						break
			if globalvars.player.cargo[index].is_a != 'missile':
				cargo_missile_column = ['There are no missiles in','your cargo hold.','','','','','','','','','']
				cargo_missile_comparator = [0.0 for _ in range(11)]
			else:
				cargo_missile_column = [globalvars.player.cargo[index].name,
						globalvars.player.cargo[index].getMissileClassName(),
						str(globalvars.player.cargo[index].refire_rate),
						str(globalvars.player.cargo[index].speed),
						str(globalvars.player.cargo[index].damage),
						str(globalvars.player.cargo[index].longevity),
						str(globalvars.player.cargo[index].turn_rate),
						'',
						'',
						'',
						'']
				cargo_missile_comparator = [0,
						globalvars.player.cargo[index].getMissileClass(),
						globalvars.player.cargo[index].refire_rate,
						globalvars.player.cargo[index].speed,
						globalvars.player.cargo[index].damage,
						globalvars.player.cargo[index].longevity,
						globalvars.player.cargo[index].turn_rate,
						0,
						0,
						0,
						0]
		i = 0
		column1_offset = 5
		column2_offset = 175
		column3_offset = 500
		#The last two values for refire rate are reversed since smaller refire rate is better.
		comparison_array = [
			['','EQUIPPED','CARGO',0,0],
			['',equipped_missile_column[0],cargo_missile_column[0],
				equipped_missile_comparator[0],cargo_missile_comparator[0]],
			['','','',0,0],
			['Class:',equipped_missile_column[1],cargo_missile_column[1],
				equipped_missile_comparator[1],cargo_missile_comparator[1]],
			['Refire rate:',equipped_missile_column[2],cargo_missile_column[2],
				cargo_missile_comparator[2],equipped_missile_comparator[2]],
			['Velocity:',equipped_missile_column[3],cargo_missile_column[3],
				equipped_missile_comparator[3],cargo_missile_comparator[3]],
			['Damage:',equipped_missile_column[4],cargo_missile_column[4],
				equipped_missile_comparator[4],cargo_missile_comparator[4]],
			['Longevity:',equipped_missile_column[5],cargo_missile_column[5],
				equipped_missile_comparator[5],cargo_missile_comparator[5]],
			['Turn rate:',equipped_missile_column[6],cargo_missile_column[6],
				equipped_missile_comparator[6],cargo_missile_comparator[6]],
			['Ammo:',equipped_missile_column[7],cargo_missile_column[7],
				equipped_missile_comparator[7],cargo_missile_comparator[7]],
			['Blast:',equipped_missile_column[8],cargo_missile_column[8],
				equipped_missile_comparator[8],cargo_missile_comparator[8]],
			['Radius:',equipped_missile_column[9],cargo_missile_column[9],
				equipped_missile_comparator[9],cargo_missile_comparator[9]],
			['Seeking:',equipped_missile_column[10],cargo_missile_column[10],
				equipped_missile_comparator[10],cargo_missile_comparator[10]]
		]
		#Fix too long names
		part1, part2 = splitTooLongWord(word_to_split=equipped_missile_column[0],\
			length_limit=20)
		comparison_array[1][1] = part1
		comparison_array[2][1] = part2
		part1, part2 = splitTooLongWord(word_to_split=cargo_missile_column[0],\
			length_limit=20)
		comparison_array[1][2] = part1
		comparison_array[2][2] = part2
		#Draw comparison array on screen
		i = self.processComparisonArray(comparison_array, i, local_font_size, column1_offset, column2_offset, column3_offset)
		#Reset color scheme
		equipped_color = colors.white
		cargo_color = colors.white
		#Give player option to equip currently selected missile in cargo
		i += 1
		self.equipCurrentCargo(index, i, 'missile', local_font_size, column3_offset, cargo_color, equipPlayerWeapon)
		i += 1
		self.previousAndNextInCargo(i, index, 'missile', local_font_size, column2_offset, column3_offset, globalvars.menu.setMissileComparePanel)


	def setEngineComparePanel(self, index):
		'''Pre: index is a valid index into globalvars.player.cargo
		and index indexes an object of type engine.
		Post: displays a panel comparing the currently equipped engine with
		the indexed engine. Also provides options to view next or previous 
		engine in the cargo hold.
		Also gives option to replace currently equipped engine with indexed engine.'''
		local_font_size = 32
		self.setStandardMenu()
		#Equipped engine (if any)
		equipped_engine_column = None
		equipped_engine_comparator = None
		if globalvars.player.engine is None:
			equipped_engine_column = ['None equipped','','','','','','']
			equipped_engine_comparator = [0.0 for _ in range(7)]
		else:
			equipped_engine_column = [globalvars.player.engine.name,
						globalvars.player.engine.getEngineClassName(),
						str(globalvars.player.engine.maxSpeed),
						str(globalvars.player.engine.dv),
						str(globalvars.player.engine.dtheta),
						str(globalvars.player.engine.turnRateDecay),
						str(globalvars.player.engine.fuel_consumption)]
			equipped_engine_comparator = [0,
						globalvars.player.engine.getEngineClass(),
						globalvars.player.engine.maxSpeed,
						globalvars.player.engine.dv,
						globalvars.player.engine.dtheta,
						globalvars.player.engine.turnRateDecay,
						globalvars.player.engine.fuel_consumption]
		#error check the cargo hold
		cargo_engine_column = None
		cargo_engine_comparator = None
		if len(globalvars.player.cargo) == 0:
			cargo_engine_column = ['There are no engines in','your cargo hold.','','','','','']
			cargo_engine_comparator = [0.0 for _ in range(7)]
		else:
			if index < 0 or index >= len(globalvars.player.cargo):
				index = 0
			if globalvars.player.cargo[index].is_a != 'engine':
				for i in range(len(globalvars.player.cargo)):
					if globalvars.player.cargo[i].is_a == 'engine':
						index = i
						break
			if globalvars.player.cargo[index].is_a != 'engine':
				cargo_engine_column = ['There are no engines in','your cargo hold.','','','','','']
				cargo_engine_comparator = [0.0 for _ in range(7)]
			else:
				cargo_engine_column = [globalvars.player.cargo[index].name,
						globalvars.player.cargo[index].getEngineClassName(),
						str(globalvars.player.cargo[index].maxSpeed),
						str(globalvars.player.cargo[index].dv),
						str(globalvars.player.cargo[index].dtheta),
						str(globalvars.player.cargo[index].turnRateDecay),
						str(globalvars.player.cargo[index].fuel_consumption)]
				cargo_engine_comparator = [0,
						globalvars.player.cargo[index].getEngineClass(),
						globalvars.player.cargo[index].maxSpeed,
						globalvars.player.cargo[index].dv,
						globalvars.player.cargo[index].dtheta,
						globalvars.player.cargo[index].turnRateDecay,
						globalvars.player.cargo[index].fuel_consumption]
		i = 0
		column1_offset = 5
		column2_offset = 210
		column3_offset = 510
		comparison_array = [
			#Last two turn rate decay and fuel consumption values are reversed since lower is better.
			['','EQUIPPED','CARGO',0,0],
			['',equipped_engine_column[0],cargo_engine_column[0],
				equipped_engine_comparator[0],cargo_engine_comparator[0]],
			['','','',0,0],
			['Class:',equipped_engine_column[1],cargo_engine_column[1],
				equipped_engine_comparator[1],cargo_engine_comparator[1]],
			['Top speed:',equipped_engine_column[2],cargo_engine_column[2],
				equipped_engine_comparator[2],cargo_engine_comparator[2]],
			['Acceleration:',equipped_engine_column[3],cargo_engine_column[3],
				equipped_engine_comparator[3],cargo_engine_comparator[3]],
			['Turn rate:',equipped_engine_column[4],cargo_engine_column[4],
				equipped_engine_comparator[4],cargo_engine_comparator[4]],
			['Turn rate decay:',equipped_engine_column[5],cargo_engine_column[5],
				cargo_engine_comparator[5],equipped_engine_comparator[5]],
			['Fuel Consumption:',equipped_engine_column[6],cargo_engine_column[6],
				cargo_engine_comparator[6],equipped_engine_comparator[6]]
		]
		#Fix too long names
		part1, part2 = splitTooLongWord(word_to_split=equipped_engine_column[0],\
			length_limit=20)
		comparison_array[1][1] = part1
		comparison_array[2][1] = part2
		part1, part2 = splitTooLongWord(word_to_split=cargo_engine_column[0],\
			length_limit=20)
		comparison_array[1][2] = part1
		comparison_array[2][2] = part2
		#Draw comparison array on screen
		i = self.processComparisonArray(comparison_array, i, local_font_size, column1_offset, column2_offset, column3_offset)
		#Reset color scheme
		equipped_color = colors.white
		cargo_color = colors.white
		#Give player option to equip currently selected engine in cargo
		i += 1
		self.equipCurrentCargo(index, i, 'engine', local_font_size, column3_offset, cargo_color, equipPlayerEngine)
		i += 2
		self.previousAndNextInCargo(i, index, 'engine', local_font_size, column2_offset, column3_offset, globalvars.menu.setEngineComparePanel)


	def processComparisonArray(self, comparison_array, i, local_font_size, column1_offset, column2_offset, column3_offset):
		for row in comparison_array:
			equipped_color = colors.white
			cargo_color = colors.white
			equipped_val = row[3]
			cargo_val = row[4]
			if equipped_val != cargo_val:
				if equipped_val > cargo_val:
					equipped_color = colors.green
					cargo_color = colors.red
				else:
					equipped_color = colors.red
					cargo_color = colors.green
			temp = drawable.Text(x1=left+column1_offset,\
				y1=local_font_size*i+topbuffer+top,\
				string=row[0],\
				font_size=local_font_size, color=colors.white)
			self.main_panel.addDrawable(temp)
			temp = drawable.Text(x1=left+column2_offset,\
				y1=local_font_size*i+topbuffer+top,\
				string=row[1],\
				font_size=local_font_size, color=equipped_color)
			self.main_panel.addDrawable(temp)
			temp = drawable.Text(x1=left+column3_offset,\
				y1=local_font_size*i+topbuffer+top,\
				string=row[2],\
				font_size=local_font_size, color=cargo_color)
			self.main_panel.addDrawable(temp)
			i += 1
		return i


	def equipCurrentCargo(self, index, i, cargo_type, local_font_size, column3_offset, cargo_color, method):
		if len(globalvars.player.cargo) > index\
		and globalvars.player.cargo[index].is_a == cargo_type:
			self.addMenuItem(x1=left+column3_offset,\
				y1=local_font_size*i+topbuffer+top,\
				string='Equip',\
				local_font_size=local_font_size, text_color=cargo_color,\
				method=method, argument=index)


	def previousAndNextInCargo(self, i, index, cargo_type, local_font_size,\
	column2_offset, column3_offset, method):
		#Find previous cargo_type in cargo to examine.
		previous = index
		for _ in range(len(globalvars.player.cargo)-1):
			previous -= 1
			if previous < 0: previous = len(globalvars.player.cargo)-1
			if globalvars.player.cargo[previous].is_a == cargo_type:
				self.addMenuItem(x1=left+column2_offset,\
					y1=local_font_size*i+topbuffer+top,\
					string='Previous', local_font_size=local_font_size,\
					method=method, argument=previous)
				break
		#Find next cargo_type in cargo to examine.
		next = index
		for _ in range(len(globalvars.player.cargo)-1):
			next = (next+1) % len(globalvars.player.cargo)
			if globalvars.player.cargo[next].is_a == cargo_type:
				self.addMenuItem(x1=left+column3_offset,\
					y1=local_font_size*i+topbuffer+top,\
					string='Next', local_font_size=local_font_size,\
					method=method, argument=next)
				break


	def setOpportunityPanel(self, opportunity):
		self.setStandardMenu(tabs=False)
		text = ['Faction: '+opportunity.actor.name+' is taking action ',
		'"'+opportunity.action+'"',
		'on your node.']
		self.addTextToMainPanel(text, left+50, topbuffer+top)

