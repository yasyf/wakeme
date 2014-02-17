from functions import *
from classes.call import Call

def make_calls():
	c = calls.find({"dt": {"$lte": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}})
	for call in c:
		call_obj = Call(str(call["_id"]))
		call_obj.make_call()