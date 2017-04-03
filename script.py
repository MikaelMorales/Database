import csv

filename = input('Enter the filename : ');

attributeNames = []
lineNb = 0

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)

baseName, extention = filename.split('.');
nullCnt = {}


for attribute in attributeNames:
	nullCnt.update({attribute: 0})

with open(filename, 'r') as f, open(baseName + "_updated." + extention, "w") as newf:
	dictReader = csv.DictReader(f)
	dictWriter = csv.DictWriter(newf, attributeNames)
	dictWriter.writeheader()
	for row in dictReader:
		lineNb += 1
		newRow = {}
		for attribute in attributeNames:
			if row[attribute] == None or row[attribute] == "null" or row[attribute] == '':
				newRow.update({attribute: "NULL"})
				nullCnt.update({attribute: nullCnt[attribute] + 1})
			else:
				newRow.update({attribute: row[attribute]})

		dictWriter.writerow(newRow)

print("""Total number of line : {}""".format(lineNb))
# We iterate on attributeNames to print in order
for attribute in attributeNames:
	print("""{} => {} <=> {}%""".format(attribute, nullCnt[attribute],round(nullCnt[attribute]/lineNb * 100, 2)))