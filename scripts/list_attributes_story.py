import csv
import re
import sys

## Take a long to execute !!!!!!!

filename = "story_cleaned.csv"

attributeNames = []
addedGenres = []
genreCnt = 0
testCnt = 0

with open(filename, 'r') as f:
	reader = csv.reader(f)
	attributeNames = next(reader)


# with open(filename, 'r') as f, open("story_genre.csv", "w") as genreFile, open("story_has_genre.csv", "w") as relationFile:
# 	reader = csv.DictReader(f)

# 	writer = csv.DictWriter(genreFile, fieldnames=['id', 'name'])
# 	writer.writeheader()

# 	relationWriter = csv.DictWriter(relationFile, fieldnames=['story_id', 'genre_id'])
# 	relationWriter.writeheader()

# 	for row in reader:

# 		if row["genre"] != "NULL":
# 			testCnt += 1
# 			elem = row["genre"]
# 			regex = r"^([A-Za-z-\s&]+);?\s?(;\s?[A-Za-z-\s&]+;?)*$"

# 			if not re.search(regex, elem):
# 				print(elem)

# 			elif re.search(regex, elem):
# 				groupTuples = re.findall(regex, elem)
# 				for t in groupTuples:
# 					for g in t:
# 						if g != '':
# 							if re.search(r"^;?\s*([A-Za-z-\s&]+);?\s?$", g):
# 								genre = re.search(r"^;?\s*([A-Za-z-\s&]+);?\s?$", g).group(1)

# 								if genre not in addedGenres:
# 									addedGenres.append(genre)
# 									writer.writerow({'id': genreCnt, 'name': genre})
# 									genreCnt += 1

# 								relationWriter.writerow({'story_id': row["id"], 'genre_id': addedGenres.index(genre)})

# 							elif not re.search(r"^;?\s*([A-Za-z-\s&]+);?\s?$", g):
# 								print(row['id'])

# print(testCnt)


# addedChar = []
# charCnt = 0

# with open(filename, 'r') as f, open("story_characters.csv", "w") as charFile, open("story_has_characters.csv", "w") as relationFile:
# 	reader = csv.DictReader(f)

# 	writer = csv.DictWriter(charFile, fieldnames=['id', 'name'])
# 	writer.writeheader()

# 	relationWriter = csv.DictWriter(relationFile, fieldnames=['story_id', 'character_id'])
# 	relationWriter.writeheader()

# 	for row in reader:
# 		if row["characters"] != "NULL":
# 			elem = row["characters"].replace(';;',';')
# 			regex = r"^([^;]+)(;[^;]+)*;?$"

# 			if not re.search(regex, elem):
# 				print(elem)

# 			elif re.search(regex, elem):
# 				groupTuples = re.findall(regex, elem)
# 				for t in groupTuples:
# 					for c in t:
# 						if c != '':
# 							character = c.replace('; ', '').replace('"','')

# 							if re.search(r"^;(.*)$", character):
# 								character = re.search(r"^;(.*)$", character).group(1)

# 							if character != '':
# 								charRegex = re.search(r"^([A-Za-z\s]+:)?([^\]\[\(\);]+).*$", character)
# 								if charRegex:
# 									cleanedChar = charRegex.group(2)

# 									if cleanedChar.lower() not in addedChar:
# 										addedChar.append(cleanedChar.lower())
# 										writer.writerow({'id': charCnt, 'name': cleanedChar})
# 										charCnt += 1

# 									relationWriter.writerow({'story_id': row["id"], 'character_id': addedChar.index(cleanedChar.lower())})

# 								else:
# 									print(character)

addedArtist = []
artistCnt = 0

with open(filename, 'r') as f, open("story_artist.csv", "w") as charFile, open("story_has_artists.csv", "w") as relationFile:
	reader = csv.DictReader(f)

	writer = csv.DictWriter(charFile, fieldnames=['id', 'name'])
	writer.writeheader()

	relationWriter = csv.DictWriter(relationFile, fieldnames=['story_id', 'artist_id'])
	relationWriter.writeheader()

	for row in reader:
		for attribute in ["script", "pencils", "inks", "colors"]:
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
								artist = c.replace('; ', '').replace('"','').replace('?','')

								if re.search(r"^;(.*)$", artist):
									artist = re.search(r"^;(.*)$", artist).group(1)

								if artist != '':
									artRegex1 = re.search(r"^([A-Za-z\s]+:)?([^\]\[\(\);]+).*$", artist)
									artRegex2 = re.search(r"^[\[\(]([A-Z][\w\s\.]+)[\)\]]\s?$", artist)

									if artRegex1 or artRegex2:
										if artRegex1:
											cleanedArtist = artRegex1.group(2)
										else: 
											cleanedArtist = artRegex2.group(1)
											
										if cleanedArtist != '':
											if cleanedArtist.lower() not in addedArtist:
												addedArtist.append(cleanedArtist.lower())
												writer.writerow({'id': artistCnt, 'name': cleanedArtist})
												artistCnt += 1

											relationWriter.writerow({'story_id': row["id"], 'artist_id': addedArtist.index(cleanedArtist.lower())})

									else:
										print(artist)



