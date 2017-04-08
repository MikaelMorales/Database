import csv
import re

filename = input("filename (only file containing reprint): ")

baseName, extention = filename.split('.');
baseName = baseName.replace("_updated", "")

attributeNames = []

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)

with open(filename, 'r') as f, open(baseName + "_cleaned." + extention, "w") as newf:
	dictReader = csv.DictReader(f)
	dictWriter = csv.DictWriter(newf, attributeNames, delimiter=',')
	dictWriter.writeheader()
	for row in dictReader:
		newRow = {}
		for attribute in attributeNames:
			elem = row[attribute]
			cleanedAttribute = elem
			if elem != "NULL":
				if attribute in ["origin_id", "target_id", "origin_issue_id", "target_issue_id"]:
					if not re.search(r"^\d+$", elem):
						print("""{} : {} : {}""".format(attribute, row["id"], elem))

			newRow.update({attribute: cleanedAttribute})

		dictWriter.writerow(newRow)