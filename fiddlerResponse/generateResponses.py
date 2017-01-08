#!/usr/bin/python
import os.path
import time


VALID_FILE_EXTENSIONS = ['.js']
FIDDLER_HEADERS_FILE = 'D:\workspaces\chromeWorkSpaces\javascript_headers.txt';



def isValidFile(filename) :
	extension = os.path.splitext(filename)[1]
	return extension in VALID_FILE_EXTENSIONS;
   
   
def getAssociatedFiddlerResponseFile(filename) :
	baseFileName = os.path.splitext(filename)[0];
	return baseFileName + '_response.txt'


def writeFiddlerHeaddersFile(outFile, contentSize) :
	with open(FIDDLER_HEADERS_FILE, 'r') as inFile:
			for line in inFile :
				outFile.write(line.replace('$SIZE$', str(contentSize)))
	return

	
  
def updateFiddlerFileIfNecesary(parent, filename) :		
	fiddlerResponseFile = os.path.join(parent, getAssociatedFiddlerResponseFile(filename))
	bodyFile = os.path.join(parent, filename);
	contentSize = os.path.getsize(bodyFile);
	
	with open(fiddlerResponseFile, 'w') as outFile:
		writeFiddlerHeaddersFile(outFile, contentSize)
		outFile.write('\n')
		with open(bodyFile, 'r') as infile:
			outFile.write(infile.read())
	return


	
def inspectFilesInDirectory(rootDir) :
	print "\nchecking files in directory %s" % rootDir
	
	for root, directories, filenames in os.walk(rootDir):
		for filename in filenames:
			if isValidFile(filename) :
				print os.path.join(root,filename)
				updateFiddlerFileIfNecesary(root, filename)
			else :
				print "Not a valid file: %s" % filename
	return
	

	
try:
	while True:
		inspectFilesInDirectory('D:/workspaces/chromeWorkSpaces')
		time.sleep(5)		
except KeyboardInterrupt:
    pass
	
print("Bye")			