import csv
import re
import sys

## Take long to execute !!!!!!!

filename = "story_cleaned.csv"

attributeNames = []

addedArtists = []
artistCnt = 0

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)


def getCleanedGenre(genre, id):
	genre.replace(" and ", ";").replace(" & ", ";")
	genreRegex = re.search(r"^;?\s*([A-Za-z-\s&]+);?\s?$", genre)
	if genreRegex:
		cleanedGenre = genreRegex.group(1)

		return cleanedGenre

	else:
		print("""{} => {} : {}""".format("genre", id, genre))
		return None


def getCleanedFeature(feature, id):
	cleanedFeature = getCleanedDefault(feature, id)
	if cleanedFeature != None:
		return cleanedFeature

	else :
		featureRegex = re.search(r"^\[([\w\'\.\sÖ&åäø\-’]+)\]$", feature)

		if featureRegex:
			cleanedFeature = featureRegex.group(1)

			return cleanedFeature

		else:
			print("""{} => {} : {}""".format("features", id, feature))
			return None



def getCleanedArtist(artist, id):
	cleanedArtist = getCleanedDefault(artist, id)
	if cleanedArtist != None:
		return cleanedArtist

	else:
		artRegex = re.search(r"^\s*[\[\(](as\s)?([A-Z][\w\s\.]+)[\)\]]\s?(\([a-z\s]+\))?$", artist)
		if artRegex:
			cleanedArtist = artRegex.group(2)
			
			return cleanedArtist

		else:
			print("""{} => {} : {}""".format("artists", id, artist))
			return None




def getCleanedDefault(item, id):
	item.replace(" and ", ";").replace(" & ", ";")
	itemRegex = re.search(r"^([A-Za-z\s]+:)?([^\]\[\(\);]+).*$", item)
	if itemRegex:
		cleanedItem = itemRegex.group(2)

		return cleanedItem

	else:
		return None


def writeRelFiles(newEntityFileName, newRelationFileName, header, attribute, getCleanedItem, addedItem, itemCnt, headerAlreadyWritten):
	addedRel = set()

	with open(filename, 'r') as f, open(newEntityFileName, "a") as charFile, open(newRelationFileName, "w") as relationFile:
		reader = csv.DictReader(f)

		writer = csv.DictWriter(charFile, fieldnames=['id', 'name'])
		
		if not headerAlreadyWritten:
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

												if (row["id"], addedItem.index(cleanedItem.lower())) not in addedRel:
													addedRel.add((row["id"], addedItem.index(cleanedItem.lower())))
													relationWriter.writerow({header[0]: row["id"], header[1]: addedItem.index(cleanedItem.lower())})
	return itemCnt



# # GET GENRE
# writeRelFiles("story_genres.csv", "story_has_genres.csv", ['story_id', 'genre_id'], 'genre', getCleanedGenre, [], 0, False)

# # GET FEATURES
# writeRelFiles("story_features.csv", "story_has_features.csv", ['story_id', 'feature_id'], 'feature', getCleanedFeature, [], 0, False)

# # GET CHARACTERS
# writeRelFiles("story_characters.csv", "story_has_characters.csv", ['story_id', 'character_id'], 'characters', getCleanedDefault, [], 0, False)

# GET ARTISTS
artistCnt = writeRelFiles("story_artists.csv", "story_has_inks.csv", ['story_id', 'artist_id'], 'inks', getCleanedArtist, addedArtists, artistCnt, False)
artistCnt = writeRelFiles("story_artists.csv", "story_has_colors.csv", ['story_id', 'artist_id'], 'colors', getCleanedArtist, addedArtists, artistCnt, True)
artistCnt = writeRelFiles("story_artists.csv", "story_has_pencils.csv", ['story_id', 'artist_id'], 'pencils', getCleanedArtist, addedArtists, artistCnt, True)
writeRelFiles("story_artists.csv", "story_has_script.csv", ['story_id', 'artist_id'], 'script', getCleanedArtist, addedArtists, artistCnt, True)


