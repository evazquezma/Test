import feedparser
import urllib

import threading
import time

RSS_VOZ_URL = 'http://servizos.meteogalicia.gal/rss/predicion/rssCortes.action?request_locale=gl'


class myThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self._stop = threading.Event()
		
	def run(self):
		print "Starting " + self.name	
		print ("Total score for {} is {}".format(self.name, self.counter))
		while True:
			time.sleep(1)
			if self.stopped() :
				break
			print 'runing...'
		print "Exiting " + self.name
		
	def stop(self):
		self._stop.set()
		
	def stopped(self):
		return self._stop.isSet()



		
		
def descargaFichero(url, destino):
	urlOpener = urllib.URLopener()
	urlOpener.retrieve(url, destino)

def main():
	# my code here
	rss = feedparser.parse(RSS_VOZ_URL)
	print rss.channel['link']
	print rss.entries[0].date
	print rss.entries[0].link

	thread1 = myThread(1, "Thread-1", 1)
	thread1.start()
	
	descargaFichero(rss.entries[0].link, 'galiciaMorning.mp3')
	descargaFichero(rss.entries[1].link, 'galiciaEvening.mp3')
	
	descargaFichero(rss.entries[12].link, 'lugoMorning.mp3')
	descargaFichero(rss.entries[13].link, 'lugoEvening.mp3')	
	
	thread1.stop()

if __name__ == "__main__":
	main()