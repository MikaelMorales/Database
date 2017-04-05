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
			year_began = int(row["year_began"])
			if attribute == "publication_dates" and row[attribute] != "NULL":
				pubDates = row[attribute]
				cleanedPubDate = 0

				if re.search(r"^(\d\d\d\d)(.*)$", pubDates):
					cleanedPubDate = re.search(r"^(\d\d\d\d)(.*)$", pubDates).group(1)
				elif re.search(r"^(\[)(\d\d\d\d)(])$", pubDates):
					cleanedPubDate = re.search(r"^(\[)(\d\d\d\d)(])$", pubDates).group(2)
				elif re.search(r"^([^\d\d\d\d]+)(\d\d\d\d)(.*)$", pubDates):
					cleanedPubDate = re.search(r"^([^\d\d\d\d]+)(\d\d\d\d)(.*)$", pubDates).group(2)
				elif re.search(r"\d{1, 3}", pubDates) or cleanedPubDate < year_began:
					cleanedPubDate = year_began
				else:
					print("""publication date : {}, id : {}""".format(pubDates, row["id"]))
					cleanedPubDate = year_began

				newRow.update({attribute: cleanedPubDate})

			else:
				newRow.update({attribute: row[attribute]})

		dictWriter.writerow(newRow)

with open("series_cleaned.csv", 'r') as f:
	cnt = 0
	dictReader = csv.DictReader(f)
	for row in dictReader:
		for attribute in attributeNames:
			if attribute == "publication_dates":
				publication_dates = row[attribute]
				if publication_dates != "NULL" and not re.search(r"^\d{4}$", publication_dates):
					cnt += 1
					print(row["id"])
	print("counter = ", cnt)