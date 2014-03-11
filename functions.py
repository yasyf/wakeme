#!/usr/bin/env python

from setup import *
from bson.objectid import ObjectId
from classes.call import Call
from classes.number import Number
from flask import Flask, Response, session, redirect, url_for, escape, request, render_template, g, flash, make_response
import twilio.twiml
from dateutil.parser import parse
from dateutil import tz
import datetime


def create_call(number,time,*args):
	timezone = args[0] if len(args) > 0 and len(args[0]) > 2 else None
	message = args[1] if len(args) > 1 else None
	call = Call(None)
	number_obj = Number(number)
	now = datetime.datetime.utcnow().replace(tzinfo=tz.tzutc())
	if not number_obj.exists():
		number_obj.create()
	if timezone:
		number_obj.set("tz",timezone)
	dt = parse(time)
	if dt.tzinfo == None:
		try:
			stored_timezone = tz.gettz(number_obj.get("tz")) if tz.gettz(number_obj.get("tz")) else tz.gettz(timezone)
			dt = dt.replace(tzinfo=stored_timezone)
		except TypeError:
			dt = dt.replace(tzinfo=tz.gettz(timezone))
	else:
		dt = dt.replace(tzinfo=tz.gettz(timezone))
	if dt.tzinfo == None:
		dt = dt.replace(tzinfo=tz.tzutc())
	if dt < now:
		dt = dt + datetime.timedelta(days=1)

	resp = twilio.twiml.Response()
	resp.message("Alarm created for %s" % (dt.strftime("%c %Z")))
	dt = dt.astimezone(tz.tzutc())
	call.create(number,dt,message)
	return str(resp)

def view_call(number):
	number = Number(number)
	c = number.get_calls()
	resp = twilio.twiml.Response()
	if c.count() == 0:
		resp.say("You have no upcoming alarms.")
	else:
		resp.say("Your next alarm is for %s" % (c[0]["dt"].strftime("%c %Z")))
		if c[0]["message"]:
			resp.say("Your custom message is: %s" % c[0]["message"])
	return str(resp)

def activate_call(number):
	number = Number(number)
	c = number.get_current_call()
	resp = twilio.twiml.Response()
	resp.say('This is Wake Me. It is time to wake up!')
	if c['message']:
		resp.say(c['message'])
	return str(resp)

def call(number, message):
	tw_client.calls.create(to=number, from_="+16176063543", url="http://ym-wakeme.herokuapp.com/alarm/activate")
	text = "[wakeme] Time to get up!"
	if message:
		text += " " + message
	tw_client.messages.create(to=number, from_="+16176063543", body=text)
