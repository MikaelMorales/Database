import csv
import re

filename = "story_updated.csv";

attributeNames = []

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)
	attributeNames.remove("characters")
	attributeNames.remove("genre")
	attributeNames.remove("script")
	attributeNames.remove("pencils")
	attributeNames.remove("inks")
	attributeNames.remove("colors")
	attributeNames.remove("feature")


with open(filename, 'r') as f, open("story_cleaned.csv", "w") as newf:
	dictReader = csv.DictReader(f)
	dictWriter = csv.DictWriter(newf, attributeNames, delimiter=',')
	dictWriter.writeheader()
	for row in dictReader:
		newRow = {}
		for attribute in attributeNames:
			elem = row[attribute]
			if attribute == "issue_id" or attribute == "type_id":
				if elem != "NULL" and not re.search("^\d+$", elem):
					print("""{} : {} : {}""".format(attribute, row["id"], elem))
					cleanedAttribute = "NULL"
				else: 
					cleanedAttribute = elem

			elif attribute == "genre" and elem != "NULL":
				cleanedAttribute = elem.lower()

			elif attribute == "title" and elem != "NULL":
				cleanedAttribute = elem.replace('"', '')

			elif attribute == "characters" and elem != "NULL":
				cleanedAttribute = elem.replace("&", ";").replace(" and ", ";")

			else:
				cleanedAttribute = elem

			newRow.update({attribute: cleanedAttribute})

		dictWriter.writerow(newRow)