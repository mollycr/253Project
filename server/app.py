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
# This is what the html page should send data to
###
@app.route('/shorts', methods=['POST'])
def home():
	"""Converts long URLs to a unique key, stores that key, and redirects to the long URL when the key is accessed"""
	begin = "people.ischool.berkeley.edu/~mrobison/server/short/"
	longURL = request.form.get('longURL')
	shortURL = request.form.get('shortURL')
	#I guess we're not doing any checking since flask-shelve doesn't have anything approaching good docs.
	db[shortURL] = longURL
	return flask.render_template(
		'proj1.html',
		shortURL = begin + shortURL
	)

###
# Redirection:
# this is 
###
@app.route('/short')
def redirect():
	shortURL = request.path
	if("the short URL isn't there"):
		return render_template('page_not_found.html'), 404

	longURL = db[shortURL]
	return flask.redirect(longURL)
	#redirect to whatever long URL is associated

@app.route('/')
def default():
	return flask.render_template('proj1.html')

if __name__ == "__main__":
	app.run(port=int(environ['FLASK_PORT']))
