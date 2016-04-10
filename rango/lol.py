import re
import json
import urllib2
import requests
import urllib
from HTMLParser import HTMLParser
url = raw_input('Enter - ')
r = requests.get(url)
# req = urllib2.Request(url)
# req.add_header({'User-agent': 'Mozilla/5.0',"Host": url})
# html = urllib2.urlopen(req).read()
# opener = urllib2.build_opener()
# opener.addheaders={"Host": url}
# html = opener.open(url)
# html = urllib2.urlopen(url).read()
html=r.text
terms=[]
# print(type(html))
class MyHTMLParser(HTMLParser):
    # def handle_starttag(self, tag, attrs):
        # print "Start tag:", tag
        # for attr in attrs:
            # print "     attr:", attr
    # def handle_endtag(self, tag):
        # print "End tag  :", taga

    def handle_data(self, data):
        data=data.strip()
        if data != "":
            terms.append(data)
        # for data in data:
        #     if data!= "\0":
        #         print data
parser = MyHTMLParser()
parser.feed(html)
translations=[]
for line in terms:
    p= re.compile('[a-z]|[A-Z]')
    if p.match(line):
        translations.append(line)
# print terms
# print '\n'.join(translations)
# json = json.dumps(translations,ensure_ascii=False)

def translate(to_translate, to_langage="auto", langage="auto"):
    '''Return the translation using google translate
	you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
	if you don't define anything it will detect it or use english by default
	Example:
	print(translate("salut tu vas bien?", "en"))
	hello you alright?'''
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, to_translate.replace(" ", "+"))
    request = urllib2.Request(link, headers=agents)
    # request = requests.get(link)
    page = urllib2.urlopen(request).read()
    # page=request.text
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return result
res=[]
print translations
if __name__ == '__main__':
    for each in translations:
        to_translate = each
        # print("%s >> %s" % (to_translate, translate(to_translate)))
        # res[each]=translate(to_translate, 'hi')
        ans=translate(to_translate, 'hi')
        res.append(ans)
        # print("%s >> %s" % (to_translate, translate(to_translate, 'hi')))
        # print "Sumedh: " +  translate(to_translate, 'hi')
	#should print Hola como estas >> Hello how are you
	#and Hola como estas? >> Bonjour comment allez-vous?
# s="hello, my name is binoy. i is an isiot"
for i in range (len(res)):
    html=html.replace(translations[i],res[i])
    # s=s.replace("is","was")
text_file = open("Output.html", "w+")
text_file.write(html)
text_file.close()
