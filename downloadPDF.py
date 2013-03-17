import httplib2
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()
status, response = http.request('http://courses.engr.illinois.edu/cs433/assignments.html')

for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        print link['href']

