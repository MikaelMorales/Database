import csv
import re
import sys

## Take long to execute !!!!!!!

filename = "story_cleaned.csv"

attributeNames = []

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)


def getCleanedArtist(artist, id):
	artRegex1 = re.search(r"^([A-Za-z\s]+:)?([^\]\[\(\);]+).*$", artist)
	artRegex2 = re.search(r"^[\[\(]([A-Z][\w\s\.]+)[\)\]]\s?$", artist)

	if artRegex1 or artRegex2:
		if artRegex1:
			cleanedArtist = artRegex1.group(2)
		else: 
			cleanedArtist = artRegex2.group(1)
		
		return cleanedArtist

	else:
		print("""{} => {} : {}""".format("artists", id, artist))
		return None


def getCleanedChar(character, id):
	character.replace(" and ", ";").replace(" & ", ";")
	charRegex = re.search(r"^([A-Za-z\s]+:)?([^\]\[\(\);]+).*$", character)
	if charRegex:
		cleanedChar = charRegex.group(2)

		return cleanedChar

	else:
		print("""{} => {} : {}""".format("characters", id, character))
		return None


def getCleanedGenre(genre, id):
	genreRegex = re.search(r"^;?\s*([A-Za-z-\s&]+);?\s?$", genre)
	if genreRegex:
		cleanedGenre = genreRegex.group(1)

		return cleanedGenre

	else:
		print("""{} => {} : {}""".format("genre", id, genre))
		return None


def getCleanedFeature(feature, id):
	feature.replace(" and ", ";").replace(" & ", ";")
	featureRegex1 = re.search(r"^([A-Za-z\s]+:)?([^\]\[\(\);]+).*$", feature)
	featureRegex2 = re.search(r"^\[([\w\'\.\sÖ&åäø\-’]+)\]$", feature)
	if featureRegex1 or featureRegex2:
		if featureRegex1: 
			cleanedFeature = featureRegex1.group(2)
		else:
			cleanedFeature = featureRegex2.group(1)

		return cleanedFeature

	else:
		print("""{} => {} : {}""".format("features", id, feature))
		return None



def writeRelFiles(newEntityFileName, newRelationFileName, header, attributes, getCleanedItem):
	addedItem = []
	itemCnt = 0

	with open(filename, 'r') as f, open(newEntityFileName, "w") as charFile, open(newRelationFileName, "w") as relationFile:
		reader = csv.DictReader(f)

		writer = csv.DictWriter(charFile, fieldnames=['id', 'name'])
		writer.writeheader()

		relationWriter = csv.DictWriter(relationFile, fieldnames=header)
		relationWriter.writeheader()

		for row in reader:
			for attribute in attributes:
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
											
											if cleanedItem != '':
												if cleanedItem.lower() not in addedItem:
													addedItem.append(cleanedItem.lower())
													writer.writerow({'id': itemCnt, 'name': cleanedItem})
													itemCnt += 1

												relationWriter.writerow({header[0]: row["id"], header[1]: addedItem.index(cleanedItem.lower())})




# GET GENRE
# writeRelFiles("story_genres.csv", "story_has_genres.csv", ['story_id', 'genre_id'], ['genre'], getCleanedGenre)

# GET FEATURES
writeRelFiles("story_features.csv", "story_has_features.csv", ['story_id', 'feature_id'], ['feature'], getCleanedFeature)

