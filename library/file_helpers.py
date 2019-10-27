import os

def create_file(name):

	f = open(name, 'w')
	f.close()

def write_file(name, data):

	f = open(name, 'w')
	f.write(data)
	f.close()

def write_file_append(name, data):

	f = open(name, 'a')
	f.write(data)
	f.close()

def write_file_binary(name, data):

	f = open(name, 'wb')
	f.write(data)
	f.close()

def read_file_line(name):

	f = open(name, 'r')
	data = f.readlines()
	f.close()
	return data

