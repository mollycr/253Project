#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from os import environ
import sqlite3
from flask import Flask,request


#We should instead use one database for all the data we're collecting. 
db = shelve.open("shorts.db")


# create our little application :)
app = Flask(__name__)
app.debug=True

@app.route('/')

#render create account template
def root():
	return flask.render_template('create_account.html')


@app.route('/', methods=['POST'])


def createAccount():
	
	#connect to cmap db
	conn=sqlite3.connect('cmap.db')
	db=conn.cursor()
'''	
	#grab all existing usernames and emails from db and make into dictionary where keys, values == usernames, emails
	existingAccounts=dict(db.execute("SELECT UserName,Email from User").fetchall())
	'''
	#username, email, password as requests to db
	username = str(request.form['username'])
	email = str(request.form['email'])
	password = str(request.form['password'])
	'''
	#checks if username already in database, reloads page for user to try again
	if username in existingAccounts:
		return flask.render_template('create_account.html', usernameError="Username is already taken")
	
	
	#checks if email already in database, reloads page for user to try again
	if email in existingAccounts.values():
		return flask.render_template('create_account.html',emailError="Email account already exists")
	
	
	else:
'''
		#insert new user's values into cmap db
	db.execute("INSERT INTO User VALUES(?,?,?,?)",(null,username,email,password))
		
		#render template account successfully created
		#add in code to show html page once account created 
		
	
	#commits and close db connection
	conn.commit()
	conn.close()




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
'''
@app.route('/')
def home(newURL="default"):
	if newURL=="default":
		return flask.render_template('proj1.html')
	else:
		return flask.render_template('proj1.html', shortURL=newURL)
'''
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
	
