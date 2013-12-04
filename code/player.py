from ship import *
from displayUtilities import TemporaryText
import random as rd
import trade_good

class Player(Ship):
	def __init__(self, image_name):
		Ship.__init__(self,image_name=image_name)

		self.setProfile()

		self.health=300
		self.maxhealth=300

		self.rect.centerx = -100.
		self.rect.centery = -100.

		self.parkAtDestination = False

		self.destination = None

		self.isPlayer = True

		#Track the most recent fuel alert level to avoid giving multiple warnings.
		self.fuelAlertLevel = 4

		#Node location of the player.
		self.nodeid = 0
		self.destinationNode = [0]

		#Give some trade goods to the player.
		self.trade_goods = []
		self.trade_goods.append(trade_good.TradeGood(amount=10, unit_price=50, name='Niblets'))

		#For testing purposes, load all the weapons except the initially equipped 
		#weapon into the player's cargo hold.
		#Load hitBoxTester
		self.cargo.append(weapon.HitBoxTesterGun(self))
		#Load 4 randomly generated mines
		for _ in range(4):
			temp = mine.generateMine(5)
			temp.shooter = self
			self.cargo.append(temp)
		#Load 4 randomly generated missiles
		for _ in range(4):
			temp = missile.generateMissile(rd.randint(0, len(missile.missile_class_names)-1))
			temp.shooter = self
			self.cargo.append(temp)
		#Load 4 more randomly generated guns
		for _ in range(4):
			temp = weapon.generateWeapon(rd.randint(0, len(weapon.weapon_class_names)-1))
			temp.shooter = self
			self.cargo.append(temp)
		#Load 3 more randomly generated engines
		for _ in range(3):
			temp = engine.generateEngine(rd.randint(0, len(engine.engine_class_names)-1))
			self.cargo.append(temp)
		#Load 3 more randomly generated ships
		for _ in range(3):
			temp = generateShip(rd.randint(0, len(ship_class_names)-1))
			self.cargo.append(temp)
		self.initialize()


	def equipShipFromCargo(self, cargo_index):
		#Error checking
		if cargo_index >= len(self.cargo):
			print 'ERROR: cargo_index '+str(cargo_index)+' is outside the cargo array.'
			exit()
		if not self.cargo[cargo_index].is_a == globalvars.SHIP:
			print 'ERROR: cargo indexed by '+str(cargo_index)+' is not a ship.'
			exit()
		#Create a new ship identical to the current ship.
		#todo_testing = 'inventory before '
		#for c in self.cargo:
		#	if c.is_a == globalvars.SHIP:
		#		todo_testing += c.getShipName()+'-'+c.name+', '
		#print todo_testing
		copy_of_current = Ship()
		copy_of_current.makeSelfCopyOfOther(self)
		#Change the current ship to be exactly like the ship in cargo.
		self.makeSelfCopyOfOther(self.cargo[cargo_index])
		#Remove the ship from the cargo hold.
		self.cargo.pop(cargo_index)
		#Put the new ship (a copy of the previous ship) in the cargo hold.
		self.cargo.append(copy_of_current)
		#todo_testing = 'inventory after '
		#for c in self.cargo:
		#	if c.is_a == globalvars.SHIP:
		#		todo_testing += c.getShipName()+'-'+c.name+', '
		#print todo_testing
		#The following is needed because the ships generated in cargo use the default ship image which is actually a small purple circle with a question mark. At least this way, we don't have to fly that around.
		self.loadNewImage('ship')


	def getTradeGoods(self, name):
		for tg in self.trade_goods:
			if tg.name == name:
				return tg
		return None


	def buyTradeGood(self, name, price):
		#Check to make sure we have enough cargo space
		if self.cargospace < 1:
			print 'ERROR in player.buyTradeGood'; exit()
		#Get any of the trade good already in cargo
		tg = self.getTradeGoods(name)
		if tg is None:
			temp = trade_good.TradeGood(amount=1, unit_price=price, name=name)
			self.trade_goods.append(temp)
		else:
			tg.add(1, price)
		#Subtract the cost from our money
		self.money -= price
		#Reduce the amount of available cargo space
		self.cargospace -= 1


	def sellTradeGood(self, name, price):
		tg = self.getTradeGoods(name)
		if tg is None:
			print 'ERROR in player.sellTradeGood'; exit()
		else:
			tg.remove(1)
		self.money += price
		#Increase the amount of available cargo space
		self.cargospace += 1


	def parkingBrake(self):
		'''Change the truth value of park.'''
		self.parkAtDestination = not self.parkAtDestination


	def update(self):
		'''The player's update function does very little.
		The player uses the special playerUpdate function
		which is needed for when the screen follows or 
		centers on the player.'''
		self.cooldown() #cooldown all the weapons
		#Update my health bar
		self.updateHealthBar()


	def getLeadIndicator(self):
		'''Return the point in space that enemies should shoot 
		at to hit the player when the player is moving.'''
		#return self.rect.center
		return geometry.translate(self.rect.center, self.theta, self.speed*50.0) #The amount to translate depends on player speed, distance from enemy, and bullet speed. There might be a better way to do this.
		#Why when self.rect.center is used does this still not work for the capital ship? Specifically there is a problem when I perch over the upper left corner of the capital ship. It creates a kind-of cool blind spot though. Maybe this is not a problem.


	def playerUpdate(self):
		self.fuel -= self.engine.fuel_consumption
		if self.fuel < 10*globalvars.FPS*self.engine.fuel_consumption and \
		self.fuelAlertLevel > 1:  #10 seconds of fuel remain
			announcement = TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52,
				text='Empty fuel tank imminent! 10 seconds!',
				timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
			globalvars.intangibles_top.add(announcement)
			self.fuelAlertLevel = 1
		elif self.fuel < 30*globalvars.FPS*self.engine.fuel_consumption and \
		self.fuelAlertLevel > 2: #30 seconds of fuel remain
			announcement = TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52,
				text='Fuel critical! 30 seconds of fuel remain.',
				timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
			globalvars.intangibles_top.add(announcement)
			self.fuelAlertLevel = 2
		elif self.fuel < 60*globalvars.FPS*self.engine.fuel_consumption and \
		self.fuelAlertLevel > 3: #60 seconds of fuel remain
			announcement = TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52,
				text='Fuel low! 60 seconds of fuel remain.',
				timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
			globalvars.intangibles_top.add(announcement)
			self.fuelAlertLevel = 3

		if not self.destination is None:
			#Turn towards target
			self.turnTowards()

			if self.parkAtDestination:
				self.park()
			else:
				#Approach target speed
				self.approachSpeed()
		else:
			#Approach target speed
			self.approachSpeed()

		self.move()

