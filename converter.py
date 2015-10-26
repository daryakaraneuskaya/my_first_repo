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

def find(token, string):
	match = re.search(ur" "+token+"(\=)(\w+)", string)
	if match:
		if token == "type":
			return match
		else:
			return match.group(2)
	else:
		if token == "span":
			return 1
		elif token == "step":
			return 1
		
		else:
			return False


def write_to_output(path, format, file_name, chromosome_name, list_of_fragments, span):
	dir_name = os.path.dirname(path)
	if format == "wiggle_0":
		with open ("%s/%s.wig" % (dir_name, file_name),"a+") as output_file:
			output_file.write("variableStep chrom=%s span=%d\n" % (chromosome_name, span))
			for fragment in list_of_fragments:
				output_file.write("%d %.2f\n" % (fragment.start + 1, fragment.value))
		
	elif format == "bedGraph":
		with open ("%s/%s.bedGraph" % (dir_name, file_name),"a+") as output_file:
			for fragment in list_of_fragments:
				output_file.write("%s %d %d %.2f\n" % (fragment.name, fragment.start, fragment.end, fragment.value))
		

def convert_file(path, file_name):
	dir_name = os.path.dirname(path)
	with open(path,"r") as input_file:
		lines_ = input_file.readlines()
		lines = filter(lambda x: not re.match(r'^\s*$', x), lines_)
	
	track_line = lines[0]
	match = find("type", track_line)
	format = match.group(2)

	if format == "bedGraph":
		format_to_convert = "wiggle_0"
		changed_track = track_line[:match.start()]+"type="+format_to_convert+track_line[match.end():]
		with open ("%s/%s.wig" % (dir_name, file_name),"a+") as output_file:
			output_file.write(changed_track)
		list_of_fragments = []
		span_list = []
		chromosome_fragment = Chromosome_fragment_bedGraph(lines[1])
		chromosome_name_pr = chromosome_fragment.name
		span_list.append(chromosome_fragment.end - chromosome_fragment.start)
		for line in lines[2:]:
			span = min(span_list)
			chromosome_fragment = Chromosome_fragment_bedGraph(line)
			chromosome_name_current = chromosome_fragment.name
			if not chromosome_name_current == chromosome_name_pr:
				write_to_output(path, format_to_convert, file_name, chromosome_name_pr, list_of_fragments, span)
				list_of_fragments = []
				span_list = []
				chromosome_name_pr = chromosome_name_current
			span_list.append(chromosome_fragment.end - chromosome_fragment.start)
			list_of_fragments.append(chromosome_fragment)
		write_to_output(path, format_to_convert, file_name, chromosome_name_pr, list_of_fragments, span)
		

		

	elif format == "wiggle_0":
		format_to_convert = "bedGraph"
		list_of_fragments = []
		changed_track = track_line[:match.start()]+" type="+format_to_convert+track_line[match.end():]
		with open ("%s/%s.%s" % (dir_name, file_name, format),"a+") as output_file:
			output_file.write(changed_track)
		
		attribute_line = lines[1]
		step = attribute_line.split()[0]
		chromosome_name = find("chrom", attribute_line)
		span = find("span", attribute_line)				 
		if step == "fixedStep":
			step = find("step", attribute_line)
			start = int(find("start", attribute_line))-1
			for line in lines[2:]:
				if line.startswith("fixedStep"):
					#write_to_output(path, format_to_convert, file_name, chromosome_name, list_of_fragments, span)
					attribute_line = line
					step = attribute_line.split()[0]
					chromosome_name = find("chrom", attribute_line)
					span = find("span", attribute_line)
					step = find("step", attribute_line)
					start = int(find("start", attribute_line))-1
				else:
					value = line.strip()
					bedGraph_string = chromosome_name+ " " + str(start)+ " " + str(start+int(step))+ " " + value
					start += int(step)
					chromosome_fragment = Chromosome_fragment_bedGraph(bedGraph_string)
					list_of_fragments.append(chromosome_fragment)
			write_to_output(path, format_to_convert, file_name, chromosome_name, list_of_fragments, span)

		
		elif step == "variableStep":
			start = int(lines[2].split()[0])
			value = lines[2].split()[1]
			for line in lines[2:]:
				if line.startswith("variableStep"):
					end = start + span
					bedGraph_string = chromosome_name + " " + str(start) + " " + str(end) + " " + value
					fragment = Chromosome_fragment_bedGraph(bedGraph_string)
					list_of_fragments.append(fragment)
					chromosome_name = find("chrom", line)
					span = find("span", line)
					start = -1
				else: 
					if start == -1:
						start = line.split()[0]
						value = line.split()[1]
					else:
						end = line.split()[0]
						bedGraph_string = chromosome_name + " " + str(start) + " " + str(end) + " " + value
						fragment = Chromosome_fragment_bedGraph(bedGraph_string)
						list_of_fragments.append(fragment)
						start = end
						value = line.split()[1]

			write_to_output(path, format_to_convert, file_name, chromosome_name, list_of_fragments, span)
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