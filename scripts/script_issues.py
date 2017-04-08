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
			elem = row[attribute]
			cleanedAttrib = 0

			if (attribute == "publication_date" or attribute == "on_sale_date") and elem != "NULL":
				if re.search(r"(\d\d\d\d)", elem):
					cleanedAttrib = re.search(r"(\d\d\d\d)", elem).group(1)
				elif re.search(r"(\d\d\d)", elem):
					cleanedAttrib = re.search(r"(\d\d\d)", elem).group(1) + "0"
				elif re.search(r"(\[)(\d\d\d)", elem):
					cleanedAttrib = re.search(r"(\[)(\d\d\d)", elem).group(2) + "0"
				elif re.search(r"^(\d{1,2}[-/.]\d{1,2}[-/.])(\d\d)$", elem):
					cleanedAttrib = "19" + re.search(r"^(\d{1,2}[-/.]\d{1,2}[-/.])(\d\d)$", elem).group(2)
				elif re.search(r"^(\d{1,2}[-/])(\d\d)$", elem):
					cleanedAttrib = "19" + re.search(r"^(\d{1,2}[-/])(\d\d)$", elem).group(2)
				elif re.search(r"^([a-zA-Z????]*[\s-])(\d\d)(-\d\d)?$", elem):
					cleanedAttrib = "19" + re.search(r"^([a-zA-Z????]*[\s-])(\d\d)(-\d\d)?$", elem).group(2)
				elif re.search(r"^([a-zA-Z]+)?([\s-]?\d{0,2}[\s-][a-zA-Z]+[\s-]'?)(\d\d)$", elem):
					cleanedAttrib = "19" + re.search(r"^([a-zA-Z]+)?([\s-]?\d{0,2}[\s-][a-zA-Z]+[\s-]'?)(\d\d)$", elem).group(3)
				else:
					cleanedAttrib = "NULL"

			elif attribute == "price" and elem != "NULL":

				if re.search(r"free", elem, re.IGNORECASE) or row["price"] in ["gratis", "Gratis", "0.00", "None [Giveaway]", "[gratis]", "0.00 FREE"]:
					cleanedAttrib = "0.00 USD"

				elif re.search(r"^\.", elem):
					cleanedAttrib = "NULL"

				elif re.search(r"(\d{1,5}\.\d{1,5})\s{0,2}([A-Za-z]{3})", elem):
					regexRes = re.search(r"(\d{1,5}\.\d{1,5})\s{0,2}([A-Za-z]{3})", elem)
					cleanedAttrib = regexRes.group(1) + " " + regexRes.group(2)

				elif re.search(r"(\d{1,5})\s{0,2}([A-Za-z]{3})", elem):
					regexRes = re.search(r"(\d{1,5})\s{0,2}([A-Za-z]{3})", elem)
					cleanedAttrib = regexRes.group(1) + ".00 " + regexRes.group(2)

				elif re.search(r"^\d{0,5}$", elem):
					regexRes = re.search(r"^(\d{0,5})$", elem)
					cleanedAttrib = regexRes.group(1) + ".00 USD"

				elif re.search(r"^(\d{0,5}\.\d{1,3})$", elem):
					regexRes = re.search(r"^(\d{0,5}\.\d{1,3})$", elem)
					cleanedAttrib = regexRes.group(1) + " USD"

				elif re.search(r"free", row["price"], re.IGNORECASE) or row["price"] in ["gratis", "Gratis", "0.00", "None [Giveaway]", "[gratis]"]:
					cleanedAttrib = "0.00 USD"

				elif row["price"] != "NULL":
					cleanedAttrib = "NULL"
			else:
				cleanedAttrib = elem

			newRow.update({attribute: cleanedAttrib})

		dictWriter.writerow(newRow)

with open("issue_cleaned.csv", 'r') as f:

	invalAttribCnt = {}
	for attribute in attributeNames:
		invalAttribCnt.update({attribute: 0})

	dictReader = csv.DictReader(f)
	for row in dictReader:
		for attribute in attributeNames:
			elem = row[attribute]
			if attribute == "publication_date" or attribute == "on_sale_date":
				if elem != "NULL" and not re.search(r"^\d{4}$", elem):
					if attribute == "on_sale_date":
						invalAttribCnt[attribute] += 1
					else:
						invalAttribCnt[attribute] += 1
					print("""{} : {} : {}""".format(attribute, row["id"], elem))

			if attribute == "price":
				if elem != "NULL" and not re.search(r"^\d{1,5}\.\d{1,5}\s[A-Za-z]{3}$", elem):
					invalAttribCnt[attribute] += 1
					print("""{} : {} : {}""".format(attribute, row["id"], elem))

			if attribute == "series_id":
				if elem == "NULL" or not re.search(r"^\d+$", elem):
					invalAttribCnt[attribute] += 1

			if attribute == "indicia_publisher_id":
				if elem != "NULL" and not re.search(r"^\d+$", elem):
					invalAttribCnt[attribute] += 1
					print("""{} : {} : {}""".format(attribute, row["id"], elem))

	for attribute in attributeNames:
		print("""{} => {}""".format(attribute, invalAttribCnt[attribute]))

