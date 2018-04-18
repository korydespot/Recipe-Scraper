
#import pg

#conn = pg.DB(host="localhost", user= )

#result = conn.query("SELECT * FROM *")

from datetime import datetime, timedelta
import re
from functools import wraps
import urllib2
import time
from bs4 import BeautifulSoup
import psycopg2
import time

hostname = 'localhost'
username = 'sean'
password = 'passwordpassword'
port = '5432'
database = 'jsdk'

conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)

TIME_REGEX = re.compile(
		r'(\D*(?P<hours>\d+)\s*(hours|hrs|hr|h|Hours|H))?(\D*(?P<minutes>\d+)\s*(minutes|mins|min|m|Minutes|M))?'
)
ningred = 0

def get_minutes(line):
	string = line.get_text()
	time = TIME_REGEX.search(string)
	minutes = "'"
	minutes = int(time.groupdict().get('minutes') or 0)
	minutes = "00:" + str(minutes)
	return minutes

def normalize_string(strings):
	string = strings.get_text()
	return re.sub(
		r'\s+', ' ',
		string.replace(
		'\xa0', ' ').replace(  # &nbsp;
		'\n', ' ').replace(
		'\t', ' ').strip()
		)
# this section prints out data

def listinfo(sinstructions, singredients,cooktime,preptime,source):
    print source
    print get_minutes(preptime)
    print get_minutes(cooktime)
    for x in sinstructions:
	    istring = x.get_text()
	    print re.sub(
			    r'\s+', ' ',
			    istring.replace(
				    'xa0', ' ').replace(  # &nbsp;
					    '\n', ' ').replace(
						    '\t', ' '))


    for x in singredients:
	    string = x.get_text()
	    print re.sub(
			    r'\s+', ' ',
			    string.replace(
				    'xa0', ' ').replace(  # &nbsp;
					    '\n', ' ').replace(
    						    '\t', ' '))

def prepinfo(sinstructions, singredients,cooktime,preptime,source, instrc, ingred):
    #print source
    #print get_minutes(preptime)
    #print get_minutes(cooktime)
    for x in sinstructions:
	    istring = x.get_text()
	    instrc + re.sub(
			    r'\s+', ' ',
			    istring.replace(
				    'xa0', ' ').replace(  # &nbsp;
					    '\n', ' ').replace(
						    '\t', ' ')) + ","


    for x in singredients:
	    string = x.get_text()
	    ingred + re.sub(
			    r'\s+', ' ',
			    string.replace(
				    'xa0', ' ').replace(  # &nbsp;
					    '\n', ' ').replace(
    						    '\t', ' ')) + ","


HEADERS = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0 ' }

fil = open("test_querys.txt","w")


#testing to get other recipie's links from index
linksrequest = urllib2.Request('http://www.simplyrecipes.com/index/', headers=HEADERS)
rurl = urllib2.urlopen(linksrequest).read()
links = BeautifulSoup(rurl, "html.parser")

testlinks = links.find('div', {'id':'recipe-index-list'}).find_all('a', attrs={'href': re.compile("^https://")}) 
d = []

for x in testlinks:
        time.sleep(.3)
        t = urllib2.Request(x.get('href'), headers=HEADERS)
        ur = urllib2.urlopen(t).read()
        l = BeautifulSoup(ur,"html.parser")
        v = l.find('li', {'itemprop': 'itemListElement'}).find_all('a', attrs={'href': re.compile("^https://")})
        for i in v:
            time.sleep(.3)
            source = i.get('href');
            rname = source.split("/",5)[4]
            rname = rname.replace("_", " ")
            #print rname
            a = urllib2.Request(i.get('href'), headers=HEADERS)
            b = urllib2.urlopen(a).read()
            c = BeautifulSoup(b, "html.parser")
            d = c.find('span', {'class': 'preptime'})
            if(d == None):
                continue
            e = c.find('span', {'class': 'cooktime'})
            if(e == None):
                continue
            f = c.find('div', {'class': 'recipe-ingredients'}).find_all('li')
            g = c.find('div', {'itemprop': 'recipeInstructions'}).find_all('p')
	    cal = 0
            serving = 2
            strc = ""
	    gred = ""
            #prepinfo(sinstructions=g,singredients=f,cooktime=e,preptime=d,source=source,strc,gred)

	    strc = "{"
    	    for x in g:
	    	istring = x.get_text()
	    	strc += re.sub(
			    r'\s+', ' ',
			    istring.replace(
				    'xa0', ' ').replace(  # &nbsp;
					    '\n', ' ').replace(
						    '\t', ' '))
	    strc += "}"
	    strc = strc.replace("'","")
	    strc = ''.join(strc).encode('utf-8')
    	    d = get_minutes(d)
    	    e = get_minutes(e)
	    print e
            rstat = "INSERT INTO public.recipe VALUES (DEFAULT,'"
 	    rstat += rname
	    rstat += "', '" 
	    rstat += str(e)
	    rstat += "',"
	    rstat += str(cal)
	    rstat += ","
	    rstat += str(serving)
	    rstat += ",'"
	    rstat += str(strc)
	    rstat += "');"
	    cur = conn.cursor()
	    cur.execute(rstat)
	    time.sleep(1)
	    print "input recipe now onto ingredients"

    	    for x in f:
	    	string = x.get_text()
	    	gred = re.sub(
			    r'\s+', ' ',
			    string.replace(
				    'xa0', ' ').replace(  # &nbsp;
					    '\n', ' ').replace(
    						    '\t', ' '))
		gred = ''.join(gred).encode('utf-8')
		ridx = cur.execute("SELECT recipeid FROM recipe WHERE recipename = " + rname)
	   	print ridx



conn.commit()
conn.close()
	    


fil.close()
exit()




