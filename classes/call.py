import dbo, functions

class Call(dbo.DBO):
	"""MongoDB-Backed Call"""
	collection = functions.db.calls
	def __init__(self,oid):
		super(Call,self).__init__(Call.collection,oid)

	def create(self,number,dt,message):
		if self.collection.find_one({"number": number, "dt": dt}) != None:
			return
		super(Call,self).create(number=number,dt=dt,message=message,completed=False)

	def make_call(self):
		functions.call(self.get("number"))
