#!/usr/bin/python

#import pg

#conn = pg.DB(host="localhost", user= )

#result = conn.query("SELECT * FROM *")

import re
from functools import wraps
import urllib2
import time

from bs4 import BeautifulSoup


TIME_REGEX = re.compile(
		r'(\D*(?P<hours>\d+)\s*(hours|hrs|hr|h|Hours|H))?(\D*(?P<minutes>\d+)\s*(minutes|mins|min|m|Minutes|M))?'
)


def get_minutes(line):
	string = line.get_text()
	time = TIME_REGEX.search(string)
	minutes = int(time.groupdict().get('minutes') or 0)
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



HEADERS = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36' }



#testing to get other recipie's links from index
linksrequest = urllib2.Request('http://www.simplyrecipes.com/index/', headers=HEADERS)
rurl = urllib2.urlopen(linksrequest).read()
links = BeautifulSoup(rurl, "html.parser")

testlinks = links.find('div', {'id':'recipe-index-list'}).find_all('a', attrs={'href': re.compile("^http://")}) 

d = []

for x in testlinks:
        time.sleep(.3)
        t = urllib2.Request(x.get('href'), headers=HEADERS)
        ur = urllib2.urlopen(t).read()
        l = BeautifulSoup(ur,"html.parser")
        v = l.find('li', {'itemprop': 'itemListElement'}).find_all('a', attrs={'href': re.compile("^http://")})
        for i in v:
            source = i.get('href');
            a = urllib2.Request(i.get('href'), headers=HEADERS)
            b = urllib2.urlopen(a).read()
            c = BeautifulSoup(b, "html.parser")
            d = c.find('span', {'class': 'preptime'})
            e = c.find('span', {'class': 'cooktime'})
            if(e == None):
                continue
            f = c.find('div', {'class': 'recipe-ingredients'}).find_all('li')
            g = c.find('div', {'itemprop': 'recipeInstructions'}).find_all('p')
            listinfo(sinstructions=g,singredients=f,cooktime=e,preptime=d,source=source)
        


exit()




