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

#url='https://wiki.engr.illinois.edu/display/cs411sp13/Schedule'
#url = 'http://courses.engr.illinois.edu/cs433/assignments.html'
#url = 'http://cse1.net/lectures'
#url = 'http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-spring-2008/lecture-notes/'	

def find_pdf(url):
	if url.find(".pdf") > 0:
		return True
	return False
def find_doc(url):
	if url.find(".doc") > 0:
		return True
	return False
def find_ppt(url):
	if url.find(".ppt") > 0:
		return True
	return False

def grab_files(url):
	
	mech = mechanize.Browser()
	mech.set_handle_robots(False)
	try:
		mech.open(url, timeout = 30.0)
		links = mech.links()	
	except:
		return


	#file ID is a number from 0x0000 to 0xffff. We should have an interface that keeps tracks of the maxID and issues the starting ID tag to this code.
	pdfID =0x0000

	for l in links:
		path = urljoin(str(l.base_url),str(l.url))
		#Make a unique ID : first a 12-bit key attribute for out future database, then the date for file version.
		generate_file_id = str(bin(pdfID))[2:].zfill(CONST_BITMAPSIZE)+"_"+str(date.today())+"_"
		#Grab file name from URL
		url_parts_array = path.split('/')
		filename = url_parts_array[len(url_parts_array)-1]

		#For future reference : Index in database instead of downloading the files.
		#So far, only supporting ppt/doc/pdfs
		if find_pdf(path):
			filename = filename[0:filename.find(".pdf")+4]
			urllib.urlretrieve(path, generate_file_id+filename)
			pdfID=(pdfID+1)%0xFFFF

		elif find_ppt(path):
			if path.find(".pptx") > 0 :
				filename = filename[0:filename.find(".pptx")+5]
			else: 
				filename = filename[0:filename.find(".ppt")+4]
			urllib.urlretrieve(path, generate_file_id+filename)
			pdfID=(pdfID+1)%0xFFFF

		elif find_doc(path):
			if path.find(".docx") > 0 :
				filename = filename[0:filename.find(".docx")+5]
			else: 
				filename = filename[0:filename.find(".doc")+4]
			urllib.urlretrieve(path, generate_file_id+filename)
			pdfID=(pdfID+1)%0xFFFF
