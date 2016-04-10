import urllib
import re
import json
import urllib2
import requests
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import unicodedata

terms=[]
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
url =""
lang_code=""
def accept(uri,lang):
    url=uri
    lang_code=lang
    response=trans(url)
    return response
# html = urllib.urlopen(url).read()
def trans(url):
    r = requests.get(url)
    html=r.text
    
    soup = BeautifulSoup(html)
#Retreive list of anchor tags
    tags = soup('a')
# print tags
#print soup
    for tag in tags:
        print tag.get('href', None)
# print(type(html))
    
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
    res=[]
    if __name__ == '__main__':
        for each in translations:
            to_translate = each
        #print("%s >> %s" % (to_translate, translate(to_translate)))
        # res[each]=translate(to_translate, 'hi')
            ans = translate(to_translate, 'hi')
            res.append(ans)
    for i in range (len(res)):
        html=html.replace(translations[i],res[i])
    # s=s.replace("is","was")
    print res
    return html.encode('utf-8')
    text_file = open("Output.html", "w")
    text_file.write(html.encode('utf-8'))
    text_file.close()
# print terms
# print '\n'.join(translations)
# json = json.dumps(translations,ensure_ascii=False)

def translate(to_translate, to_langage, langage="auto"):
    '''Return the translation using google translate
    you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
    if you don't define anything it will detect it or use english by default
    Example:
    print(translate("salut tu vas bien?", "en"))
    hello you alright?'''
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, to_translate.replace(" ", "+"))
    '''request = urllib2.Request(link, headers=agents)
    page = urllib2.urlopen(request).read()'''
    request=requests.get(link)
    page=request.text
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return result

        #print("%s >> %s" % (to_translate, translate(to_translate, 'hi')))
        # print "Sumedh: " +  translate(to_translate, 'hi')
    #should print Hola como estas >> Hello how are you
    #and Hola como estas? >> Bonjour comment allez-vous?


'''
newjson={}
newjson['data']=translations
final=json.dumps(newjson,ensure_ascii=False)
print final
headers = {"Content-Type": "application/json", "Accept": "application/json", "REV-API-KEY": "4PtxtYemYvKvgNTRGo0srL1CKoN2EqCBiITz", "REV-APP-ID": "Axis_hack"}
# dat= '{"data":'+json+'}, "http://sandbox.reverieinc.com/v2/lo"'
url = 'http://sandbox.reverieinc.com/v2/localization?target_lang=hindi&source_lang=english'
req = urllib2.Request(url, data=final, headers=headers)
f = urllib2.urlopen(req)
for x in f:
    print(x)
f.close()
'''