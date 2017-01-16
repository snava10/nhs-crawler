
import unittest
from mock import MagicMock
from webApi import *

class TestWebApiMethods(unittest.TestCase):
	def test_search(self):
		body = {
		"query": {
				"multi_match":{
					"query" : 'mock search',
					"fields": ["content","title"]
				}
			},
			"size":10
		}
		es.search = MagicMock(index=indexName, doc_type=docType, filter_path=['hits.hits._source.url'], body=body)
		es.search.return_value = dict()
		search('mock search')
		es.search.assert_called_with(index=indexName, doc_type=docType, filter_path=['hits.hits._source.url'], body=body)

	def test_search_if_no_results_should_return_the_default_message(self):
		es.search = MagicMock(index=indexName, doc_type=docType, filter_path=['hits.hits._source.url'], body=None)
		es.search.return_value = dict()
		res = search('mock search')
		self.assertTrue(res == noResultsMessage)

if __name__ == '__main__':
    unittest.main()