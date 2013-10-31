#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ

app = flask.Flask(__name__)
app.debug = True
#app.config['SERVER_NAME'] = "people.ischool.berkeley.edu/"
#app.config['APPLICATION_ROOT'] = "~mrobison/server"
db = shelve.open("shorts.db")


###
# This is what the html page should send data to
###
@app.route('/shorts', methods=['POST'])
def shorts():
	begin = "people.ischool.berkeley.edu/~mrobison/server/short/"
	longURL = request.form.get('longURL')
	shortURL = request.form.get('shortURL')
	db[shortURL] = longURL
	return flask.render_template(
		'proj1.html',
		shortURL = begin + shortURL
	)

###
# Redirection: 
###
@app.route('/short/<shortURL>')
def short(shortURL):
	flask.log(shortURL)
	if(db.has_key(shortURL)==False):
		return render_template('page_not_found.html'), 404
	longURL = db[shortURL]
	return flask.redirect(longURL)
	#redirect to whatever long URL is associated

@app.route('/')
def home():
	return flask.render_template('proj1.html', shortURL = "test")

if __name__ == "__main__":
	app.run(port=int(environ['FLASK_PORT']))
