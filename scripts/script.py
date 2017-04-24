import csv
import re

filename = input('Enter the filename : ');

attributeNames = set()
lineNb = 0

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)

baseName, extention = filename.split('.');
nullCnt = {}
emptyValues = set(["NULL", "null", "", "[nn]", "?", "NONE", "[none]", "none", "[undated]", "[no date]", "[No date]", "[?]", "[ongedateerd]", "[Unknown]", "[none given]", "none given", "[none listed]", "None listed", "None Listed", "no date", "Unknown", "[None]", "None [Premium]", "Premium [None]", "None", "nessuno", "na", "0?", "0 ?", "N/A", "n/a", "[aucun]", "[NONE]", "[none", "[ohne]", "uvurderlig", "[none] (see notes)", "[None see notes]", "[none?]", "none shown", "None Shown", "None indicated", "[none]s", "no coverpr", "see note", "[no price listed]", "[aucun indiqué]", "[see note]", "none listed", "(see Notes)", "0.00 [None]", "[esc 000]", "[None] (See Notes)", "[see notes]", "[none] (see note)"])
illId = 0

for attribute in attributeNames:
	nullCnt.update({attribute: 0})

with open(filename, 'r') as f, open(baseName + "_updated." + extention, "w") as newf:
	dictReader = csv.DictReader(f, quoting=csv.QUOTE_NONE)
	# dictWriter = csv.DictWriter(newf, attributeNames, quoting=csv.QUOTE_NONE, escapechar='\\')
	dictWriter = csv.DictWriter(newf, attributeNames, delimiter=',')
	dictWriter.writeheader()
	for row in dictReader:
		lineNb += 1
		newRow = {}
		for attribute in attributeNames:
			if row[attribute] == None or row[attribute] in emptyValues:
				newRow.update({attribute: "NULL"})
				nullCnt.update({attribute: nullCnt[attribute] + 1})
			else:
				newRow.update({attribute: row[attribute]})

			if attribute == "id" and not re.search(r"^\d+$", row[attribute]):
				illId += 1

		dictWriter.writerow(newRow)

print("""Total number of line : {}""".format(lineNb))
# We iterate on attributeNames to print in order
for attribute in attributeNames:
	print("""{} => {} <=> {}%""".format(attribute, nullCnt[attribute],round(nullCnt[attribute]/lineNb * 100, 2)))

print("bad id counter : ", illId)