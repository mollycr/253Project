#!/usr/bin/env python

from subprocess import check_output
import flask
from os import environ
import os
import sqlite3
import random
import string
from flask import Flask,request, session
import hashlib


#TODO: make a table in the database for this
#db = shelve.open("shorts.db")


# create our little application :)
app = Flask(__name__)
app.debug=True

@app.route('/')
#render create account template
def root(message='default'):
	if message=='default':
		return flask.render_template('create_account.html')
	else:
		if 'username' in session:
			return flask.render_template('create_account.html',statusMessage='Logged in as %s' % escape(session['username']))
		else:
			return flask.render_template('create_account.html',statusMessage=message)

@app.route('/create_account', methods=['POST'])
def createAccount():
	#connect to cmap db
	conn=sqlite3.connect('cmap.db')
	db=conn.cursor()
	#grab all existing usernames and emails from db and make into dictionary where keys, values == usernames, emails
	existingAccounts=dict(db.execute("SELECT UserName,Email from User").fetchall())
	#username, email, password as requests to db
	username = str(request.form['username'])
	email = str(request.form['email'])
	password = str(request.form['password'])
	#checks if username already in database, reloads page for user to try again
	if username in existingAccounts:
		return flask.render_template('create_account.html', usernameError="Username is already taken")
	#checks if email already in database, reloads page for user to try again
	if email in existingAccounts.values():
		return flask.render_template('create_account.html',emailError="Email account already exists")
	else:
		#insert new user's values into cmap db
		salt = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(40))
		h = hashlib.sha1()
		#put salt and password to be hashed
		h.update(salt)
		h.update(password)
		db.execute('''INSERT INTO User VALUES(?,?,?,?)''',(username,email,salt,str(h.hexdigest())))

		#render template account successfully created
		#add in code to show html page once account created 
	#commits and close db connection
	conn.commit()
	conn.close()
	session['username']=username
	return root("Your account is created and you are logged in")

@app.route('/login', methods=['POST'])
def login():
	username = str(request.form['username'])
	password = str(request.form['password'])
	existingAccounts=dict(db.execute("SELECT UserName from User").fetchall())
	if(username not in existingAccounts):
		return root("Incorrect username. Want to create an account?")
	salt = str(db.execute("SELECT salt FROM User WHERE UserName=?",(username)).fetchone())
	dbHash = str(db.execute("SELECT hash FROM User WHERE UserName=?",(username)).fetchone())
	h = hashlib.sha1()
	h.update(salt)
	h.update(password)
	myHash = str(h.hexdigest())
	if(myHash != dbHash):
		return root("Incorrect password.")
	#start a session
	session['username']= username
	return redirect("http://people.ischool.berkeley.edu/~"+os.environ['USER']+"/server/")
	
@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect("http://people.ischool.berkeley.edu/~"+os.environ['USER']+"/server/")

'''
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
'''

app.secret_key = 'x1dc9rxe5^&cH#a0c6x10:90bd00f4edx92Wd6d2f3f'

if __name__ == "__main__":
	app.run(port=int(environ['FLASK_PORT']))	
