#!/usr/bin/env python3

from clone import Clone
import argparse
import os

def main():

	# Construct the argument parser
	ap = argparse.ArgumentParser()
    
	# Add the arguments to the parser
	ap.add_argument("-u", "--url", required=True, help="Enter the url")
	ap.add_argument("-o", "--output", help="Return the resulting directory")
	ap.add_argument("-d", "--delay", help="Delay the requested time")

	# Get arguments
	args = vars(ap.parse_args())
	url = args['url']
	directory = args['output']
	if args['delay']:
		delay = int(args['delay'])
	else:
		delay = 0

	os.system('clear')
 	
	clone = Clone(url)
	clone.run()

if __name__ == '__main__':
	main()