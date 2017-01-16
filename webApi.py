

#!flask/bin/python
from flask import Flask, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('localhost:9200')
indexName = 'nhs_conditions'
docType = 'condition'
noResultsMessage = 'We could not find any relevant results, please refine your search'

@app.route('/')
def index():
    return "Welcome to our nhs search api. The search endpoint is: /search/<text>"

@app.route('/search/<string:text>', methods=['GET'])
def search(text):
	body = {
		"query": {
			"multi_match":{
				"query" : text,
				"fields": ["content","title"]
			}
		},
		"size":10
	}
	res = es.search(index=indexName, doc_type=docType, filter_path=['hits.hits._source.url'], body=body)
	resList = []
	try:
		for doc in res['hits']['hits']:
			resList.append(doc['_source']['url'])
		return jsonify(resList)
	except KeyError as e:
		return noResultsMessage
	else:
		pass
	finally:
		pass
	

	return noResultsMessage


if __name__ == '__main__':
    app.run(debug=True)