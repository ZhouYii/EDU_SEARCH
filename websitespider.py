from bs4 import BeautifulSoup
from urlparse import urljoin
from copy import deepcopy
import urllib
import mechanize
import grab_files

url_set = set()

def crawl(url, depth):
	print("DEPTH TYPE: " + str(type(depth)) + " DEPTH: " + str(depth))
	global url_set
	if depth<=0:
		return 1
	if(depth >0):
		print("NOW CRAWLING : "+str(url))
		#Grab files at root URL
		grab_files.grab_files(url)

		#Recursively visit next tree level
		mech = mechanize.Browser()
		mech.set_handle_robots(False)
		try:
			mech.open(url, timeout = 30.0)
			links = mech.links()
		except:
			return depth +1

		for entry in links:
			child_url = str(urljoin(str(entry.base_url),str(entry.url)))
			#ignore anchor tags
			if child_url.find('#')!=-1:
				child_url=str(child_url[0:child_url.find('#')+1])
			if child_url not in url_set:
				url_set.add(child_url)
				print("2DEPTH TYPE: " + str(type(depth)) + " DEPTH: " + str(depth))
				#print ("EMBARKING ON " + str(child_url))
				depth = crawl(child_url, depth-1)
		return depth+1	

url_set.clear()
crawl ('http://courses.engr.illinois.edu/cs433/', 3)
