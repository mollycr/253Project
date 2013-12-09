#!/usr/bin/env python

from subprocess import check_output
import flask
import os
import string
import hashlib
import sqlite3
import random
import string
from flask import Flask,request, session, escape, redirect
import bcrypt


# create our little application :)
app = Flask(__name__)
app.debug=True

user=os.environ['USER']

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
	em=db.execute("SELECT email FROM User WHERE username=?", (username,)).fetchone()
	if em is not None:
		return flask.render_template('create_account.html', statusMessage="Username is already taken")
	#checks if email already in database, reloads page for user to try again
	un=db.execute("SELECT username FROM User WHERE email=?", (email,)).fetchone()
	if un is not None:
		return flask.render_template('create_account.html',statusMessage="There's already an account for this email")
	else:
		#check to see if we have any urls from when they didn't have a username
		ip = request.remote_addr
		if ip in usernameList:
			db.execute("UPDATE Urls SET username=? WHERE username=?", (username, ip))
		else:
		#insert new user's values into cmap db
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			db.execute('''INSERT INTO User VALUES(?,?,?)''',(username,email,hashed))
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
	db.execute("SELECT hash FROM User WHERE username=?", (username,))
	hashed=db.fetchone()
	if hashed is None:
		return index("Incorrect username. Want to create an account?")
	if bcrypt.hashpw(password, hashed) != hashed:
		return index("Incorrect password.")
	#start a session
	conn.commit()
	conn.close()
	session['username']= username
	return index()
	
@app.route('/logout')
def logout():
	session.pop('username', None)
	return index()

@app.route('/myAccount')
def myAccount():
	#Insert html generation here
	#TODO test

	#generate the starting html
	html = '''<form id="deleteLinks" action="delete" method="post">
						<table id="links">
							<th>
								<td>Long url</td>
								<td>Short url</td>
								<td>Number of visits</td>
								<td>Tags</td>
								<td>Created</td>
								<td>Delete?</td>
							</th>
				'''
	tableEnd = '</table> <input type="submit" value="Delete selected"/> </form>'
	rowTemplate = '''<tr>
						<td> %(long) </td>
						<td> %(short) </td>
						<td> %(visits) </td>
						<td> %(tags) </td>
						<td> %(timestamp) </td>
						<td> <input type="checkbox" name="delete" value="%(short)"/> </td
					</tr>
				'''
	#get all the user's links from the database:
	conn=sqlite3.connect('cmap.db')
	db=conn.cursor()
	username = session['username']
	db.execute("SELECT url, short, timesVisited, currentTime FROM Urls WHERE username=?", (username,))
	row = db.fetchone()
	#row is a... list? array? whatever of all the values

	while row is not None:
	#for every link in that table:
		longURL = row[0]
		shortURL = row[1]
		visits = row[2]
		timestamp = row[3]
		tags = ""
		#get the tags for that link
		db.execute("SELECT tag FROM Tags WHERE short=?", (shortURL,))
		tagsList = db.fetchall()
		for tag in tagsList:
			 tags += tag[0]
		#add all the information into the template
		row = rowTemplate % {"long" : longURL, "short" : shortURL, "visits" : visits, "timestamp" : timestamp, "tags" : tags}
		#add the template to the main
		html += row
		row = db.fetchone()

	html += tableEnd
	conn.commit()
	conn.close()
	return flask.render_template('my_account.html',USER=user,LinkTable=html)

@app.route('/delete', methods=['POST'])
def delete():
	#delete the selected rows from the table
	#TODO test
	conn=sqlite3.connect('cmap.db')
	db=conn.cursor()

	toDelete = request.form.getlist("delete")
	for short in toDelete:
		db.execute("DELETE FROM Urls WHERE short=?", (short,))

	conn.commit()
	conn.close()
	return myAccount()

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
	generated = False
	shortURL = ""
	if(request.form["URL"]=="autoCreate"):
		generated = True
		shortURL = ''.join(random.choice(string.ascii_lowercase+string.digits) for x in range(6))
	else:
		shortURL = str(request.form['short'])
	username = ""

	if 'username' in session:
		username = session['username']
	else:
		username = str(request.remote_addr)

	#check to see if the short url is already in the db
	shortUrlList=db.execute("SELECT * FROM Urls WHERE short=?", (shortURL,)).fetchone()
	if shortUrlList is not None:
		if generated:
			# if it is, and the short was auto, generate a new short until it's not taken
			flag = False
			while(flag==False):
				shortURL = ''.join(random.choice(string.ascii_lowercase+string.digits) for x in range(6))
				if shortURL not in shortUrlList:
					flag = True
		else:
			# if it is, and the user specified the short, return error
			return index("That short URL was already taken. Try again.")
	# if we're good, put the long, short, 0, {username or IP} into the DB
	db.execute("INSERT INTO Urls VALUES(?,?,?,?,datetime('now','localtime'))",(longURL,shortURL,0,username))
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
	db.execute("SELECT url from Urls WHERE short=?", (shortURL,))
	longURL = db.fetchone()
	#if it's not, return 404
	if longURL is None:
		return render_template('page_not_found.html'), 404
	# if it is, return it and increase the counter
	db.execute("UPDATE Urls SET timesVisited=timesVisited+1 WHERE short=?", (shortURL,))
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


app.secret_key = os.urandom(24)

if __name__ == "__main__":
	app.run(port=int(os.environ['FLASK_PORT']))	
