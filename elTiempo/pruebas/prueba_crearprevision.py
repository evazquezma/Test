# coding: UTF-8
import xml.etree.ElementTree as ET
import urllib2

import threading
import time

RSS_CONCELLO_HOY = 'http://servizos.meteogalicia.es/rss/predicion/rssLocalidades.action?idZona=27031&dia=0'
RSS_CONCELLO_DIA1 = 'http://servizos.meteogalicia.es/rss/predicion/rssLocalidades.action?idZona=27031&dia=1'
RSS_CONCELLO_DIA2 = 'http://servizos.meteogalicia.es/rss/predicion/rssLocalidades.action?idZona=27031&dia=2'

PATH_TEMPLATE = 'D:/repos/git/python/elTiempo/resources/template_prevision.txt'


dictIconosCielo = {-9999: 'no disponible', \
	101: 'despejado', \
	102: 'con nubes altas', \
	103: 'con nubes y claros', \
	104: 'achubascado 75 por ciento', \
	105: 'cubierto', \
	106: 'con nieblas', \
	107: 'con chuvasco', \
	108: 'con chuvasco (75 por ciento)', \
	109: 'con chuvasco nieve', \
	110: 'con orballo', \
	111: 'con lluvia', \
	112: 'con nieve', \
	113: 'con treboada', \
	114: 'con niebla', \
	115: 'con bancos de niebla', \
	116: 'con nubes medias', \
	117: 'con lluvia débil', \
	118: 'con chuvascos débiles', \
	119: 'con treboada con pocas nubes', \
	120: 'con agua nieve', \
	121: 'con sarabia', \
	201: 'despejado', \
	202: 'con nubes altas', \
	203: 'con nubes y claros', \
	204: 'con achubascado 75 por ciento', \
	205: 'con cubierto', \
	206: 'con nieblas', \
	207: 'con chuvasco', \
	208: 'con chuvasco (75 por ciento)', \
	209: 'con chuvasco nieve', \
	210: 'con orballo', \
	211: 'con lluvia', \
	212: 'con nieve', \
	213: 'con treboada', \
	214: 'con niebla', \
	215: 'con bancos de niebla', \
	216: 'con nubes medias', \
	217: 'con lluvia débil', \
	218: 'con chuvascos débiles', \
	219: 'con treboada con pocas nubes', \
	220: 'con agua nieve', \
	221: 'con sarabia'}

dictIconosViento = {-9999: 'No disponible', \
	299: 'viento en calma', \
	300: 'viento variable', \
	301: 'viento flojo del norte (N)', \
	302: 'viento flojo del nordés (NE)', \
	303: 'viento flojo del este (E)', \
	304: 'viento flojo del sueste (SE)', \
	305: 'viento flojo del sur (S)', \
	306: 'viento flojo del sudoeste (SO)', \
	307: 'viento flojo del oeste (O)', \
	308: 'viento flojo del noroeste (NO)', \
	309: 'viento moderado del norte (N)', \
	310: 'viento moderado del nordés (NE)', \
	311: 'viento moderado del este (E)', \
	312: 'viento moderado del sueste (SE)', \
	313: 'viento moderado del sur (S)', \
	314: 'viento moderado del sudoeste (SO)', \
	315: 'viento moderado del oeste (O)', \
	316: 'viento moderado del noroeste (EN El)', \
	317: 'viento fuerte del norte (N)', \
	318: 'viento fuerte del nordés (NE)', \
	319: 'viento fuerte del este (E)', \
	320: 'viento fuerte del sueste (SE)', \
	321: 'viento fuerte del sur (E)', \
	322: 'viento fuerte del sudoeste (SO)', \
	323: 'viento fuerte del oeste (O)', \
	324: 'viento fuerte del noroeste (EN El)', \
	325: 'viento muy fuerte del norte (N)', \
	326: 'viento muy fuerte del nordés (NE)', \
	327: 'viento muy fuerte del este (E)', \
	328: 'viento muy fuerte del sueste (SE)', \
	329: 'viento muy fuerte del sur (S)', \
	330: 'viento muy fuerte del sudoeste (SO)', \
	331: 'viento muy fuerte del oeste (O)', \
	332: 'viento muy fuerte del noroeste (NO)'}

	
