#!/usr/bin/env python

from subprocess import check_output
import flask
from os import environ
import string
import sqlite3
import random
import string
from flask import Flask,request, session, escape, redirect
import hashlib


#TODO: make a table in the database for this

# create our little application :)
app = Flask(__name__)
app.debug=True

user=environ['USER']

#reroutes home page to index page
@app.route('/')
def sendToIndex():
	url='http://people.ischool.berkeley.edu/~'+user+'/server/index'
	return flask.redirect(url)

@app.route('/index')
def index(message='default', url='default'):
	if message=='default':
		if url=='default':
			if 'username' in session:
				return flask.render_template('home.html',USER=user,USERNAME=escape(session['username']))
			else:
				return flask.render_template('home.html',USER=user)
		else:
			if 'username' in session:
				return flask.render_template('home.html',USER=user,USERNAME=escape(session['username']),shortURL=url)
			else:
				return flask.render_template('home.html',USER=user,shortURL=url)
	else:
		if url=='default':
			if 'username' in session:
				return flask.render_template('home.html', USER=user, USERNAME=escape(session['username']), statusMessage=message)
			else:
				return flask.render_template('home.html',USER=user, statusMessage=message)
		else:
			if 'username' in session:
				return flask.render_template('home.html', USER=user, USERNAME=escape(session['username']), statusMessage=message, shortURL=url)
			else:
				return flask.render_template('home.html',USER=user, statusMessage=message, shortURL=url)

@app.route('/create_account',methods=['GET'])
#renders create account page before and after create account form is posted
def createAccountConfirm(message='default'):
	if message!='default':
		return flask.render_template('create_account.html',statusMessage=message)
	else:
		if 'username' in session:
			return flask.render_template('create_account.html',statusMessage='Logged in as %s' % escape(session['username']))
		else:
			return flask.render_template('create_account.html')

@app.route('/create_account', methods=['POST'])
def create_account():
	#connect to cmap db
	conn=sqlite3.connect('cmap.db')
	db=conn.cursor()
	#create things from form
	username = str(request.form['username'])
	email = str(request.form['email'])
	password = str(request.form['password'])

	#checks if username already in database, reloads page for user to try again
	db.execute("SELECT email FROM User WHERE username='"+username+"'")
	if db.fetchone() is not None:
		return flask.render_template('create_account.html', statusMessage="Username is already taken")
	#checks if email already in database, reloads page for user to try again
	db.execute("SELECT username FROM User WHERE email='"+email+"'")
	if db.fetchone() is not None:
		return flask.render_template('create_account.html',statusMessage="There's already an account for this email")
	else:
		#insert new user's values into cmap db
		salt = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(40))
		h = hashlib.sha1()
		#put salt and password to be hashed
		h.update(salt)
		h.update(password)
		db.execute('''INSERT INTO User VALUES(?,?,?,?)''',(username,email,salt,h.hexdigest()))

		#render template account successfully created
		#add in code to show html page once account created 
	#commits and close db connection
	conn.commit()
	conn.close()
	session['username']=username
	return index("Your account is created and you are logged in")

@app.route('/login', methods=['POST'])
def login():
	conn=sqlite3.connect('cmap.db')
	db=conn.cursor()
	username = str(request.form['username'])
	password = str(request.form['password'])
	#check if user exists
	db.execute("SELECT salt FROM User WHERE username='"+username+"'")
	salt=db.fetchone()
	if salt is None:
		return index("Incorrect username. Want to create an account?")
	salt=salt[0]
	db.execute("SELECT hash FROM User WHERE username='"+username+"'")
	dbHash=db.fetchone()[0]
	h = hashlib.sha1()
	h.update(salt)
	h.update(password)
	myHash = str(h.hexdigest())
	if(myHash != dbHash):
		return index("Incorrect password.")
	#start a session
	conn.commit()
	conn.close()
	session['username']= username
	return redirect("http://people.ischool.berkeley.edu/~"+user+"/server/")
	
@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect("http://people.ischool.berkeley.edu/~"+user+"/server/")


###
# This is what the html page should send data to
###
@app.route('/shorts', methods=['POST'])
def shorts():
	conn=sqlite3.connect('cmap.db')
	db=conn.cursor()
	begin = "people.ischool.berkeley.edu/~"+user+"/server/short/"
	longURL = str(request.form['long'])
	longURL = processURL(longURL)
	shortURL = str(request.form['short'])
	generated = False
	username = ""
	if 'username' in session:
		username = session['username']
	else:
		username = str(request.remote_addr)
	if shortURL=="":
		shortURL = ''.join(random.choice(string.ascii_lowercase+string.digits) for x in range(6))
		generated = True
	#check to see if the short url is already in the db
	db.execute("SELECT * FROM Urls WHERE short='"+shortURL+"'")
	if db.fetchone() is not None:
		if generated:
			# if it is, and the short was auto, generate a new short until it's not taken
			flag = False
			while(flag==False):
				shortURL = ''.join(random.choice(string.ascii_lowercase+string.digits) for x in range(6))
				db.execute("SELECT * FROM Urls WHERE short='"+shortURL+"'")
				if db.fetchone() is None:
					flag = True
		else:
			# if it is, and the user specified the short, return error
			return index("That short URL was already taken. Try again.")
	# if we're good, put the long, short, 0, {username or IP} into the DB
	db.execute("INSERT INTO Urls VALUES(?,?,?,?)",(longURL,shortURL,0,username))
	conn.commit()
	conn.close()
	return index(url=begin+shortURL)

###
# Redirection: 
###
@app.route('/short/<shortURL>')
def short(shortURL):
	shortURL = str(shortURL)
	#check to see if the short URL is in the database
	conn=sqlite3.connect('cmap.db')
	db=conn.cursor()
	db.execute("SELECT url from Urls WHERE short='"+shortURL+"'")
	longURL = db.fetchone()
	#if it's not, return 404
	if longURL is None:
		return render_template('page_not_found.html'), 404
	# if it is, return it and increase the counter
	db.execute("UPDATE Urls SET timesVisited=timesVisited+1 WHERE short='"+shortURL+"'")
	longURL = longURL[0]
	conn.commit()
	conn.close()
	return flask.redirect(longURL)
	#redirect to whatever long URL is associated

def processURL (url):
	#see if it's in http://www.google.com form
	if url[:7]=="http://":
		return url
	elif url[:4]=="www.":
		return "http://"+url
	else:
		return "http://www."+url


app.secret_key = 'x1dc9rxe5^&cH#a0c6x10:90bd00f4edx92Wd6d2f3f'

if __name__ == "__main__":
	app.run(port=int(environ['FLASK_PORT']))	
