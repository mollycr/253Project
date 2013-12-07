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

    
def add_row(long, short, clicks, tags):

    #create new html file or overwrite file if it already exists
    results_file = open("new.html", "w+")

    #create start tags for html doc
    start_html = '<!DOCTYPE html><html><header><title></title></header><body>'

    row_html = '<TR> <TD></TD><TD>%s</TD><TD>%s</TD><TD>%d</TD><TD><input type="checkbox" value="enrolled" unchecked></TD><TD>%s</TD> % (long, short, clicks, tags)

    end_html = '</body></html>'

    html_code = start_html + row_html + end_html
    
         
    #write opening tags for html document up to body
    results_file.write(html_code)    


    #open written file in web browser
    webbrowser.open("file:///pathtofile_____new.html")       
    




