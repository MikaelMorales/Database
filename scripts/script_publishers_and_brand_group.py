import csv
import re

filename = input("filename (only file containing publisher and brand group): ")

baseName, extention = filename.split('.');
baseName = baseName.replace("_updated", "")

attributeNames = set()

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
				if attribute in set(["country_id", "publisher_id"]):
					if not re.search(r"^\d+$", elem):
						print("""{} : {} : {}""".format(attribute, row["id"], elem))
						cleanedAttribute = "NULL"

				elif attribute in ["year_began", "year_ended"]:
					if not re.search(r"^\d\d\d\d$", elem):
						cleanedAttribute = "NULL"

				elif attribute == "is_surrogate":
					if not re.search(r"^[01]$", elem):
					 	print("""{} : {} : {}""".format(attribute, row["id"], elem))

				elif attribute == "url":
					if not re.search(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)", elem):
					 	print("""{} : {} : {}""".format(attribute, row["id"], elem))

			newRow.update({attribute: cleanedAttribute})

		dictWriter.writerow(newRow)