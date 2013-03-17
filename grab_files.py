import mechanize
import urllib
import urllib2
import sys
from urlparse import urljoin

#timestamp for file IDs
import time
from datetime import date

CONST_BASESIZE = 16
CONST_BITMAPSIZE = 16

mech = mechanize.Browser()
mech.set_handle_robots(False)

#use beautifulsoup to browse and generate these URLs.
url='https://wiki.engr.illinois.edu/display/cs411sp13/Schedule'
#url = 'http://courses.engr.illinois.edu/cs433/assignments.html'
#url = 'http://cse1.net/lectures'
try:
	mech.open(url, timeout = 30.0)
except HTTPError, e:
	sys.exit("%d: %s" % (e.code, e.msg))

links = mech.links()
#for j in links:
	#if str(j).find(".pdf") > 0:
	#	print(j)

#file ID is a number from 0x0000 to 0xffff. We should have an interface that keeps tracks of the maxID and issues the starting ID tag to this code.
pdfID =0x0000

for l in links:
	path = urljoin(str(l.base_url),str(l.url))
	print(path)
	#Make a unique ID : first a 12-bit key attribute for out future database, then the date for file version.
	generate_file_id = str(bin(pdfID))[2:].zfill(CONST_BITMAPSIZE)+"_"+str(date.today())+"_"
	#Grab file name from URL
	url_parts_array = path.split('/')
	filename = url_parts_array[len(url_parts_array)-1]

	if path.find(".pdf") > 0:
		filename = filename[0:filename.find(".pdf")+4]
		#Instead of downloading the file, maybe it's better to index the file in database.
		urllib.urlretrieve(path, generate_file_id+filename)
		pdfID=(pdfID+1)%0xFFFF;
	elif path.find(".ppt") > 0 :
		filename = filename[0:filename.find(".ppt")+4]
		#Instead of downloading the file, maybe it's better to index the file in database.
		urllib.urlretrieve(path, generate_file_id+filename)
		pdfID=(pdfID+1)%0xFFFF;
