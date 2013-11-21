import sqlite3
import flask 

# create our little application :)
app = flask.Flask(__name__)

#connect to db
conn=sqlite3.connect('cmap.db')
db=conn.cursor()

#create table
db.executescript('''
	DROP TABLE IF EXISTS Entries;
	create table entries(
	id integer primary key autoincrement,
	title text not null,
	text text not null);
''')

@app.route('/')
def show_entries():
	entries=db.execute('select title,text from entries')


if __name__ == '__main__':
    app.run()