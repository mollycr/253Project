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
# Only supports the GET method, returns a homepage represented as HTML
###
@app.route('/home', methods=['POST'])
def home():
	"""Converts long URLs to a unique key, stores that key, and redirects to the long URL when the key is accessed"""
	#get the long URL (ID=long)
	#check the database to see if the long URL has already been entered
	# db[short] = long
	#if not:
	#	hash the long URL to some key (maybe not actually hash, we'll see)
	#	db.insert(hash(long), long)
	#display the form and fill in the short value (ID=short)


###
# Redirection:
# 
###
@app.route('/short', methods=['GET'])
def redirect():
	#get the hash value from the path
	#look up the hash in the database
	#long = db[short]
	#redirect to whatever long URL is associated

if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
