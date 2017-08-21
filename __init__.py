from binaryninja import *
import requests
import json
from bs4 import BeautifulSoup
import epdb

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

def search_and_render(bv):
    search_this = get_text_line_input('function name', 'Query MSDN API')
    render(bv, search_this)

def render(bv, search):
	url = getAPIUrlFor(search)
    	if url:
        	doc = getDocsFrom(url)
        	template = "<html><body>%s</body></html>" % doc
		show_html_report(search + " result", template)
	else:
        	log_info("no documentation found for '%s'" % search)

def search_and_render_addr(bv, addr):
    block = bv.get_basic_blocks_at(addr)[0]
    if not block:
        log_warning("Block at address '0x%08x' not found" % addr)
        return

    il = block.function.get_lifted_il_at(addr)

    if not il:
        log_warning("Intermediate instruction at address '0x%08x' not found" % addr)
        return

    if il.operation == LowLevelILOperation.LLIL_CALL:
        call_addr = il.dest.operands[0].operands[0]
        sym = bv.get_symbol_at(call_addr)
        if not sym:
            log_warning("Symbol at address '0x%08x' not found" % call_addr)
            return

        sym_name = sym.name
        if "!" in sym_name and "@" in sym_name:
            function_name = sym_name.split("!")[1].split("@")[0]
            render(bv, function_name)
        else:
            render(bv, sym_name)

PluginCommand.register("Search MSDN", "Searches the MSDN Api and displays the first result if found.", search_and_render)
PluginCommand.register_for_address('Search MSDN from instruction', 'Search MSDN for call from instruction', search_and_render_addr)
