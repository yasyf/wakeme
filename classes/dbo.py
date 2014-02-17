#!/usr/bin/env python

from functions import ObjectId

class DBO(object):
	"""MongoDB-Backed Object"""
	def __init__(self,collection,oid,**kwargs):
		self.collection = collection
		for kw,val in kwargs:
			self.obj = self.collection.find_one({kw: val})
			if self.obj != None:
				break
		self.obj = self.collection.find_one({"_id": ObjectId(oid)})

	def exists(self):
		return self.obj != None

	def create(self, **kwargs):
		if self.obj == None:
			self.collection.insert(kwargs)

	def get(self,attr):
		try:
			return self.obj[attr]
		except KeyError:
			return None

	def set(self,attr,val):
		self.collection.update({"_id": self.get("_id")}, {"$set": {attr: val}})
		self.obj = self.collection.find_one({"_id": self.get("_id")})
