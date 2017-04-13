import csv
import re

filename = "series_updated.csv";

attributeNames = []

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)
	attributeNames.remove("paper_stock")
	attributeNames.remove("binding")
	attributeNames.remove("color")

with open(filename, 'r') as f, open("series_cleaned.csv", "w") as newf:
	dictReader = csv.DictReader(f)
	dictWriter = csv.DictWriter(newf, attributeNames)
	dictWriter.writeheader()
	for row in dictReader:
		newRow = {}
		for attribute in attributeNames:
			elem = row[attribute]
			if attribute == "year_began" or attribute == "year_ended":
				if not re.search(r"^\d\d\d\d$", elem):
					cleanedAttrib = "NULL"
				else: 
					cleanedAttrib = elem

			elif attribute == "publication_dates" and row[attribute] != "NULL":
				year_began = int(row["year_began"])
				if elem == "0":
					cleanedAttrib = "NULL"
				elif re.search(r"(\d\d\d\d)", elem):
					cleanedAttrib = re.search(r"(\d\d\d\d)", elem).group(1)
				elif re.search(r"(\d\d\d)([\?x])", elem):
					cleanedAttrib = re.search(r"(\d\d\d)([\?x])", elem).group(1) + "0"
				else:
					print("""publication date : {}, id : {}""".format(elem, row["id"]))
					cleanedAttrib = year_began

			else:
				cleanedAttrib = elem
				
			newRow.update({attribute: cleanedAttrib})

		dictWriter.writerow(newRow)

with open("series_cleaned.csv", 'r') as f:
	invalAttribCnt = {}
	for attribute in attributeNames:
		invalAttribCnt.update({attribute: 0})

	dictReader = csv.DictReader(f)
	for row in dictReader:
		for attribute in attributeNames:
			if row[attribute] != "NULL":
				elem = row[attribute]
				if attribute == "publication_dates":
					if not re.search(r"^\d{4}$", elem):
						invalAttribCnt[attribute] += 1
						print("""{} : {} : ({})""".format(attribute, row["id"], elem))

				if attribute in ["first_issue_id", "last_issue_id", "publisher_id", "country_id", "language_id"]:
					if not re.search("^\d+$", row[attribute]):
						invalAttribCnt[attribute] += 1
						print("""{} : {} : {}""".format(attribute, row["id"], elem))

				if attribute == "year_began" or attribute == "year_ended":
					if not re.search("^\d\d\d\d$", elem):
						invalAttribCnt[attribute] += 1
						print("""{} : {} : {}""".format(attribute, row["id"], elem))

				if attribute == "publication_type_id":
					if not re.search("^\d+$", elem):
						invalAttribCnt[attribute] += 1
						print("""{} : {} : {}""".format(attribute, row["id"], elem))

	for attribute in attributeNames:
		print("""{} => {}""".format(attribute, invalAttribCnt[attribute]))