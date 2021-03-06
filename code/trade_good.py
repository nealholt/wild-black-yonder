import globalvars

class TradeGood():
	def __init__(self, amount=0, unit_price=0, name=''):
		self.amount = amount
		self.unit_price = float(unit_price)
		self.value = self.unit_price * float(self.amount)
		self.name=name
		self.is_a = globalvars.TRADEGOOD

	def add(self, amount, unit_price):
		#Update value
		self.value = float(unit_price) * float(amount) + self.unit_price * float(self.amount)
		#Update amount
		self.amount += amount
		#Update unit price
		self.unit_price = self.value / float(self.amount)

	def remove(self, amount):
		#Update amount
		self.amount -= amount
		#Update value
		self.value = self.unit_price * float(self.amount)

	def getUnitPrice(self):
		return int(self.unit_price)

	def getProfit(self, comparison_unit_price):
		per_unit_profit = self.unit_price - float(comparison_unit_price)
		percent_profit = 100.0 * ((float(comparison_unit_price) / self.unit_price) - 1.0)
		return per_unit_profit, percent_profit

