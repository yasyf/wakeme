import pymongo, os
from twilio.rest import TwilioRestClient

client = pymongo.MongoClient(os.environ['db'])
tw_client = TwilioRestClient()
db = client.sos
calls = db.calls