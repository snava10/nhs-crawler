import requests
from bs4 import BeautifulSoup
import re
from urlparse import urlparse
import json
from elasticsearch import Elasticsearch
import sys

class PageInfoModel:
	def __init__(self,title,url,content):
		self.title = title
		self.url = url
		self.content = content

	def to_json(self):
		return json.dumps(self.__dict__)

def get_pages_info_models(startUrl,depth=2,printLog=True):
	mainUrl = urlparse(startUrl)
	raw = requests.get(startUrl).content
	soup = BeautifulSoup(raw,'html.parser')
	yield get_model(soup,startUrl)
	reviewedUrls = set([startUrl])
	if not depth:
		raise StopIteration

	nextUrls = [(link,1) for link in get_condition_links(soup)]

	while len(nextUrls):
		(link, currentDepth) = nextUrls.pop(0)
		url = '{}://{}{}'.format(mainUrl.scheme,mainUrl.netloc,link)
		if url in reviewedUrls:
			continue
		if printLog:
			print('Analyzing  {}'.format(url))
		raw = requests.get(url).content
		soup = BeautifulSoup(raw,'html.parser')
		yield get_model(soup,url)
		reviewedUrls.add(url)
		if currentDepth < depth:
			nextUrls.extend([(link,currentDepth+1) for link in get_content_links(soup)])


def get_content_links(soup):
	contentDiv = soup.select_one("div .content-wrap")
	return [link.get('href') for link in contentDiv.find_all('a') 
			if link.get('href') is not None and link.get('href').lower().startswith('/conditions')]

def get_condition_links(soup):
	return [link.get('href') for link in soup.find_all('a') if link.get('href').lower().startswith('/conditions')]

def get_page_content(soup):
	#remove javascript and styles
	for script in soup(['script','style']):
		script.decompose()
	text = soup.get_text()

	#remove unnecessary spaces
	text = re.sub('\s+',' ',text)

	return text.strip()

def get_model(soup,url):
	return PageInfoModel(soup.title.string,url,get_page_content(soup))

def run(args):
	elasticsearchServer = args[0] if len(args) else 'localhost:9200'
	indexName = 'nhs_conditions'
	docType = 'condition'

	es = Elasticsearch(elasticsearchServer)
	es.indices.delete(index=indexName, ignore=[400,404])

	f = open('nhsPageContent','w')
	f.write('[')
	for model in get_pages_info_models('http://www.nhs.uk/Conditions/Pages/hub.aspx'):
		json = model.to_json()
		es.index(index=indexName, doc_type=docType, body=json)
		f.write(json + ",\n")
	
	f.write(']')
	f.close()
	es.indices.refresh(index=indexName)

if __name__ == '__main__':
	run(sys.argv[1:])
	