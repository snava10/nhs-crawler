# nhs-crawler
A service to scrape the nhs public conditions pages. Rest endpoint to search.

## Requirements
- Java
- Elasticsearch
- Python 2.7
- The following python modules:
  - requests
  - BeautifulSoup
  - urlparse
  - elasticsearch
  - flask
  - mock (only to run the tests)

## Usage
- Open a console and run `python nhsWebCrawler.py <elasticsearchServer>`.
  - This will start crawling the nhs website,
  - Index the content of the pages in elasticsearch and
  - Store the url, title and content in a file called `nhsPageContent` in json format.
  - Please be aware that this could take some minutes to complete, depending on your internet connection.

- Run `python webApi.py` to start the Rest Api's
  - The address for the elasticsearch server is defaulted to localhost:9200, if another server is used the file `webApi.py` must be edited in consequence.
 
- To start using the api, open a browser and enter `http://localhost:5000/`
- The search will return the top links that match the search criteria, sorted by relevance. 
