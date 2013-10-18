#!/usr/bin/env python

from subprocess import check_output
import flask
from flask import request
from flask.ext import shelve
from os import environ

app = flask.Flask(__name__)
app.debug = True

app.config['SHELVE_FILENAME'] = 'shelve.db'
shelve.init_app(app)

db = shelve.get_shelve('c')

###
# Home Resource:
# Take and store
###
@app.route('/process', methods=['GET'])
def home():
	"""Converts long URLs to a unique key, stores that key, and redirects to the long URL when the key is accessed"""
	begin = "people.ischool.berkeley.edu/~mrobison/server/shorts/short/?shortURL="
	longURL = request.args.get('longURL')
	shortURL = request.args.get('shortURL')
	#I guess we're not doing any checking since flask-shelve doesn't have anything approaching good docs.
	db[shortURL] = longURL
	return flask.render_template(
		'proj1.html',
		shortURL = begin + shortURL
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
