import csv
import re

filename = input("filename (only file containing reprint): ")

baseName, extention = filename.split('.');
baseName = baseName.replace("_updated", "")

attributeNames = []

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)
	attributeNames.remove("id")

newName = baseName + "_cleaned." + extention

with open(filename, 'r') as f, open(newName, "w") as newf:
	dictReader = csv.DictReader(f)
	dictWriter = csv.DictWriter(newf, attributeNames, delimiter=',')
	dictWriter.writeheader()

	for row in dictReader:
		newRow = {}
		for attribute in attributeNames:
			elem = row[attribute]
			if elem != "NULL":
				if attribute in ["origin_id", "target_id", "origin_issue_id", "target_issue_id"]:
					if not re.search(r"^\d+$", elem):
						print("""{} : {} : {}""".format(attribute, row["id"], elem))

					cleanedAttribute = elem
					newRow.update({attribute: cleanedAttribute})

		dictWriter.writerow(newRow)

with open(newName, 'r') as f, open("new_reprint.csv", "w") as newf:
	reader = csv.reader(f)
	writer = csv.writer(newf)

	rows = []

	for row in reader:
		if row not in rows:
			writer.writerow(row)
			rows.append(row)
