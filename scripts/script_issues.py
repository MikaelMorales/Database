import csv
import re

filename = "issue_updated.csv";

attributeNames = []

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)

with open(filename, 'r') as f, open("issue_cleaned.csv", "w") as newf:
	dictReader = csv.DictReader(f)
	dictWriter = csv.DictWriter(newf, attributeNames)
	dictWriter.writeheader()
	for row in dictReader:
		newRow = {}
		for attribute in attributeNames:
			if (attribute == "publication_date" or attribute == "on_sale_date") and row[attribute] != "NULL":
				pubDates = row[attribute]
				cleanedPubDate = 0

				if re.search(r"(\d\d\d\d)", pubDates):
					cleanedPubDate = re.search(r"(\d\d\d\d)", pubDates).group(1)
				elif re.search(r"(\d\d\d)", pubDates):
					cleanedPubDate = re.search(r"(\d\d\d)", pubDates).group(1) + "0"
				elif re.search(r"(\[)(\d\d\d)", pubDates):
					cleanedPubDate = re.search(r"(\[)(\d\d\d)", pubDates).group(2) + "0"
				elif re.search(r"^(\d{1,2}[-/.]\d{1,2}[-/.])(\d\d)$", pubDates):
					cleanedPubDate = "19" + re.search(r"^(\d{1,2}[-/.]\d{1,2}[-/.])(\d\d)$", pubDates).group(2)
				elif re.search(r"^(\d{1,2}[-/])(\d\d)$", pubDates):
					cleanedPubDate = "19" + re.search(r"^(\d{1,2}[-/])(\d\d)$", pubDates).group(2)
				elif re.search(r"^([a-zA-Z????]*[\s-])(\d\d)(-\d\d)?$", pubDates):
					cleanedPubDate = "19" + re.search(r"^([a-zA-Z????]*[\s-])(\d\d)(-\d\d)?$", pubDates).group(2)
				elif re.search(r"^([a-zA-Z]+)?([\s-]?\d{0,2}[\s-][a-zA-Z]+[\s-]'?)(\d\d)$", pubDates):
					cleanedPubDate = "19" + re.search(r"^([a-zA-Z]+)?([\s-]?\d{0,2}[\s-][a-zA-Z]+[\s-]'?)(\d\d)$", pubDates).group(3)
				else:
					# print("""{} : {}, id : {}""".format(attribute, pubDates, row["id"]))
					cleanedPubDate = "NULL"

				newRow.update({attribute: cleanedPubDate})

			elif attribute == "price" and row[attribute] != "NULL":
				cleanedPrice = 0

				if re.search(r"free", row[attribute], re.IGNORECASE) or row["price"] in ["gratis", "Gratis", "0.00", "None [Giveaway]", "[gratis]", "0.00 FREE"]:
					cleanedPrice = "0.00 USD"

				elif re.search(r"^\.", row[attribute]):
					cleanedPrice = "NULL"

				elif re.search(r"(\d{1,5}\.\d{1,5})\s{0,2}([A-Za-z]{3})", row[attribute]):
					regexRes = re.search(r"(\d{1,5}\.\d{1,5})\s{0,2}([A-Za-z]{3})", row[attribute])
					cleanedPrice = regexRes.group(1) + " " + regexRes.group(2)

				elif re.search(r"(\d{1,5})\s{0,2}([A-Za-z]{3})", row[attribute]):
					regexRes = re.search(r"(\d{1,5})\s{0,2}([A-Za-z]{3})", row[attribute])
					cleanedPrice = regexRes.group(1) + ".00 " + regexRes.group(2)

				elif re.search(r"^\d{0,5}$", row[attribute]):
					regexRes = re.search(r"^(\d{0,5})$", row[attribute])
					cleanedPrice = regexRes.group(1) + ".00 USD"

				elif re.search(r"^(\d{0,5}\.\d{1,3})$", row[attribute]):
					regexRes = re.search(r"^(\d{0,5}\.\d{1,3})$", row[attribute])
					cleanedPrice = regexRes.group(1) + " USD"

				elif re.search(r"free", row["price"], re.IGNORECASE) or row["price"] in ["gratis", "Gratis", "0.00", "None [Giveaway]", "[gratis]"]:
					cleanedPrice = "0.00 USD"

				elif row["price"] != "NULL":
					cleanedPrice = "NULL"

				newRow.update({attribute: cleanedPrice})

			else:
				newRow.update({attribute: row[attribute]})

		dictWriter.writerow(newRow)

with open("issue_cleaned.csv", 'r') as f:

	invalAttribCnt = {}
	for attribute in attributeNames:
		invalAttribCnt.update({attribute: 0})

	dictReader = csv.DictReader(f)
	for row in dictReader:
		for attribute in attributeNames:
			if attribute == "publication_date" or attribute == "on_sale_date":
				date = row[attribute]
				if date != "NULL" and not re.search(r"^\d{4}$", date):
					if attribute == "on_sale_date":
						invalAttribCnt[attribute] += 1
					else:
						invalAttribCnt[attribute] += 1
					print("""{} : {} : {}""".format(attribute, row["id"], row[attribute]))

			if attribute == "price":
				price = row[attribute]
				if price != "NULL" and not re.search(r"^\d{1,5}\.\d{1,5}\s[A-Za-z]{3}$", price):
					invalAttribCnt[attribute] += 1
					print("""{} : {} : {}""".format(attribute, row["id"], row[attribute]))

			if attribute == "series_id":
				if row[attribute] == "NULL" or not re.search(r"^\d+$", row[attribute]):
					invalAttribCnt[attribute] += 1

			if attribute == "indicia_publisher_id":
				if row[attribute] != "NULL" and not re.search(r"^\d+$", row[attribute]):
					invalAttribCnt[attribute] += 1
					print("""{} : {} : {}""".format(attribute, row["id"], row[attribute]))

	for attribute in attributeNames:
		print("""{} => {}""".format(attribute, invalAttribCnt[attribute]))

