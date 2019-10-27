import re

gen_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language':'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate',
                   'Connection':'keep-alive'}

def isHttps(url):

	if re.search('^https://', url):
		return True
	return False







