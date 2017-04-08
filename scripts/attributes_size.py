import csv
import re

filename = input('Enter the filename : ');

attributeNames = []
attributeSizeCnt = {}

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)

for attribute in attributeNames:
	attributeSizeCnt.update({attribute: 0})

with open(filename, 'r') as f:
	dictReader = csv.DictReader(f, quoting=csv.QUOTE_NONE)
	for row in dictReader:
		for attribute in attributeNames:
			attributeSizeCnt[attribute] = max(attributeSizeCnt[attribute], len(row[attribute]))
			
for attribute in attributeNames:
	print("""{} => {}""".format(attribute, attributeSizeCnt[attribute]))