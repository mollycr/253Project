import sqlite3
from flask import Flask,request

# create our little application :)
app = Flask(__name__)

@app.route('/')
def root():
	return render_template('create_account.html')

@app.route('/', methods=['POST'])
def createAccount():
	#connect to db
	conn=sqlite3.connect('cmap.db')
	db=conn.cursor()
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
		db.execute('''INSERT INTO User VALUES(?,?,?,?)''',(null,userName,Email,Password))
		#render template Account successfully created
	#commits and close db connection
	conn.commit()
	conn.close()

if __name__ == '__main__':
    app.run()
  
