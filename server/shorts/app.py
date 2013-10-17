#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ

app = flask.Flask(__name__)
app.debug = True

db = shelve.open("shorten.db")


###
# Home Resource:
# Take and store
###
@app.route('/process', methods=['GET'])
def home():
	"""Converts long URLs to a unique key, stores that key, and redirects to the long URL when the key is accessed"""
	begin = "people.ischool.berkeley.edu/~mrobison/server/shorts/short/?shortURL="
	longURL = request.args.get('longURL')
	#check the database to see if the long URL has already been entered
	#check to see if the hash(longURL) is in the database
	dbKey = hash(longURL)
	#if the hash(longURL) is already in database but long URLs are not the same, then increment the key until you find
	# one that is empty or has a URL that matches the long URL	
	while(db.has_key(dbKey)==True and db[dbKey] != longURL):
		dbKey +=1
	#if long URL has already been entered, display the short URL
	if(db[dbKey]==longURL):
		return flask.rended_template(
			'proj1-draft.html',
			shortURL = begin+str(dbKey)
		)
	else:
		#hash the long URL to some key (maybe not actually hash, we'll see)
		db[dbKey] = longURL
		#display the form and fill in the short value
		return flask.render_template(
			'proj1-draft.html',
            shortURL = begin+str(dbKey)
		)
	return flask.rended_template(
		'error.html',
		)

###
# Redirection:
# 
###
@app.route('/short', methods=['GET'])
def redirect():
	shortURL = request.args.get('shortURL')
	longURL = db[shortURL]
	return flask.redirect(longURL)
	#redirect to whatever long URL is associated

if __name__ == "__main__":
	app.run(port=int(environ['FLASK_PORT']))
