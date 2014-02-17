import dbo, functions

class Call(dbo.DBO):
	"""MongoDB-Backed Call"""
	collection = functions.db.numbers
	def __init__(self,oid):
		super(Call,self).__init__(Call.collection,oid)

	def create(self,number,dt,message):
		super(Call,self).create(number=number,dt=dt,message=message,completed=False)

	def make_call(self):
		functions.call(self.get("number"))
