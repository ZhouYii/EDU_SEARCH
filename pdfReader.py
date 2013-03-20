import pyPdf
import MySQLdb
import sys
 
def convertPdf2String(path):
    	content = ""
    	# load PDF file
    	pdf = pyPdf.PdfFileReader(file(path, "rb"))
    	# iterate pages
    	for i in range(0, pdf.getNumPages()):
        	# extract the text from each page
        	content += pdf.getPage(i).extractText() + " "
    	# collapse whitespaces
    	#content = u" ".join(content.replace(u"xa0", u" ")#.strip().split())
    	dictionary = dict()
	textarray = content.lower().replace('\'', '').replace('"','').split(' ')
	for entry in textarray:
		if(entry not in dictionary):
			dictionary[entry] = 1
		else:
			dictionary[entry] += 1
   	return dictionary

def getDbConn(host, user, password, db):
	return MySQLdb.connect(host, user, password, db)

def getMaxDocID(dbConn):
	maxCursor = dbConn.cursor()
	sql = 'SELECT max(doc_id) FROM documents'
	maxCursor.execute(sql)
	return maxCursor.fetchone()

#Find filepath and extract filename
filepath = '0000000000000001_2013-03-17_cs433-sp13-hw1.pdf'
filenameArray = filepath.split('\\')
filename = filenameArray[len(filenameArray)-1]

db = getDbConn('127.0.0.1', 'root', '', 'edu')
cursor = db.cursor()

wordDict= convertPdf2String(filepath)
newDocId = getMaxDocID(db)[0] + 1
try:
	cursor.execute('INSERT INTO documents VALUES ("'+str(filename)+'",'+str(newDocId)+')')
	for key in wordDict:
		if(not key == ''):
			print(key)
			sql = 'INSERT INTO reverse_indicies VALUES ('+str(newDocId)+',"'+str(key)+'","'+str(wordDict[key])+'")'
			print(sql)
			cursor.execute(sql)

	
except MySQLdb.Error,e:
    print e[0],e[1]
    db.rollback()
    cursor.close()
    db.close()
    #print lengthy error description!!
    sys.exit(2)
	
db.commit()