# ********************************************* #
# ********************************************* #
# ********************************************* #
class Prevision :
	tMax = 99
	tMin = -99
	idCieloMorning = -1
	idVientoMorning = -1
	probLluviaMorning = -1
	idCieloEvening = -1
	idVientoEvening = -1
	probLluviaEvening = -1
	idCieloNight  = -1
	idVientoNight = -1
	probLluviaNight = -1
	
	def __init__(self):
		#nada que poner de momento
		print "creando objeto prevision"
		
	def __str__( self ):
		return "temperaturas: [{} - {}]. Morning: [{} - {} -{}]. Evening: [{} - {} -{}]. Night: [{} - {} -{}]"\
				.format(self.tMax, self.tMin, \
						self.idCieloMorning, self.idVientoMorning, self.probLluviaMorning, \
						self.idCieloEvening, self.idVientoEvening, self.probLluviaEvening, \
						self.idCieloNight, self.idVientoNight, self.probLluviaNight)


# ********************************************* #
# ********************************************* #
# ********************************************* #

def parsearPrediccionRSS(rssBody):
	tree = ET.fromstring(rssBody)
	entry = tree.findall('./channel/item')[0]
		
	prevision = Prevision()
	prevision.date = entry[5].text	
	prevision.tMax = int(entry[10].text)
	prevision.tMin = int(entry[11].text)
	prevision.idCieloMorning  = int(entry[12].text)
	prevision.idVientoMorning = int(entry[15].text)
	prevision.probLluviaMorning = int(entry[18].text)
	prevision.idCieloEvening  = int(entry[13].text)
	prevision.idVientoEvening = int(entry[16].text)
	prevision.probLluviaEvening = int(entry[19].text)
	prevision.idCieloNight  = int(entry[14].text)
	prevision.idVientoNight = int(entry[17].text)
	prevision.probLluviaNight = int(entry[20].text)
	
	return prevision
	

def cargarTemplate(path):
	with open(path, 'r') as myfile:
		data = myfile.read()
	return data.decode('utf-8')
	
	
def volcarPrevisionAFichero(prevision, template):
	texto = template
	
	texto = texto.replace('${TMAX}', str(prevision.tMax)).replace('${TMIN)', str(prevision.tMin))
	texto = texto.replace('${CIELO_MORNING}', dictIconosCielo[prevision.idCieloMorning]).replace('${VIENTO_MORNING}', dictIconosViento[prevision.idVientoMorning]).replace('${LLUVIA_MORNING}', str(prevision.probLluviaMorning))
	texto = texto.replace('${CIELO_EVENING}', dictIconosCielo[prevision.idCieloEvening]).replace('${VIENTO_EVENING}', dictIconosViento[prevision.idVientoEvening]).replace('${LLUVIA_EVENING}', str(prevision.probLluviaEvening))
	texto = texto.replace('${CIELO_NIGHT}', dictIconosCielo[prevision.idCieloNight]).replace('${VIENTO_NIGHT}', dictIconosViento[prevision.idVientoNight]).replace('${LLUVIA_NIGHT}', str(prevision.probLluviaNight))
	
	
	print texto
	
	with open('prevision_hoy.txt', 'w') as myfile:
		myfile.write(texto.encode('utf-8'))
	
	return 0


	
def main():
	# my code here
	response = urllib2.urlopen(RSS_CONCELLO_HOY)	
	previsionHoy = parsearPrediccionRSS(response.read())
	
	response = urllib2.urlopen(RSS_CONCELLO_DIA1)	
	previsionManana = parsearPrediccionRSS(response.read())
	
	response = urllib2.urlopen(RSS_CONCELLO_DIA2)	
	previsionPasado = parsearPrediccionRSS(response.read())
	
	print "Prevision para hoy {}".format(previsionHoy)
	print "Prevision para manaha {}".format(previsionManana)
	print "Prevision para pasado {}".format(previsionPasado)
	

	template = cargarTemplate(PATH_TEMPLATE)
	volcarPrevisionAFichero(previsionManana, template)
	
	
	
	
if __name__ == "__main__":
	main()