from bs4 import BeautifulSoup
from urllib2 import urlopen
from collections import defaultdict
import string
import re
import webbrowser 


#Write file that generates html page showing rows of the database transformed into HTML table. 
#Or do we just want to insert into the body of the existing HTML page? 
#Use .write() only once if possible for efficiency. 
#Open html file. 
#Create table based on rows of database for signed-in user (reference session cookie).
#Fill in all link information based on contents of db.  

# <TR> <TD>///For each new link shortened, generate a new row in table here/// </TD>
#                      <TD>long link</TD>
#                      <TD>short link</TD>
#                      <TD># of clicks</TD>
#                      <TD>checkbox</TD>
#                      <TD>tag1, tag2, tag4</TD>

#When form submitted by clicking "Delete Links" at bottom, we can drop rows related to those links. 
#What would be better is allowing a delete that doesn't force rerendering of entire page. 

####################
#	So all we need to generate here is the table that's going into the html page
#	Once we have that table, we're going to plug it into the page through flask, using the curly-brace thing.
#	So, we need to pull all the relavent information from the database and massage it into a table
#

def create_table(username):
	#generate the starting html
	tableStart = '''<table id="links">
						<th>
							<td>Long url</td>
				etc
				'''
	#get all the user's links from the database:
	#SELECT * FROM Urls WHERE user=username

	#for every link in that table:
		#start another row of html
		tableRow = "<tr>"
		#add table cells to that for all the relavent information
		
		#add a cell with the tags in it:
		#SELECT tag FROM Tags WHERE short=short
		#for all the tags:
			#add the tag text

  
def add_row(long, short, clicks, tags):

    #create new html file or overwrite file if it already exists
    results_file = open("new.html", "w+")

    #create start tags for html doc
    start_html = '<!DOCTYPE html><html><header><title></title></header><body>'

    row_html = '<TR> <TD></TD><TD>%s</TD><TD>%s</TD><TD>%d</TD><TD><input type="checkbox" value="enrolled" unchecked></TD><TD>%s</TD> % (long, short, clicks, tags)'

    end_html = '</body></html>'

    html_code = start_html + row_html + end_html
    
         
    #write opening tags for html document up to body
    results_file.write(html_code)    


    #open written file in web browser
    webbrowser.open("file:///pathtofile_____new.html")       
    




