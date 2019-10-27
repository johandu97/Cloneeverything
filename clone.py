from library.domain_helpers import *
from library.http_helpers import *
from library.file_helpers import *
from bs4 import BeautifulSoup
from urllib import parse
from termcolor import colored
import requests
import sys
import re
		
class Clone():

	__components = ['js', 'css', 'images']
	__imageExtension = ['jpg', 'png', 'svg']

	def __init__(self, url, delay=0, directory='website'):

		self.url = url
		self.delay = delay
		self.directory = directory
		self.__count_js = 0
		self.__count_img = 0
		self.__count_css = 0
		self.session = requests.Session()

	# Run the entire cloning process
	def run(self):

		# Initialize information
		os.makedirs(self.directory)
		os.chdir(self.directory)

		create_file('js_log')
		create_file('css_log')
		create_file('img_log')

		for component in Clone.__components:
			os.makedirs(component)

		print(colored('[-] Cloning the site ...\n', 'blue'))
		print(colored('Url: ', 'yellow') + self.url)

		
		res = self.session.get(self.url, headers=gen_headers)
		print (res.request.headers, 'red')
		print(colored('Response code: ', 'yellow') + str(res.status_code))
		print('-' * 80)

		html_string = res.text
		soup = BeautifulSoup(html_string, 'html.parser')

		# Extract all linked files from script tag
		scripts = soup.find_all('script')
		print(colored('[-] Extracting all linked files from script tag\n', 'blue'))
		self.__extract_script_tag(scripts)

		# Extract all linked files from link tag
		links = soup.find_all('link')
		print(colored('[-] Extracting all linked files from link tag\n', 'blue'))
		self.__extract_link_tag(links)
	
		# Extract all linked files from img tag
		imgs = soup.find_all('img')
		print(colored('[-] Extracting all linked files from img tag\n', 'blue'))
		self.__extract_img_tag(imgs)

		
		# Extract all linked files from style attribute
		style = soup.find_all(attrs={"style":True})
		print(colored('[-] Extracting all linked files from style attribute\n', 'blue'))
		self.__extract_style_attr(style)
		
		
		# Create the index.html
		print(colored('[-] Creating the file index.html\n', 'blue'))
		prettyHTML = soup.prettify()
		write_file('index.html', prettyHTML)

		write_file_append('js_log', 'Total: ' + str(self.__count_js) + '\n')
		write_file_append('css_log', 'Total: ' + str(self.__count_css) + '\n')
		write_file_append('img_log', 'Total: ' + str(self.__count_img) + '\n')

	# Extract all linked files from script tag
	def __extract_script_tag(self, scripts):

		for script in scripts:
			if script.get('src'):
				url_latest = parse.urljoin(self.url, script.get('src'))
				if get_domain(self.url) == get_domain(url_latest):
					flag = False
					for url in read_file_line('js_log'):
						if url.strip() == url_latest:
							flag = True
							break
					if isHttps(self.url) == True:	
						path = re.findall('https://[^/]*/(.*)', url_latest)[0]
					else:
						path = re.findall('http://[^/]*/(.*)', url_latest)[0]
					path = 'js/' + path
					if flag == True:
						script['src'] = path
						continue
					path_dir = os.path.dirname(path)
					if not os.path.isdir(path_dir):
						os.makedirs(path_dir)
					self.__count_js += 1
					write_file_append('js_log', url_latest + '\n')
					print(colored('Url javascript: ', 'yellow') + url_latest)
				
					res = self.session.get(url_latest, headers=gen_headers)
					print(colored('Response code: ', 'yellow') + str(res.status_code))
					write_file_binary(path, res.content)
					print(colored('[!] Create successful javascript file!', 'white'))
					script['src'] = path
			
					print('-' * 80)

	# Extract all linked files from links tag
	def __extract_link_tag(self, links):

		for link in links:
			if link.get('href'):
				url_latest = parse.urljoin(self.url, link.get('href'))
				if get_domain(self.url) == get_domain(url_latest):
					if isHttps(self.url) == True:	
						path = re.findall('https://[^/]*/(.*)', url_latest)[0]
					else:
						path = re.findall('http://[^/]*/(.*)', url_latest)[0]
					# Checking CSS
					if re.search('.css$', link.get('href')):
						flag = False
						path_css = 'css/' + path
						for url in read_file_line('css_log'):
							if url.strip() == url_latest:
								link['href'] = path_css
								flag = True
								break
						if flag == True:
							continue
						path_dir_css = os.path.dirname(path_css)
						if not os.path.isdir(path_dir_css):
							os.makedirs(path_dir_css)
						self.__count_css += 1
						write_file_append('css_log', url_latest + '\n')
						print(colored('Url css: ', 'yellow') + url_latest)
	
						res = self.session.get(url_latest, headers=gen_headers)
						print(colored('Response code: ', 'yellow') + str(res.status_code))
						data = self.__extract_css_content(res.text, url_latest)
						write_file_binary(path_css, data.encode())
						print(colored('[!] Create successful css file!', 'white'))
						link['href'] = path_css
						
						print('-' * 80)

	# Extract all linked files from img tag
	def __extract_img_tag(self, imgs):
		
		for img in imgs:
			if img.get('src'):
				url_latest = parse.urljoin(self.url, img.get('src'))
				if get_domain(self.url) == get_domain(url_latest):
					flag = False
					if isHttps(self.url) == True:	
						path = re.findall('https://[^/]*/(.*)', url_latest)[0]
					else:
						path = re.findall('http://[^/]*/(.*)', url_latest)[0]
					path = 'images/' + path
					for url in read_file_line('img_log'):
						if url.strip() == url_latest:
							flag = True
							img['src'] = path
							break
					if flag == True:
						continue
					path_dir = os.path.dirname(path)
					if not os.path.isdir(path_dir):
						os.makedirs(path_dir)
					self.__count_img += 1
					write_file_append('img_log', url_latest + '\n')
					print(colored('Url img: ', 'yellow') + url_latest)

					res = self.session.get(url_latest, headers=gen_headers)
					print(colored('Response code: ', 'yellow') + str(res.status_code))
					write_file_binary(path, res.content)
					print(colored('[!] Create successful img file!', 'white'))
					img['src'] = path
					
					print('-' * 80)

	# Extract all linked files from style attribute
	def __extract_style_attr(self, styles):

		for style in styles:
			for background in re.findall('url\(([^\)]*)', style.get('style')):
				url_latest = parse.urljoin(self.url, background)
				flag = False
				for image  in Clone.__imageExtension:
					if re.search('.' + image + '$', background):
						if isHttps(self.url) == True:	
							path = re.findall('https://[^/]*/(.*)', url_latest)[0]
						else:
							path = re.findall('http://[^/]*/(.*)', url_latest)[0]
						path = 'images/' + path
						for _url in read_file_line('img_log'):
							if _url.strip() == url_latest:
								flag = True
								style['style'] = style['style'].replace(background, path)
								break
						if not flag:
							flag = True
							path_dir = os.path.dirname(path)
							if not os.path.isdir(path_dir):
								os.makedirs(path_dir)
							self.__count_img += 1
							write_file_append('img_log', url_latest + '\n')
							print(colored('Url img: ', 'yellow') + url_latest)
							
							res = self.session.get(url_latest, headers=gen_headers)
							print(colored('Response code: ', 'yellow') + str(res.status_code))
							write_file_binary(path, res.content)
							style['style'] = style['style'].replace(background, path)
						
				if not flag:
					print (colored(url_latest, 'red'))
				

	# Extract all linked files from css content
	def __extract_css_content(self, data, url):

		for background in re.findall('url\(([^\)]*)', data):
			clone = background
			background = background.strip('"')
			url_latest = parse.urljoin(url, background)
			flag = False
			for image  in Clone.__imageExtension:
				if re.search('.' + image + '$', background):
					if isHttps(url) == True:	
						path = re.findall('https://[^/]*/(.*)', url_latest)[0]
					else:
						path = re.findall('http://[^/]*/(.*)', url_latest)[0]
					path = 'images/' + path
					for _url in read_file_line('img_log'):
						if _url.strip() == url_latest:
							flag = True
							data = data.replace('url(' + clone, 'url(' + path)
							break
					if not flag:
						flag = True
						
						path_dir = os.path.dirname(path)
						if not os.path.isdir(path_dir):
							os.makedirs(path_dir)
						self.__count_img += 1
						write_file_append('img_log', url_latest + '\n')
						print(colored('Url img: ', 'red') + url_latest)
					
						res = self.session.get(url_latest, headers=gen_headers)
						print(colored('Response code: ', 'red') + str(res.status_code))
						write_file_binary(path, res.content)
						data = data.replace('url(' + clone, 'url(' + path)
					
			if not flag:
				print (colored(url_latest, 'red'))
		return data







		
