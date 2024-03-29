#!/usr/bin/env python

from subprocess import check_output
import flask
import os
import string
import hashlib
import sqlite3
import random
import string
from flask import Flask,request, session, escape, redirect, jsonify
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
def index(loginMessage = 'default', topMessage='default', url='default'):
	if loginMessage=='default':
		if topMessage=='default':
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
	else:
		if topMessage=='default':
			if url=='default':
				if 'username' in session:
					return flask.render_template('home.html',lmessage = loginMessage,USER=user,USERNAME=escape(session['username']))
				else:
					return flask.render_template('home.html',lmessage = loginMessage,USER=user)
			else:
				if 'username' in session:
					return flask.render_template('home.html',USER=user,lmessage = loginMessage,USERNAME=escape(session['username']),shortURL=url)
				else:
					return flask.render_template('home.html',USER=user,lmessage = loginMessage,shortURL=url)
		else:
			if url=='default':
				if 'username' in session:
					return flask.render_template('home.html', USER=user,lmessage = loginMessage, USERNAME=escape(session['username']), statusMessage=message)
				else:
					return flask.render_template('home.html',USER=user,lmessage = loginMessage, statusMessage=message)
			else:
				if 'username' in session:
					return flask.render_template('home.html', USER=user,lmessage = loginMessage, USERNAME=escape(session['username']), statusMessage=message, shortURL=url)
				else:
					return flask.render_template('home.html',USER=user, statusMessage=message,lmessage = loginMessage, shortURL=url)


@app.route('/create_account',methods=['GET'])
#renders create account page before and after create account form is posted
def createAccountConfirm(message='default'):
	if message!='default':
		return flask.render_template('create_account.html',USER=user, statusMessage=message)
	else:
		if 'username' in session:
			return flask.render_template('create_account.html',USER=user, statusMessage='Logged in as %s' % escape(session['username']))
		else:
			return flask.render_template('create_account.html', USER=user)

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
		return flask.render_template('create_account.html', USER=user, statusMessage="Username is already taken")
	#checks if email already in database, reloads page for user to try again
	un=db.execute("SELECT username FROM User WHERE email=?", (email,)).fetchone()
	if un is not None:
		return flask.render_template('create_account.html',USER=user,statusMessage="There's already an account for this email")
	else:
		#check to see if we have any urls from when they didn't have a username
		db.execute("UPDATE Urls SET username=? WHERE username=?", (username, request.remote_addr)) #can't hurt
		#insert new user's values into cmap
		hashed = bcrypt.hashpw(password, bcrypt.gensalt())
		db.execute('''INSERT INTO User(username, email, hash) VALUES(?,?,?)''',(username,email,hashed))
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
		return index('Incorrect username. Want to <a href="http://people.ischool.berkeley.edu/~'+user+'/server/create_account">create an account?</a>')
	hashed = hashed[0]
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
	#generate the starting html
	html = '''<form id="deleteLinks" action="update" method="post">
				<input type="hidden" name="shorts" value="%(allShorts)s"/>
				<table id="linksTable">
					<thead>
					<tr>
						<th data-sort="string">Long url</th>
						<th data-sort="string">Short url</th>
						<th data-sort="int">Number of visits</th>
						<th data-sort="string">Created</th>
						<th>Delete?</th>
						<th>Tags</th>
						<th>Add tags</th>
					</tr>
					</thead>
					<tbody>
				'''
	tableEnd = '</tbody></table> <input type="submit" value="Delete selected"/> </form>'
	rowTemplate = '''
					<tr>
						<td> %(long)s </td>
						<td> %(short)s </td>
						<td> %(visits)d </td>
						<td> %(timestamp)s </td>
						<td> <input type="checkbox" name="delete" value="%(short)s"/> </td>
						<td> %(tags)s </td>
						<td>
							<div name="nestedform">
								<input type="text" name="%(short)s" placeholder="tag1 tag2"/>
								<input type="submit" value="Add tag(s)"/>
							</div>
						</td>
					</tr>
					'''
	tagTemplate = '<span class="tag">%(tag)s</span> '

	#get all the user's links from the database:
	conn=sqlite3.connect('cmap.db')
	db=conn.cursor()
	db2=conn.cursor()
	username = session['username']
	db.execute("SELECT url, short, timesVisited, currentTime FROM Urls WHERE username=?", (username,))
	row = db.fetchone()
	#row is a... list? array? whatever of all the values

	x = 0
	tempHtml = ""
	shorts = ""

	while row is not None:
	#for every link in that table:
		longURL = row[0]
		shortURL = row[1]
		visits = row[2]
		timestamp = row[3]
		tags = ""
		#get the tags for that link
		db2.execute("SELECT tag FROM Tags WHERE short=?", (shortURL,))
		tagsList = db2.fetchall()
		for tag in tagsList:
			 tags += tagTemplate % {"tag" : tag[0]}
		#add all the information into the template
		row = rowTemplate % {"long" : longURL, "short" : shortURL, "visits" : visits, "timestamp" : timestamp, "tags" : tags, "x" : x}
		shorts += (shortURL + " ")
		#add the template to the main
		tempHtml += row
		row = db.fetchone()
		x += 1
	finalhtml = html%{"allShorts": shorts} + tempHtml + tableEnd
	conn.commit()
	conn.close()
	return flask.render_template('my_account.html',USER=user,LinkTable=finalhtml)

@app.route('/update', methods=['POST'])
def update():
	#fake two forms: either deleting or adding tags
	conn=sqlite3.connect('cmap.db')
	db=conn.cursor()

	shorts = request.form["shorts"]

	#TODO not all of these shorts have data
	shorts = string.split(shorts)
	for short in shorts:
		if short in request.form:
			print "HERE"
			tags = request.form[short]
			tags = string.split(tags)
			for tag in tags:
				db.execute("INSERT INTO Tags(tag, short) VALUES(?, ?)", (tag, short))

	#TODO will this work if there's nothing?
	toDelete = request.form.getlist("delete")
	print toDelete
	for short in toDelete:
		print short
		db.execute("DELETE FROM Urls WHERE short=?", (short,))
		db.execute("DELETE FROM Tags WHERE short=?", (short,))

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
			return index(topMessage = "That short URL was already taken. Try again.")
	# if we're good, put the long, short, 0, {username or IP} into the DB
	db.execute("INSERT INTO Urls(url, short, username, timesVisited, currentTime) VALUES(?,?,?,?,datetime('now','localtime'))",(longURL,shortURL,username,0))
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
		return flask.render_template('page_not_found.html', USER=user), 404
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
