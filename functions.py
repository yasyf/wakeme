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


def create_call(number,time,message,*args):
	call = Call(None)
	number = Number(number)
	if not number.exists():
		number.create()
	dt = parse(time)
	if dt.tzinfo == None:
		dt = parse(time + number.get("tz"))
	else:
		number.set("tz",dt.tzname())		
	if dt < datetime.datetime.utcnow():
		dt = dt + datetime.timedelta(days=1)
	call.create(number,dt,message)
	resp = twilio.twiml.Response()
	resp.message("Alarm created for %s" % (dt.strftime("%c %Z")))
	return str(resp)

def view_call(number):
	number = Number(number)
	c = number.get_calls()
	resp = twilio.twiml.Response()
	if c.count() == 0:
		resp.say("You have no upcoming alarms.")
	else:
		resp.say("Your next alarm is for %s" % (c[0]["dt"].strftime("%c %Z")))
	return str(resp)

def activate_call(number):
	number = Number(number)
	c = number.get_current_call()
	resp = twilio.twiml.Response()
	resp.say('This is wakeme. It is time to wake up!')
	if c['message']:
		resp.say(c['message'])
	return str(resp)

def call(number):
	tw_client.calls.create(to=number, from_="+16176063543",url="http://http://ym-wakeme.herokuapp.com/alarm/activate")