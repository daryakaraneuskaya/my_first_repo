""" Converter - is supposed to convert files from .wig format 
to .bedGraph format and otherwise.
Example usage
python converter.py /path/to/input/file.format"""

import sys 
import os

class Chromosome_fragment_bedGraph(object):
	def __init__(self, string):
		self.chromosome_name = string.split()[0]
		self.start = int(string.split()[1])
		self.end = int(string.split()[2])
		self.value = float(string.split()[3])


def convert_file(path, file_name):
	dir_name = os.path.dirname(path)
	with open(path,"r") as input_file:
		lines = input_file.readlines()

	output_file = open ("%s/file_name" % dir_name, "a+")
	track_line = lines[0]
	if format == "bedGraph":
		for line in lines[1:]:
			chromosome_fragment = Chromosome_fragment_bedGraph(line)

	elif format == "wiggle_0":

	else:
		print "Unsupported file format"



if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) == 0:
		print "Please give a valid path to input file"
	else: 
		path = args[0]
		file_ = path.split('/')[-1]
		file_name = file_.split('.')[0]
		convert_file(path, file_name)

    	print "File %s has been successfully converted" % file_