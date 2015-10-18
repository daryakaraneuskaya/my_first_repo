""" Converter - is supposed to convert files from .wig format 
to .bedGraph format and otherwise.
Example usage
python converter.py /path/to/input/file.format"""

import sys 
import os
import re

class Chromosome_fragment_bedGraph(object):
	def __init__(self, string):
		self.name = string.split()[0]
		self.start = int(string.split()[1])
		self.end = int(string.split()[2])
		self.value = float(string.split()[3])


def write_to_output_wiggle(path, file_name, changed_track, chromosome_name, list_of_fragments):
	dir_name = os.path.dirname(path)
	output_file = open ("%s/%s.wig" % (dir_name, file_name),"a+")
	output_file.write(changed_track)
	output_file.write("variableStep chrom=%s\n" % chromosome_name)
	for fragment in list_of_fragments:
		output_file.write("%d %.2f\n" % (fragment.start + 1, fragment.value))
	output_file.close()


def convert_file(path, file_name):
	with open(path,"r") as input_file:
		lines = input_file.readlines()

	track_line = lines[0]
	match = re.search(ur"(type\=)(\w+)", track_line)
	format = match.group(2)
	if format == "bedGraph":
		changed_track = track_line[:match.start()]+"type=wiggle_0"+track_line[match.end():]
		list_of_fragments = []
		for line in lines[1:]:
			chromosome_fragment = Chromosome_fragment_bedGraph(line)
			chromosome_name = chromosome_fragment.name

			list_of_fragments.append(chromosome_fragment)
		write_to_output_wiggle(path, file_name, changed_track,chromosome_name, list_of_fragments)


	elif format == "wiggle_0":
		for line in lines[2:]:
			if step == "fixedStep":
				print "todo"
			elif step == "variableStep":
				print "todo"

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