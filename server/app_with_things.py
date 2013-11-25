#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ

app = flask.Flask(__name__)
app.debug = True
db = shelve.open("shorts.db")

###
# This is what the html page should send data to
###
@app.route('/shorts', methods=['POST'])
def shorts():
	begin = "people.ischool.berkeley.edu/~mrobison/server/short/"
	longURL = str(request.form['long'])
	longURL = processURL(longURL)
	shortURL = str(request.form['short'])
	db[shortURL] = longURL
	return home(begin+shortURL)

###
# Redirection: 
###
@app.route('/short/<shortURL>')
def short(shortURL):
	shortURL = str(shortURL)
	if(db.has_key(shortURL)==False):
		return render_template('page_not_found.html'), 404
	longURL = db[shortURL]
	return flask.redirect(longURL)
	#redirect to whatever long URL is associated

@app.route('/login', methods=['POST'])
def login():
	username = str(request.form['username'])
	hashword = str(request.form['passwordHash'])
	if("the username is not in the database"):
		return "Incorrect username. Want to create an account?"
	else:
		if("the password is incorrect"):
			return "Incorrect password."
		"start a session"

@app.route('/', methods=['POST'])
def createAccount():
	#grab all existing usernames and emails from db
	existingAccounts=dict(db.execute('''SELECT UserName,Email from User''').fetchall())
	userName = str(request.form['username'])
	Email=str(request.form['email'])
	Password=str(request.form['password'])
	if userName in existingAccounts:
		return render_template('create_account.html', usernameError="Username is already taken")
	if Email in existingAccounts.values():
		return render_template('create_account.html',emailError="Email account already exists")
	else:
		salt = os.urandom(40)
		h = hashlib.sha1()
		h.update(salt)
		h.update(Password)
		db.execute('''INSERT INTO User VALUES(?,?,?,?,?)''',(null,userName,Email,h.hexdigest(),salt))
		#render template Account successfully created

@app.route('/')
def home(newURL="default"):
	if newURL=="default":
		return flask.render_template('proj1.html')
	else:
		return flask.render_template('proj1.html', shortURL=newURL)

def processURL (url):
	#see if it's in http://www.google.com form
	if url[:7]=="http://":
		return url
	elif url[:4]=="www.":
		return "http://"+url
	else:
		return "http://www."+url

if __name__ == "__main__":
	app.run(port=int(environ['FLASK_PORT']))