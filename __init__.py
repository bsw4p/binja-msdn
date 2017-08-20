from binaryninja import *
import requests
import json
from bs4 import BeautifulSoup

def getSoupFrom(url):
    r = requests.get(url)

    if not (r.status_code == 200):
        raise Exception("Could not grab url '%s'" % url)

    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get(html_id, from_url):
    return getSoupFrom(from_url).find(id=html_id)

def getDocsFrom(url):
    return get("content", from_url=url)

def searchForResult(in_tag):
    if len(in_tag.contents) > 0:
        if "results" in in_tag.contents[0]:
            return True
    return False

def getAPIUrlFor(function):
    search_url = "https://social.msdn.microsoft.com/search/en-US/windows?query=%s"
    s = getSoupFrom(search_url % function)

    scripts = filter(searchForResult, s.find_all("script"))[0]
    results_json = filter(lambda x: "var results" in x, scripts.contents[0].split("\r\n"))[0].strip()[14:-1]
    parsed_results = json.loads(results_json)
    links = parsed_results['data']['results']

    return links[0]['url']

def render(bv):
	search_this = get_text_line_input('function name', 'Query MSDN API')
	url = getAPIUrlFor(search_this)
    	if url:
        	doc = getDocsFrom(url)
        	template = "<html><body>%s</body></html>" % doc
		show_html_report(search_this + " result", template)
	else:
        	log_info("no documentation found for '%s'" % search)

PluginCommand.register("Search MSDN", "Searches the MSDN Api and displays the first result if found.", render)
