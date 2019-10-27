import re

# Extract the domain from the url
def get_domain(url):

	if re.search('^https://', url):
		domain = re.findall('^https://([^/]*)', url)[0]
	else:
		domain = re.findall('^http://([^/]*)', url)[0]
	return domain
