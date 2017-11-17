import re
from functools import wraps
import urllib2

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



HEADERS = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36' }

request = urllib2.Request('http://www.simplyrecipes.com/recipes/beef_chili_mac_and_cheese', headers=HEADERS)
url = urllib2.urlopen(request).read()

requestl = urllib2.Request('http://www.simplyrecipes.com/?s', headers=HEADERS)
lurl = urllib2.urlopen(requestl).read()

test = BeautifulSoup(url, "html.parser")
linkss = BeautifulSoup(lurl, "html.parser")
#print test
# preptime 
sprep = test.find('span', {'class': 'preptime'})  
# cooktime
scook = test.find('span', {'class': 'cooktime'})  
# ingredients
singredients = test.find('div', {'class': 'recipe-ingredients'}).find_all('li')
# instructions
sinstructions = test.find('div', {'itemprop': 'recipeInstructions'}).find_all('p')

for links in linkss.find_all('h3', attrs={'class' : 'r'}):
    print links.string

#for x in singredients:
#	string = singredients
#print (singredients)
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

#print ingredients  
#print get_minutes(scook)















