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

		self.initialize()

		#For testing purposes, load all the weapons except the initially equipped 
		#weapon into the player's cargo hold.

		#Load hitBoxTester
		#self.equipToCargo(weapon.HitBoxTesterGun(self))

		#Load one really good item of each type:
		temp = mine.generateMine(len(mine.mine_class_names)-1)
		temp.shooter = self
		self.equipToCargo(temp)
		temp = missile.generateMissile(len(missile.missile_class_names)-1)
		temp.shooter = self
		self.equipToCargo(temp)
		temp = weapon.generateWeapon(len(weapon.weapon_class_names)-1)
		temp.shooter = self
		self.equipToCargo(temp)
		temp = engine.generateEngine(len(engine.engine_class_names)-1)
		self.equipToCargo(temp)
		temp = generateShip(len(ship_class_names)-1)
		self.equipToCargo(temp)
		#Give some trade goods to the player.
		self.trade_goods = []
		self.loadTradeGoods('Niblets', 10, 50.0)


	def equipToCargo(self, item):
		if self.cargospace > 0:
			self.cargo.append(item)
			self.cargospace -= 1
			return True
		else:
			return False


	def equipShipFromCargo(self, cargo_index):
		#Error checking
		if cargo_index >= len(self.cargo):
			print 'ERROR: cargo_index '+str(cargo_index)+' is outside the cargo array.'
			exit()
		if not self.cargo[cargo_index].is_a == globalvars.SHIP:
			print 'ERROR: cargo indexed by '+str(cargo_index)+' is not a ship.'
			exit()
		#Create a new ship identical to the current ship.
		copy_of_current = Ship()
		copy_of_current.makeSelfCopyOfOther(self)
		#Change the current ship to be exactly like the ship in cargo.
		self.makeSelfCopyOfOther(self.cargo[cargo_index])
		#Remove the ship from the cargo hold.
		self.cargo.pop(cargo_index)
		#self still has all its trade goods. make a list of these, remove them, then add them back in so that cargo space will be synced up properly.
		tradegoods = []
		for tg in self.trade_goods:
			tradegoods.append([tg.name, tg.amount, tg.unit_price])
		self.trade_goods = []
		for tg in tradegoods:
			self.loadTradeGoods(tg[0], tg[1], tg[2])
		#Put the new ship (a copy of the previous ship) in the cargo hold.
		self.cargo.append(copy_of_current)
		#The following is needed because the ships generated in cargo use the default ship image which is actually a small purple circle with a question mark. At least this way, we don't have to fly that around.
		self.loadNewImage('ship')
		self.updateImageAngle()
		#Update the health bar
		self.myHealthBar.new_width = (self.health/float(self.maxhealth))*healthBarDefaultWidth


	def getTradeGoods(self, name):
		for tg in self.trade_goods:
			if tg.name == name:
				return tg
		return None


	def loadTradeGoods(self, name, amount, unit_price):
		#Check to make sure we have enough cargo space.
		#If not, just silently fail to load the cargo.
		if self.cargospace < amount:
			amount = self.cargospace
		#Get any of the trade good already in cargo
		tg = self.getTradeGoods(name)
		if tg is None:
			temp = trade_good.TradeGood(amount=amount, unit_price=unit_price, name=name)
			self.trade_goods.append(temp)
		else:
			tg.add(amount, unit_price)
		#Reduce the amount of available cargo space
		self.cargospace -= amount


	def unloadTradeGoods(self, name, amount):
		tg = self.getTradeGoods(name)
		if tg is None:
			print 'ERROR in player.unloadTradeGoods'; exit()
		elif tg.amount >= amount:
			tg.remove(amount)
		else:
			print 'ERROR in player.unloadTradeGoods. Removing more than is ownded.'
			exit()
		#Increase the amount of available cargo space
		self.cargospace += amount


	def buyTradeGood(self, name, price):
		amount = 1
		#Check to make sure we have enough cargo space
		if self.cargospace < amount:
			print 'ERROR in player.buyTradeGood'; exit()
		self.loadTradeGoods(name, amount, price)
		#Subtract the cost from our money
		self.money -= price*amount


	def sellTradeGood(self, name, price):
		amount = 1
		self.unloadTradeGoods(name, amount)
		self.money += price*amount


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

