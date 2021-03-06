import csv
import re
import sys

filename = "series_cleaned.csv"

attributeNames = set()

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)


def getCleanedColor(color, id):
	cleanedColor = getCleanedDefault(color, id)
	if cleanedColor != None:
		return cleanedColor
	else :
		colorRegex = re.search(r"^;?\s*([A-Za-z-\s&]+);?\s?$", color)
		if colorRegex:
			cleanedColor = colorRegex.group(1)

			return cleanedColor

		else:
			print("""{} => {} : {}""".format("color", id, color))
			return None


def getCleanedDefault(item, id):
	itemRegex1 = re.search(r"^([A-Za-z\s]+:)?([^\]\[\(\);]+).*$", item)
	itemRegex2 = re.search(r"^[\[\(]([A-Z][\w\s\.]+)[\)\]]\s?$", item)

	if itemRegex1 or itemRegex2:
		if itemRegex1:
			cleanedItem = itemRegex1.group(2)
		else: 
			cleanedItem = itemRegex2.group(1)
		
		return cleanedItem

	else:
		print("""{} : {}""".format(id, item))
		return None


def writeRelFiles(newEntityFileName, newRelationFileName, header, attribute, getCleanedItem):
	addedItem = {}
	itemCnt = 0
	addedRel = set()

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
													addedItem.update({cleanedItem.lower(): itemCnt})
													writer.writerow({'id': itemCnt, 'name': cleanedItem})
													itemCnt += 1

												addedItemId = addedItem.get(cleanedItem.lower())

												if (row["id"], addedItemId) not in addedRel:
													addedRel.add((row["id"], addedItemId))
													relationWriter.writerow({header[0]: row["id"], header[1]: addedItemId})




# writeRelFiles("series_color.csv", "series_has_color.csv", ['series_id', 'color_id'], 'color', getCleanedColor)

writeRelFiles("series_paper_stock.csv", "series_has_paper_stock.csv", ['series_id', 'paper_stock_id'], 'paper_stock', getCleanedDefault)

# writeRelFiles("series_binding.csv", "series_has_binding.csv", ['series_id', 'binding_id'], 'binding', getCleanedDefault)




