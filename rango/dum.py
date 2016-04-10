import urllib
import re
import json
import urllib2
import requests
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import unicodedata


def accept(url,lang1):
#url = raw_input('Enter - ')
#lang1 = raw_input("Enter target language - ")
	lang=""
	if lang1 == "english":
	    lang = "en"
	elif lang1 == "hindi":
	    lang = "hi"
	elif lang1 == "marathi":
	    lang = "mr"
	elif lang1 == "gujarati":
		lang = "gu"
	elif lang1 == "bengali":
		lang = "bn"
	elif lang1 == "malayalam":
		lang = "ml"
	elif lang1 == "kannada":
		lang = "kn"
	# html = urllib.urlopen(url).read()
	str = "http://translate.google.com/translate?sl=en&tl="+lang+"&u="+url
	# url = "http://translate.google.com/translate?sl=en&tl=hi&u=url"
	url = str
	print url
	r = requests.get(url)
	html=r.text
	terms=[]
	soup = BeautifulSoup(html)
	#Retreive list of anchor tags
	# tags = soup('a')
	text_file = open("Output1.html", "w")
	text_file.write(html.encode('utf-8'))
	text_file.close()

	return html