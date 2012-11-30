import urllib2
from BeautifulSoup import BeautifulSoup

reviewPageURL = 'http://www.glassdoor.com/Reviews/Shell-Oil-Company-Reviews-E5833_P2.htm'
request = urllib2.Request(reviewPageURL)
response = urllib2.urlopen(request)
soup = BeautifulSoup(''.join(response.read()))

print soup
