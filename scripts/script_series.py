import csv
import re

filename = "series_updated.csv";

attributeNames = []

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)

with open(filename, 'r') as f, open("series_cleaned.csv", "w") as newf:
	dictReader = csv.DictReader(f)
	dictWriter = csv.DictWriter(newf, attributeNames)
	dictWriter.writeheader()
	for row in dictReader:
		newRow = {}
		for attribute in attributeNames:

			if attribute == "year_began" or attribute == "year_ended":
				year = row[attribute]
				cleanedYear = 0
				if not re.search(r"^\d\d\d\d$", year):
					cleanedYear = "NULL"
				else: 
					cleanedYear = year

				newRow.update({attribute: cleanedYear})

			elif attribute == "publication_dates" and row[attribute] != "NULL":
				year_began = int(row["year_began"])
				pubDates = row[attribute]
				cleanedPubDate = 0
				if pubDates == "0":
					cleanedPubDate = "NULL"
				elif re.search(r"(\d\d\d\d)", pubDates):
					cleanedPubDate = re.search(r"(\d\d\d\d)", pubDates).group(1)
				elif re.search(r"(\d\d\d)([\?x])", pubDates):
					cleanedPubDate = re.search(r"(\d\d\d)([\?x])", pubDates).group(1) + "0"
				else:
					print("""publication date : {}, id : {}""".format(pubDates, row["id"]))
					cleanedPubDate = year_began

				newRow.update({attribute: cleanedPubDate})

			else:
				newRow.update({attribute: row[attribute]})

		dictWriter.writerow(newRow)

with open("series_cleaned.csv", 'r') as f:
	invalAttribCnt = {}
	for attribute in attributeNames:
		invalAttribCnt.update({attribute: 0})

	dictReader = csv.DictReader(f)
	for row in dictReader:
		for attribute in attributeNames:
			if row[attribute] != "NULL":
				if attribute == "publication_dates":
					publication_dates = row[attribute]
					if not re.search(r"^\d{4}$", publication_dates):
						invalAttribCnt[attribute] += 1
						print("""{} : {} : ({})""".format(attribute, row["id"], row[attribute]))

				if attribute in ["first_issue_id", "last_issue_id", "publisher_id", "country_id", "language_id"]:
					if not re.search("^\d+$", row[attribute]):
						invalAttribCnt[attribute] += 1
						print("""{} : {} : {}""".format(attribute, row["id"], row[attribute]))

				if attribute == "year_began" or attribute == "year_ended":
					if not re.search("^\d\d\d\d$", row[attribute]):
						invalAttribCnt[attribute] += 1
						print("""{} : {} : {}""".format(attribute, row["id"], row[attribute]))

				if attribute == "publication_type_id":
					if not re.search("^\d+$", row[attribute]):
						invalAttribCnt[attribute] += 1
						print("""{} : {} : {}""".format(attribute, row["id"], row[attribute]))

	for attribute in attributeNames:
		print("""{} => {}""".format(attribute, invalAttribCnt[attribute]))