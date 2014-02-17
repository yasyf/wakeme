import dbo, functions

class Number(dbo.DBO):
	"""MongoDB-Backed Number"""
	collection = functions.db.numbers
	def __init__(self,number):
		self.number = number
		super(Number,self).__init__(Number.collection,None,number=self.number)

	def create(self):
		super(Number,self).create(number=self.number,tz="UTC")
