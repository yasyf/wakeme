import dbo, functions

class Number(dbo.DBO):
	"""MongoDB-Backed Number"""
	collection = functions.db.numbers
	def __init__(self,number):
		self.number = number
		super(Number,self).__init__(Number.collection,None,number=self.number)

	def create(self):
		super(Number,self).create(number=self.number,tz="UTC")

	def get_calls(self):
		return functions.db.calls.find({"number": self.number, "completed": False})

	def get_current_call(self):
		call = functions.db.calls.find_one({"number": self.number, "completed": False},sort=[("dt", pymongo.ASCENDING)])
		functions.db.calls.update({"_id": call["_id"]},{"$set": {"completed": True}})
		return call
