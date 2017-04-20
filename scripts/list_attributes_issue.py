import csv
import re
import sys

## Take long to execute !!!!!!!

filename = "issue_cleaned.csv"

attributeNames = []

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)


def getCleanedDefault(item, id):
	itemRegex1 = re.search(r"^([A-Za-z\s]+:)?([^\]\[\(\);]+).*$", item)
	itemRegex2 = re.search(r"^[\[\(]([A-Z][\w\s\.]+)[\)\]]\s?$", item)
	itemRegex3 = re.search(r"^\[([A-Za-z\s]+)\(.*\)\]$", item)

	if itemRegex1 or itemRegex2 or itemRegex3:
		if itemRegex1:
			cleanedItem = itemRegex1.group(2)
		elif itemRegex2: 
			cleanedItem = itemRegex2.group(1)
		else:
			cleanedItem = itemRegex3.group(1)

		if cleanedItem == ' ':
			return None
		else:
			return cleanedItem

	else:
		print("""{} : {}""".format(id, item))
		return None


def writeRelFiles(newEntityFileName, newRelationFileName, header, attribute, getCleanedItem):
	addedItem = []
	itemCnt = 0

	with open(filename, 'r') as f, open(newEntityFileName, "w") as charFile, open(newRelationFileName, "w") as relationFile:
		reader = csv.DictReader(f)

		writer = csv.DictWriter(charFile, fieldnames=['id', 'name'])
		writer.writeheader()

		relationWriter = csv.DictWriter(relationFile, fieldnames=header)
		relationWriter.writeheader()

		for row in reader:
			elem = row[attribute]
			if elem != "NULL":
				elem = row[attribute].replace(';;',';')
				regex = r"^([^;]+)(;[^;]+)*;?$"

				if not re.search(regex, elem):
					print(elem)

				elif re.search(regex, elem):
					groupTuples = re.findall(regex, elem)
					for t in groupTuples:
						for c in t:
							if c != '':
								item = c.replace('; ', '').replace('"','').replace('?','')

								if re.search(r"^;(.*)$", item):
									item = re.search(r"^;(.*)$", item).group(1)

								if item != '':

									cleanedItem = getCleanedItem(item, row['id'])

									if cleanedItem != None:

										spaceRegex = re.search(r"^\s*([^\s]+\s*[^\s]+)\s*$", cleanedItem)

										if spaceRegex:
											cleanedItem = spaceRegex.group(1)
										
											if cleanedItem != None and cleanedItem != '' and cleanedItem != ' ':
												if cleanedItem.lower() not in addedItem:
													addedItem.append(cleanedItem.lower())
													writer.writerow({'id': itemCnt, 'name': cleanedItem})
													itemCnt += 1

												relationWriter.writerow({header[0]: row["id"], header[1]: addedItem.index(cleanedItem.lower())})




# writeRelFiles("issue_editing.csv", "issue_has_editing.csv", ['issue_id', 'editing_id'], 'editing', getCleanedDefault)

writeRelFiles("issue_colors.csv", "issue_has_colors.csv", ['issue_id', 'color_id'], 'color', getCleanedDefault)