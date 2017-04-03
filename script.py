import csv

filename = input('Enter the filename : ');

attribute_names = []

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attribute_names = next(reader)

filenameDecomposed = filename.split('.');

with open(filename, 'r') as f, open(filenameDecomposed[0] + "_updated." + filenameDecomposed[1], "w") as newf:
	dictReader = csv.DictReader(f)
	dictWriter = csv.DictWriter(newf, attribute_names)
	dictWriter.writeheader()
	for row in dictReader:
		newRow = {}

		for attribute in attribute_names:
			if row[attribute] == None or row[attribute] == "null" or row[attribute] == '':
				newRow.update({attribute: "NULL"})
			else:
				newRow.update({attribute: row[attribute]})

		dictWriter.writerow(newRow)


