import csv
import re

filename = input("filename (only file containing reprint): ")

baseName, extention = filename.split('.');
baseName = baseName.replace("_updated", "")

attributeNames = set()

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)
	attributeNames.remove("id")

newName = baseName + "_cleaned." + extention

with open(filename, 'r') as f, open(newName, "w") as newf:
	dictReader = csv.DictReader(f)
	dictWriter = csv.DictWriter(newf, ["origin_id", "target_id"], delimiter=',')
	dictWriter.writeheader()

	for row in dictReader:
		newRow = {}
		for attribute in attributeNames:
			elem = row[attribute]
			if elem != "NULL":
				if not re.search(r"^\d+$", elem):
					print("""{} : {} : {}""".format(attribute, row["id"], elem))

				cleanedAttribute = elem
				newRow.update({attribute: cleanedAttribute})

		dictWriter.writerow(newRow)

with open(newName, 'r') as f, open("new_reprint.csv", "w") as newf:
	reader = csv.DictReader(f)
	writer = csv.writer(newf)

	rows = set()

	for row in reader:
		if row["origin_id"] not in rows:
			writer.writerow(row)
			rows.add(row["origin_id"])
