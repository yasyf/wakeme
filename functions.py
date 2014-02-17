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
	if dt < dt.utcnow():
		dt = dt + datetime.timedelta(days=1)
	call.create(number,dt,message)