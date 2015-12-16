
#------------- Some helper classes are defined here--------------------# 

class History:
	def __init__(self, line):		
		values = line.split(',')
		self.user = values[0]
		self.chain = values[1]
		self.offer = values[2]
		self.market = values[3]
		self.repeattrips = values[4]
		self.repeater = values[5]
		self.offerdate = values[6]
		
	@classmethod
	def getHistories(cls,count = 100, filename = 'trainHistory.csv'):

		histories = []
		for e, line in enumerate(open(filename, 'r')):
			if(e == 0):
				continue
			if(e > count):
				break
			histories.append(History(line))
		return histories
	
class JoinedHistory:
	def __init__(self, line):		
		values = line.split(',')
		self.user = values[0]
		self.company = values[1]
		self.category = values[2]
		self.brand = values[3]
		self.chain = values[4]		
		self.market = values[5]
		self.repeattrips = values[6]
		self.repeater = values[7]
		self.offerdate = values[8]
		self.quantity = values[9]
		self.offervalue = values[10]
		
	@classmethod
	def getHistories(cls,count = 100, filename = 'joinedTrainHistory.csv'):

		histories = []
		for e, line in enumerate(open(filename, 'r')):
			if(e == 0):
				continue
			if(e > count):
				break
			histories.append(History(line))
		return histories

class Offer:
	def __init__(self, line):			
		values = line.split(',')
		self.offer = values[0]
		self.category = values[1]
		self.quantity = values[2]
		self.company = values[3]
		self.offervalue = values[4]
		self.brand = values[5]
		
	@classmethod
	def get_offers(cls,count = 100, filename = 'offers.csv'):

		offers = []
		for e, line in enumerate(open(filename, 'r')):
			if(e == 0):
				continue
			if(e > count):
				break
			offers.append(Offer(line))
		return offers

class Transaction:	
	def __init__(self, line):		
		values = line.split(',')
		self.user = values[0]
		self.chain = values[1]
		self.dept = values[2]
		self.category = values[3]
		self.company = values[4]
		self.brand = values[5]
		self.date = values[6]
		self.productsize = values[7]
		self.productmeasure = values[8]
		self.purchasequantity = values[9]
		self.purchaseamount = values[10]

	@classmethod
	def getTransactions(cls,count = 100, filename = 'reduced.csv'):		

		transactions = []
		for e, line in enumerate(open(filename, 'r')):
			if(e == 0):
				continue
			if(e > count):
				break
			transactions.append(Transaction(line))
		return transactions
