from functions import *
from classes.call import Call

def make_calls():
	c = calls.find({"dt": {"$lte": datetime.datetime.utcnow().replace(tzinfo=tz.tzutc()) + datetime.timedelta(minutes=10)}})
	for call in c:
		print call
		call_obj = Call(str(call["_id"]))
		call_obj.make_call()

if __name__ == "__main__":
	make_calls()